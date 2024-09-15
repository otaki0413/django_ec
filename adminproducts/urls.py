from django.urls import path
from . import views


app_name = "adminproducts"
urlpatterns = [
    path("", views.AdminProductListView.as_view(), name="admin_product_list"),
]
