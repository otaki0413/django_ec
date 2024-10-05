from django import forms
from ec.models import Order


class CheckoutForm(forms.ModelForm):
    """チェックアウト用フォーム"""

    class Meta:
        model = Order
        fields = [
            "first_name",
            "last_name",
            "user_name",
            "email",
            "address1",
            "address2",
            "country",
            "state",
            "zip_code",
            "card_name",
            "card_number",
            "expiration_date",
            "cvv",
        ]
        widgets = {
            "email": forms.TextInput(attrs={"placeholder": "you@example.com"}),
            "address1": forms.Textarea(
                attrs={"rows": 2, "placeholder": "1234 Main St"}
            ),
            "address2": forms.Textarea(
                attrs={"rows": 2, "placeholder": "Apartment or suite"}
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 各フォームフィールドのBootstrap設定
        for field_name, field in self.fields.items():
            if (field_name == "country") or (field_name == "state"):
                # countryとstateのフィールドの場合
                field.widget.attrs["class"] = "form-select"
            else:
                # その他のフィールドの場合
                field.widget.attrs["class"] = "form-control"
