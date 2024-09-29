from django.views.generic import ListView, DetailView, TemplateView, View
from django.shortcuts import get_object_or_404, redirect
from django.http import HttpResponseBadRequest

from .models import Product, Cart, CartProduct


class ProductListView(ListView):
    model = Product
    template_name = "ec/index.html"
    context_object_name = "product_list"

    def get_queryset(self):
        return Product.objects.prefetch_related("images")


class ProductDetailView(DetailView):
    model = Product
    template_name = "ec/detail.html"
    context_object_name = "product"

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["related_product_list"] = Product.objects.prefetch_related(
            "images"
        ).order_by("-created_at")[:4]
        return context


class CheckoutView(TemplateView):
    template_name = "ec/checkout.html"

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)

        # セッションキーの取得
        session_key = self.request.session.session_key
        # セッションキーが存在しない場合は、空のカートとする
        if not session_key:
            context["cart_product_list"] = []
            return context

        try:
            # カートの取得
            cart = Cart.objects.prefetch_related("products").get(
                session_key=session_key
            )

            # カート内の合計金額の計算
            total_amount = 0
            for cp in cart.products.all():
                # 各カート商品の小計を加算
                total_amount += cp.sub_total

            # カート内商品と合計金額をコンテキストに渡す
            context["cart_product_list"] = cart.products.all()
            context["total_amount"] = total_amount

        except Cart.DoesNotExist:
            # カートが存在しない場合は空のカートとする
            context["cart_product_list"] = []

        return context


class AddToCartView(View):
    """商品をカートに追加する処理"""

    def post(self, request, *args, **kwargs):
        # フォームデータから商品ID取得
        product_id = request.POST.get("product_id")
        if not product_id:
            return HttpResponseBadRequest("商品が選択されていません。")

        # 商品の取得（存在しない場合404エラー）
        product = get_object_or_404(Product, pk=product_id)

        try:
            # フォームデータから数量取得（一覧画面からのカート追加の場合、デフォルト値1が入る）
            quantity = int(request.POST.get("quantity", 1))
            # 数量チェック
            if quantity < 1:
                return HttpResponseBadRequest("数量は1以上である必要があります。")
        except ValueError:
            return HttpResponseBadRequest("無効な数量が指定されました。")

        # セッションキーの取得
        session_key = request.session.session_key
        # セッションキーが存在しない場合は、新規作成
        if not session_key:
            request.session.create()
            session_key = request.session.session_key

        # 既存カートの取得、なければ新規カートの作成
        cart, _created = Cart.objects.get_or_create(session_key=session_key)

        # カート商品の取得、なければ新規カート商品の作成
        cart_product, created_product = CartProduct.objects.get_or_create(
            cart=cart, product=product
        )

        # 数量の更新
        if created_product:
            # 新規商品をカートに追加する場合
            cart_product.quantity = quantity
        else:
            # 既存商品をカートに追加する場合
            cart_product.quantity += quantity

        # カート商品の保存
        cart_product.save()

        # リクエスト元のURL取得
        # 参考：https://just-python.com/document/django/views-basic/request-method
        incoming_url = request.META.get("HTTP_REFERER")

        # リクエスト元のURLが存在する場合は、そのURLにリダイレクト
        # MEMO：詳細ページからPOSTリクエストした際には、詳細ページにリダイレクトしたかったため、この実装にしている。
        if incoming_url:
            return redirect(incoming_url)
        else:
            return redirect("ec:product_list")


class DeleteFromCart(View):
    """商品をカートから削除する処理"""

    def post(self, request, *args, **kwargs):
        # フォームデータからカート商品ID取得
        cart_product_id = request.POST.get("cart_product_id")

        # カート商品の取得（存在しない場合404エラー）
        cart_product = get_object_or_404(CartProduct, pk=cart_product_id)

        # カートから削除
        cart_product.delete()

        # チェックアウトページにリダイレクト
        return redirect("ec:checkout")


# TODO:セッション有効期限が切れたカートの削除処理処理いる？
