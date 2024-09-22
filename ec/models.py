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
    public_id = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField("登録日時", auto_now_add=True)
    updated_at = models.DateTimeField("更新日時", auto_now=True)

    def __str__(self):
        return f"{self.product.name} Image"
