from django.views.generic import ListView, DetailView, CreateView, View
from django.shortcuts import get_object_or_404, redirect
from django.http import HttpResponseBadRequest
from django.urls import reverse_lazy
from django.db import transaction
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings

from .forms import CheckoutForm
from .models import Product, Cart, CartProduct, Order, OrderDetail


class ProductListView(ListView):
    model = Product
    template_name = "ec/index.html"
    context_object_name = "product_list"

    def get_queryset(self):
        return Product.objects.prefetch_related("images")

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        # カート商品数をコンテキストに設定
        context["cart_product_count"] = get_cart_product_count(self.request)
        return context


class ProductDetailView(DetailView):
    model = Product
    template_name = "ec/detail.html"
    context_object_name = "product"

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["related_product_list"] = Product.objects.prefetch_related(
            "images"
        ).order_by("-created_at")[:4]
        # カート商品数をコンテキストに設定
        context["cart_product_count"] = get_cart_product_count(self.request)
        return context


class CheckoutView(CreateView):
    model = Order
    form_class = CheckoutForm
    template_name = "ec/checkout.html"
    success_url = reverse_lazy("ec:product_list")

    def get(self, *args, **kwargs):
        # カート取得
        cart = get_cart_by_session(self.request)
        # カートが存在しない場合、一覧ページにリダイレクト
        if not cart:
            messages.error(self.request, "カートが空です。", extra_tags="danger")
            return redirect("ec:product_list")
        return super().get(*args, **kwargs)

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        # カート取得
        cart = get_cart_by_session(self.request)
        # カート関連の情報をコンテキストに設定
        context["cart"] = cart
        context["cart_product_list"] = cart.products.all() if cart else []
        return context

    def form_valid(self, form):
        """フォームが有効な場合の処理"""
        try:
            # トランザクション開始
            with transaction.atomic():
                # 注文情報を保存
                order = form.save()
                # 注文詳細データの作成
                self.create_order_detail(order=order)

            # 注文詳細データの取得（必要なデータのみを抽出した辞書型）
            order_details = OrderDetail.objects.filter(order=order).values(
                "product__name", "quantity", "price"
            )
            # 注文詳細メールの送信処理
            self.send_order_detail_mail(order=order, order_details=order_details)

        except Exception as e:
            print(f"チェックアウト処理中に例外が発生しました！：{str(e)}")
            messages.error(
                self.request,
                "チェックアウト処理に失敗しました。もう一度お試しください。",
            )
            # チェックアウトページにリダイレクト
            return redirect("ec:checkout")

        else:
            print("チェックアウト処理が正常に完了しました！")
            messages.success(
                self.request, "購入ありがとうございます！", extra_tags="success"
            )
            return super().form_valid(form)

    def create_order_detail(self, order):
        """注文詳細データを保存する処理"""
        # カート取得
        cart = get_cart_by_session(self.request)
        if not cart:
            raise ValueError("カートが存在しません。")

        # カート内のすべての商品取得
        cart_products = cart.products.all()
        if not cart_products:
            raise ValueError("カート内に商品が存在しません。")

        # カート内の各商品を注文詳細として保存
        for cp in cart_products:
            order_detail = OrderDetail(
                order=order,
                product=cp.product,
                quantity=cp.quantity,
                price=cp.product.price,
            )
            order_detail.save()

        # カート削除（カスケード処理により、カート商品もすべて削除）
        cart.delete()

    def send_order_detail_mail(self, order, order_details):
        """注文詳細メールを送信する処理"""
        # メール本文の作成
        message_lines = [
            f"商品: {detail['product__name']}, 数量: {detail['quantity']}, 価格: {detail['price']}円\n"
            for detail in order_details
        ]
        message = "\n".join(message_lines)

        # メール送信
        send_mail(
            subject=f"【注文ID:{order.id}】ご注文頂きありがとうございます。",
            message=message,
            from_email=settings.FROM_EMAIL,
            recipient_list=[order.email],
        )
        print("注文詳細メールを送信しました！")


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
                messages.error(
                    self.request,
                    "数量は1以上である必要があります。",
                    extra_tags="danger",
                )
                return redirect("ec:product_detail", pk=product_id)
        except ValueError:
            # intへの変換に失敗した場合
            messages.error(
                self.request,
                "無効な数量が指定されました。",
                extra_tags="danger",
            )
            return redirect("ec:product_detail", pk=product_id)

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

        messages.info(
            self.request,
            f"カートに『{product.name}』を追加しました。",
            extra_tags="info",
        )

        # リクエスト元のURLが存在する場合は、そのURLにリダイレクト
        # MEMO：詳細ページからPOSTリクエストした際には、詳細ページにリダイレクトしたかったため、この実装にしている。
        if incoming_url:
            return redirect(incoming_url)
        else:
            return redirect("ec:product_list")


class DeleteFromCartView(View):
    """商品をカートから削除する処理"""

    def post(self, request, *args, **kwargs):
        # フォームデータからカート商品ID取得
        cart_product_id = request.POST.get("cart_product_id")

        # カート商品の取得（存在しない場合404エラー）
        cart_product = get_object_or_404(CartProduct, pk=cart_product_id)

        # カートから削除
        cart_product.delete()
        messages.error(
            self.request,
            f"カートから『{cart_product.product.name}』を削除しました",
            extra_tags="success",
        )

        # チェックアウトページにリダイレクト
        return redirect("ec:checkout")


def get_cart_by_session(request):
    """セッションキーに基づいてカートを取得する関数"""
    session_key = request.session.session_key
    if session_key:
        try:
            return Cart.objects.prefetch_related("products").get(
                session_key=session_key
            )
        except Cart.DoesNotExist:
            return None
    return None


def get_cart_product_count(request):
    """カート商品数を取得する処理"""
    cart = get_cart_by_session(request)
    if cart:
        # カートが存在する場合
        return cart.products.count()
    return 0


# TODO:セッション有効期限が切れたカートの削除処理処理いる？
