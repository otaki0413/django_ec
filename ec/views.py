from django.views import generic
from django.shortcuts import get_object_or_404, redirect
from django.http import HttpResponseBadRequest

from .models import Product, Cart, CartProduct


class ProductListView(generic.ListView):
    model = Product
    template_name = "ec/index.html"
    context_object_name = "product_list"

    def get_queryset(self):
        return Product.objects.prefetch_related("images")


class ProductDetailView(generic.DetailView):
    model = Product
    template_name = "ec/detail.html"
    context_object_name = "product"

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["related_product_list"] = Product.objects.prefetch_related(
            "images"
        ).order_by("-created_at")[:4]
        return context


class CheckoutView(generic.TemplateView):
    template_name = "ec/checkout.html"


def add_to_cart(request):
    """商品をカートに追加する処理"""
    if request.method == "POST":
        # フォームデータから商品ID取得
        product_id = request.POST.get("product_id")
        if not product_id:
            return HttpResponseBadRequest("商品が選択されていません。")

        # 商品の取得（存在しない場合404エラー）
        product = get_object_or_404(Product, pk=product_id)

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
            cart_product.quantity = 1
        else:
            # 既存商品をカートに追加する場合
            cart_product.quantity += 1

        # カート商品の保存
        cart_product.save()

        # 商品一覧ページにリダイレクト
        return redirect("ec:product_list")

    return HttpResponseBadRequest("無効なリクエストです。")


# TODO:セッション有効期限が切れたカートの削除処理処理いる？
