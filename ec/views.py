import pprint

from django.views import generic
from django.shortcuts import get_object_or_404, redirect
from django.http import HttpResponseBadRequest

from .models import Product
from .cart import Cart


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
        # フォームデータから商品id取得
        product_id = request.POST.get("product_id")
        if not product_id:
            return HttpResponseBadRequest("商品が選択されていません。")

        # 商品の取得（存在しない場合404エラー）
        product = get_object_or_404(Product, pk=product_id)
        # セッションからカート生成
        cart = Cart.from_session(request.session, "cart")
        # カートに商品追加
        cart.add(product)
        # セッションにカート保存
        cart.save_session(request.session, "cart")
        # デバッグ用
        pprint.pprint(request.session["cart"])

        # 商品一覧ページにリダイレクト
        return redirect("ec:product_list")

    return HttpResponseBadRequest("無効なリクエストです。")
