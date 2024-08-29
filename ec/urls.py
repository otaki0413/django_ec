from django.urls import path

from . import views

app_name = "ec"
urlpatterns = [
    path("products/", views.IndexView.as_view(), name="index"),
    path("products/<int:pk>", views.DetailView.as_view(), name="detail"),
]
