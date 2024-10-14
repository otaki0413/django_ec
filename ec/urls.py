from django.urls import path
from django.views.generic import RedirectView

from . import views

app_name = "ec"
urlpatterns = [
    path(
        "",
        RedirectView.as_view(pattern_name="ec:product_list"),
        name="redirect_to_product_list",
    ),
    path("products/", views.ProductListView.as_view(), name="product_list"),
    path(
        "products/<int:pk>/", views.ProductDetailView.as_view(), name="product_detail"
    ),
    path("checkout/", views.CheckoutView.as_view(), name="checkout"),
    path("add_to_cart/", views.AddToCartView.as_view(), name="add_to_cart"),
    path(
        "delete_from_cart/", views.DeleteFromCartView.as_view(), name="delete_from_cart"
    ),
]
