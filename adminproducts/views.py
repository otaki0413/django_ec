from django.views import generic
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator

import cloudinary.uploader
from basicauth.decorators import basic_auth_required

from .forms import ProductRegisterForm, ProductImageRegisterForm
from ec.models import Product, ProductImage


@method_decorator(basic_auth_required, name="dispatch")
class AdminProductListView(generic.ListView):
    model = Product
    template_name = "adminproducts/index.html"
    context_object_name = "product_list"

    def get_queryset(self):
        return Product.objects.prefetch_related("images")


@method_decorator(basic_auth_required, name="dispatch")
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
        # Productモデルのインスタンスを保存
        product = form.save()
        # ProductImageモデルのインスタンスを保存
        self.save_product_image(product=product)
        return super().form_valid(form)

    def save_product_image(self, product):
        # 画像フォームのインスタンス生成（データとファイルをセットする）
        image_form = self.image_form_class(self.request.POST, self.request.FILES)
        # 画像フォームのデータが有効かつimageフィールドに画像がアップロードされている場合、保存処理を行う
        if image_form.is_valid() and image_form.cleaned_data.get("image"):
            # 画像データを一旦取得し、関連するProductインスタンスを追加
            product_image = image_form.save(commit=False)
            product_image.product = product
            product_image.save()


@method_decorator(basic_auth_required, name="dispatch")
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
        # Productモデルのインスタンスを保存
        product = form.save()
        # 画像データの更新処理
        self.update_product_image(product=product)
        return super().form_valid(form)

    def update_product_image(self, product):
        # 画像フォームのデータとファイルを取得
        image_form = self.image_form_class(self.request.POST, self.request.FILES)

        # 画像フォームのデータが有効かつimageフィールドに画像がアップロードされている場合、既存の画像を削除し、新規画像を保存する
        if image_form.is_valid() and image_form.cleaned_data.get("image"):
            # 既存の画像データ取得
            old_image = product.images.first()
            # 既存の画像が存在する場合、Cloudinaryから削除
            if old_image and old_image.image:
                cloudinary.uploader.destroy(old_image.image.name, invalidate=True)
                # 既存の画像レコード削除
                old_image.delete()

            # 新規画像データを取得し、関連するProductインスタンスを追加
            product_image = image_form.save(commit=False)
            product_image.product = product
            product_image.save()


@method_decorator(basic_auth_required, name="dispatch")
class AdminProductDeleteView(generic.DeleteView):
    model = Product
    template_name = "adminproducts/delete.html"
    success_url = reverse_lazy("adminproducts:admin_product_list")

    def form_valid(self, form):
        # 削除対象のProductインスタンス取得
        product = self.get_object()
        # 関連するProductImageインスタンス取得して、Cloudinaryから削除
        self.delete_image_from_cloudinary(product_image=product.images.first())
        return super().form_valid(form)

    def delete_image_from_cloudinary(self, product_image):
        # Cloudinaryから画像を削除する処理
        if product_image and product_image.image:
            cloudinary.uploader.destroy(product_image.image.name, invalidate=True)
