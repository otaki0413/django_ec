from django import forms
from ec.models import Product, ProductImage


class ProductRegisterForm(forms.ModelForm):
    """商品登録フォーム"""

    class Meta:
        model = Product
        fields = ["name", "description", "price"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs["class"] = "form-control"


class ProductImageRegisterForm(forms.ModelForm):
    """商品画像登録フォーム"""

    class Meta:
        model = ProductImage
        fields = ["image"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["image"].widget.attrs["class"] = "form-control"
