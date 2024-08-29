from django.db.models.query import QuerySet
from django.shortcuts import render
from django.http import HttpResponse
from django.views import generic

from .models import Product, ProductImage


class IndexView(generic.ListView):
    template_name = "ec/list.html"
    context_object_name = "product_list"

    def get_queryset(self):
        return Product.objects


class DetailView(generic.DetailView):
    model = Product
    template_name = "ec/detail.html"
