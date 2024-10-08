from django.core.validators import RegexValidator, MinValueValidator
from django.db import models


class Product(models.Model):
    class Meta:
        db_table = "product"

    name = models.CharField("商品名", max_length=50, null=False)
    description = models.TextField("説明", blank=True, null=False)
    price = models.IntegerField("値段", null=False, default=0)
    created_at = models.DateTimeField("登録日時", auto_now_add=True)
    updated_at = models.DateTimeField("更新日時", auto_now=True)

    def __str__(self):
        return self.name


class ProductImage(models.Model):
    class Meta:
        db_table = "product_image"

    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="images"
    )
    image = models.ImageField(upload_to="images/", blank=True)
    created_at = models.DateTimeField("登録日時", auto_now_add=True)
    updated_at = models.DateTimeField("更新日時", auto_now=True)

    def __str__(self):
        return f"{self.product.name} Image"


class Cart(models.Model):
    class Meta:
        db_table = "cart"

    session_key = models.CharField(
        "セッションキー", max_length=40, null=False, unique=True
    )
    created_at = models.DateTimeField("登録日時", auto_now_add=True)
    updated_at = models.DateTimeField("更新日時", auto_now=True)

    def __str__(self):
        return f"Cart {self.session_key} (Created: {self.created_at.strftime('%Y-%m-%d %H:%M:%S')})"

    @property
    def total_amount(self):
        """カート内の合計金額"""
        total_amount = 0
        for product in self.products.all():
            # 各カート商品の小計を加算
            total_amount += product.sub_total
        return total_amount


class CartProduct(models.Model):
    class Meta:
        db_table = "cart_product"

    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="products")
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="cart_products"
    )
    quantity = models.IntegerField("数量", null=False, default=1)
    created_at = models.DateTimeField("登録日時", auto_now_add=True)
    updated_at = models.DateTimeField("更新日時", auto_now=True)

    def __str__(self):
        return f"{self.product.name} (Quantity: {self.quantity}) in Cart {self.cart.session_key}"

    @property
    def sub_total(self):
        """各カート商品の小計"""
        return self.product.price * self.quantity


class Order(models.Model):
    COUNTRY_CHOICES = [("", "Choose..."), ("US", "United States")]

    STATE_CHOICES = [
        ("", "Choose..."),
        ("CA", "California"),
        ("TX", "Texas"),
        ("FL", "Florida"),
        ("NY", "New York"),
    ]

    # カード番号のバリデーター
    CARD_NUMBER_VALIDATOR = RegexValidator(
        regex=r"^(?:\d{13}|\d{15}|\d{16})$",  # 13桁、15桁、または16桁の数字
        message="カード番号は13桁、15桁、または16桁の数字である必要があります。",
    )

    # カード有効期限のバリデータ
    EXPIRATION_DATE_VALIDATOR = RegexValidator(
        regex=r"^(0[1-9]|1[0-2])\/?([0-9]{2})$",  # MM/YY形式
        message="カード有効期限はMM/YY形式である必要があります。",
    )

    # CVV(セキュリティコード)のバリデータ
    CVV_VALIDATOR = RegexValidator(
        regex=r"^\d{3,4}$",  # 3桁または4桁の数字
        message="CVVは3桁または4桁の数字である必要があります。",
    )

    class Meta:
        db_table = "order"

    first_name = models.CharField("名前", max_length=20, null=False)
    last_name = models.CharField("名字", max_length=20, null=False)
    user_name = models.CharField("ユーザー名", max_length=40, null=False)
    email = models.EmailField("メールアドレス", blank=True, null=False)
    address1 = models.TextField("住所1", null=False)
    address2 = models.TextField("住所2", blank=True, null=False)
    country = models.CharField("国", max_length=20, null=False, choices=COUNTRY_CHOICES)
    state = models.CharField("州", max_length=20, null=False, choices=STATE_CHOICES)
    zip_code = models.CharField("郵便番号", max_length=20, null=False)
    card_name = models.CharField("カード名義", max_length=50, null=False)
    card_number = models.CharField(
        "カード番号", max_length=16, null=False, validators=[CARD_NUMBER_VALIDATOR]
    )
    expiration_date = models.CharField(
        "カード有効期限",
        max_length=5,
        null=False,
        validators=[EXPIRATION_DATE_VALIDATOR],
    )
    cvv = models.CharField(
        "セキュリティコード", max_length=4, null=False, validators=[CVV_VALIDATOR]
    )
    created_at = models.DateTimeField("登録日時", auto_now_add=True)
    updated_at = models.DateTimeField("更新日時", auto_now=True)

    def __str__(self):
        return f"Order {self.id} by {self.last_name} {self.first_name} ({self.created_at.strftime('%Y-%m-%d')})"


class OrderDetail(models.Model):
    class Meta:
        db_table = "order_detail"

    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="details")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(
        "数量", null=False, default=1, validators=[MinValueValidator(1)]
    )
    price = models.IntegerField("購入時の値段", null=False)
    created_at = models.DateTimeField("登録日時", auto_now_add=True)
    updated_at = models.DateTimeField("更新日時", auto_now=True)

    def __str__(self):
        return f"{self.product.name} ({self.quantity}個) of Order {self.order.id}"
