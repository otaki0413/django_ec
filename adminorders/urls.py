from django.urls import path
from . import views


app_name = "adminorders"
urlpatterns = [
    path("", views.AdminOrderListView.as_view(), name="admin_order_list"),
    path(
        "<int:pk>/",
        views.AdminOrderDetailView.as_view(),
        name="admin_order_detail",
    ),
]
