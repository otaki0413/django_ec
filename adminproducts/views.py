from django.views import generic
from .forms import ProductRegisterForm, ProductImageRegisterForm
from ec.models import Product, ProductImage
from django.urls import reverse_lazy

import cloudinary.uploader


class AdminProductListView(generic.ListView):
    model = Product
    template_name = "adminproducts/index.html"
    context_object_name = "product_list"

    def get_queryset(self):
        return Product.objects.prefetch_related("images")


class AdminProductRegisterView(generic.CreateView):
    model = Product
    form_class = ProductRegisterForm
    image_form_class = ProductImageRegisterForm
    template_name = "adminproducts/new.html"
    success_url = reverse_lazy("adminproducts:admin_product_list")

    def get_context_data(self, **kwargs):
        # 既存のコンテキストを取得
        context = super().get_context_data(**kwargs)
        # 画像フォームのインスタンスをコンテキストに設定
        if "image_form" not in context:
            context["image_form"] = self.image_form_class()
        return context

    def form_valid(self, form):
        """有効なフォームデータの場合に実行される処理"""
        # Productモデルのインスタンスを保存
        product = form.save()
        # 画像フォームのインスタンス生成（データとファイルをセットする）
        image_form = self.image_form_class(self.request.POST, self.request.FILES)

        # 画像フォームのデータが有効かつimageフィールドに画像がアップロードされている場合、保存処理を行う
        if image_form.is_valid() and image_form.cleaned_data.get("image"):
            # 画像データを一旦取得し、関連するProductインスタンスを追加
            product_image = image_form.save(commit=False)
            product_image.product = product
            # ProductImageモデルのインスタンスを保存
            product_image.save()

        # 親クラスのデフォルト処理（リダイレクトなど）を実行
        return super().form_valid(form)


class AdminProductEditView(generic.UpdateView):
    model = Product
    form_class = ProductRegisterForm
    image_form_class = ProductImageRegisterForm
    template_name = "adminproducts/edit.html"
    success_url = reverse_lazy("adminproducts:admin_product_list")

    def get_context_data(self, **kwargs):
        # 既存のコンテキストを取得
        context = super().get_context_data(**kwargs)
        # 画像フォームのインスタンスをコンテキストに設定
        if "image_form" not in context:
            context["image_form"] = self.image_form_class()
        return context

    def form_valid(self, form):
        """有効なフォームデータの場合に実行される処理"""
        # Productモデルのインスタンスを保存
        product = form.save()
        # 画像フォームのデータとファイルを取得
        image_form = self.image_form_class(self.request.POST, self.request.FILES)

        if image_form.is_valid():
            # 画像データを一旦取得し、関連するProductインスタンスを追加
            product_image = image_form.save(commit=False)
            product_image.product = product
            # ProductImageモデルのインスタンスを保存
            product_image.save()

        # 親クラスのデフォルト処理（リダイレクトなど）を実行
        return super().form_valid(form)


class AdminProductDeleteView(generic.DeleteView):
    model = Product
    template_name = "adminproducts/delete.html"
    success_url = reverse_lazy("adminproducts:admin_product_list")

    def form_valid(self, form):
        # 削除対象のProductインスタンス取得
        product = self.get_object()
        # 関連するProductImageインスタンス取得
        product_image = product.images.first()
        # 画像が存在する場合、Cloudinaryから削除
        if product_image and product_image.image:
            cloudinary.uploader.destroy(product_image.image.name, invalidate=True)

        return super().form_valid(form)
