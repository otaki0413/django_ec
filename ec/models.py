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
    def total_price(self):
        """各カート商品の合計金額"""
        return self.product.price * self.quantity
