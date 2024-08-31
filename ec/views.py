from django.db.models.query import QuerySet
from django.shortcuts import render
from django.http import HttpResponse
from django.views import generic

from .models import Product, ProductImage


class ProductListView(generic.ListView):
    model = Product
    template_name = "ec/list.html"


class ProductDetailView(generic.DetailView):
    model = Product
    template_name = "ec/detail.html"
