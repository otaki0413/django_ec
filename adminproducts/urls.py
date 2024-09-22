from django.urls import path
from . import views


app_name = "adminproducts"
urlpatterns = [
    path("", views.AdminProductListView.as_view(), name="admin_product_list"),
    path(
        "new/", views.AdminProductRegisterView.as_view(), name="admin_product_register"
    ),
    path(
        "edit/<int:pk>/",
        views.AdminProductEditView.as_view(),
        name="admin_product_edit",
    ),
]
