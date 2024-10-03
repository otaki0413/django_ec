from django.contrib import admin

from .models import Product, ProductImage, Cart, CartProduct, Order, OrderDetail


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    model = Product
    list_display = ["name", "price", "created_at", "updated_at"]
    readonly_fields = ("created_at", "updated_at")


@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    model = ProductImage
    readonly_fields = ("created_at", "updated_at")


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    model = Cart
    readonly_fields = ("session_key", "created_at", "updated_at")


@admin.register(CartProduct)
class CartProductAdmin(admin.ModelAdmin):
    model = CartProduct
    readonly_fields = ("created_at", "updated_at")


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    model = Order
    readonly_fields = ("created_at", "updated_at")


@admin.register(OrderDetail)
class OrderDetailAdmin(admin.ModelAdmin):
    model = OrderDetail
    readonly_fields = ("created_at", "updated_at")
