from django.urls import path

from . import views

app_name = "ec"
urlpatterns = [
    path("products/", views.ProductListView.as_view(), name="product_list"),
    path("products/<int:pk>", views.ProductDetailView.as_view(), name="product_detail"),
]
