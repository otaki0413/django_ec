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
            "first_name": forms.TextInput(
                attrs={
                    "placeholder": "太郎",
                    "class": "form-control",
                }
            ),
            "last_name": forms.TextInput(
                attrs={
                    "rows": 2,
                    "placeholder": "佐藤",
                    "class": "form-control",
                }
            ),
            "user_name": forms.TextInput(
                attrs={"placeholder": "sato", "class": "form-control"}
            ),
            "email": forms.TextInput(
                attrs={"placeholder": "taro_sato@example.com", "class": "form-control"}
            ),
            "address1": forms.Textarea(
                attrs={
                    "rows": 2,
                    "placeholder": "石川県金沢市浅野本町2丁目15番3号",
                    "class": "form-control",
                }
            ),
            "address2": forms.Textarea(
                attrs={
                    "rows": 2,
                    "placeholder": "グリーンハイツ金沢 102号室",
                    "class": "form-control",
                }
            ),
            "country": forms.Select(attrs={"class": "form-select"}),
            "state": forms.Select(attrs={"class": "form-select"}),
            "zip_code": forms.TextInput(
                attrs={
                    "placeholder": "920-0981",
                    "class": "form-control",
                }
            ),
            "card_name": forms.TextInput(
                attrs={"placeholder": "SATO TARO", "class": "form-control"}
            ),
            "card_number": forms.TextInput(
                attrs={"placeholder": "1234567891011", "class": "form-control"}
            ),
            "expiration_date": forms.TextInput(
                attrs={"placeholder": "MM/YY", "class": "form-control"}
            ),
            "cvv": forms.TextInput(
                attrs={"placeholder": "1234", "class": "form-control"}
            ),
        }
