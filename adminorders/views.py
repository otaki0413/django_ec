from django.views.generic import ListView, DetailView
from ec.models import Order


class AdminOrderListView(ListView):
    model = Order
    template_name = "adminorders/index.html"
    context_object_name = "order_list"

    def get_queryset(self):
        # values()で使用するフィールドのみを抽出したdictを返す
        return Order.objects.values(
            "id", "first_name", "last_name", "user_name", "email", "created_at"
        )


class AdminOrderDetailView(DetailView):
    model = Order
    template_name = "adminorders/detail.html"
    context_object_name = "order"

    def get_queryset(self):
        # template側で、Orderモデルのインスタンスに紐づくget_FOO_display()を使用したいので、values()は使用しない
        return Order.objects.prefetch_related("details")
