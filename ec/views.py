from django.shortcuts import render
from django.http import HttpResponse
from django.views import generic

from .models import Product, ProductImage


class ProductListView(generic.ListView):
    model = Product
    template_name = "ec/index.html"


class ProductDetailView(generic.DetailView):
    model = Product
    template_name = "ec/detail.html"

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["related_product_list"] = Product.objects.filter().order_by(
            "-created_at"
        )[:4]
        return context
