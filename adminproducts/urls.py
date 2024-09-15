from django.urls import path
from . import views


app_name = "adminproducts"
urlpatterns = [
    path("", views.index),
]
