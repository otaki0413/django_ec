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
]
