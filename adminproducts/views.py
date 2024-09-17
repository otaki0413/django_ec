from django.views import generic
from .forms import ProductRegisterForm, ProductImageRegisterForm
from ec.models import Product, ProductImage
from django.urls import reverse_lazy


class AdminProductListView(generic.ListView):
    model = Product
    template_name = "adminproducts/index.html"
    context_object_name = "product_list"

    def get_queryset(self):
        return Product.objects.prefetch_related("images")


class AdminProductRegisterView(generic.CreateView):
    model = Product
    form_class = ProductRegisterForm
    second_form_class = ProductImageRegisterForm
    template_name = "adminproducts/new.html"
    success_url = reverse_lazy("adminproducts:admin_product_list")

    def get_context_data(self, **kwargs):
        context = super(AdminProductRegisterView, self).get_context_data(**kwargs)
        if "image_form" not in context:
            context["image_form"] = self.second_form_class()
        return context
