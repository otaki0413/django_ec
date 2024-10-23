from django.views.generic import ListView, DetailView
from django.utils.decorators import method_decorator

from basicauth.decorators import basic_auth_required

from ec.models import Order


@method_decorator(basic_auth_required, name="dispatch")
class AdminOrderListView(ListView):
    model = Order
    template_name = "adminorders/index.html"
    context_object_name = "order_list"

    def get_queryset(self):
        # values()で使用するフィールドのみを抽出したdictを返す
        return Order.objects.values(
            "id", "first_name", "last_name", "user_name", "email", "created_at"
        )


@method_decorator(basic_auth_required, name="dispatch")
class AdminOrderDetailView(DetailView):
    model = Order
    template_name = "adminorders/detail.html"
    context_object_name = "order"

    def get_queryset(self):
        # template側で、Orderモデルのインスタンスに紐づくget_FOO_display()を使用したいので、values()は使用しない
        return Order.objects.select_related("promotion_code").prefetch_related(
            "details"
        )

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        # Orderインスタンス取得
        order = self.get_object()
        # プロモーションコードがあれば取得
        promotion_code = (
            order.promotion_code if hasattr(order, "promotion_code") else None
        )
        # 割引額を取得
        discount_amount = promotion_code.discount_amount if promotion_code else 0
        # 注文の合計金額を計算
        total_amount = max(0, order.total_amount - discount_amount)
        # 合計金額をコンテキストに追加
        context["total_amount"] = total_amount
        return context
