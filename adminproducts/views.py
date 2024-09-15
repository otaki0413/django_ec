from django.views import generic

from ec.models import Product


class AdminProductListView(generic.ListView):
    model = Product
    template_name = "adminproducts/index.html"
    context_object_name = "product_list"

    def get_queryset(self):
        return Product.objects.prefetch_related("images")
