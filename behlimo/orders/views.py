import zoneinfo
from django.db.models import Sum, F
from django.shortcuts import render, redirect
from django.utils import timezone
from django.views import View
from ..base.cart import get_cart_id
from ..cart.models import CartItem
from .models import Order, OrderItem
from .forms import OrderForm


class PlaceOrderView(View):
    model = CartItem

    def dispatch(self, request, *args, **kwargs):
        cart_count = self.get_queryset().count()
        if cart_count <= 0:
            return redirect('menu')
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        cart_id = get_cart_id(self.request)
        return self.model.objects.filter(
            cart__cart_id=cart_id,
            is_active=True
        )

    def get(self, request):
        form = OrderForm()
        error_message = 'این صفحه فقط برای درخواست‌های POST قابل دسترسی است.'
        return render(request, 'checkout.html', {'error_message': error_message, 'form': form})

    def post(self, request):
        form = OrderForm(request.POST)
        if form.is_valid():
            return self.form_valid(form)
        return self.form_invalid(form)

    def form_valid(self, form):
        cart_items = self.get_queryset()
        total = cart_items.annotate(
            item_price=F('menu__price') * F('quantity')
        ).aggregate(total_price=Sum('item_price'))['total_price'] or 0

        table = form.cleaned_data.get('table')
        customer_name = form.cleaned_data['customer_name']

        tehran_tz = zoneinfo.ZoneInfo('Asia/Tehran')
        current_date = timezone.localdate(timezone=tehran_tz).strftime("%Y%m%d")

        latest_id = self.model.objects.only('id').order_by('-id').first()
        next_id = latest_id.id if latest_id else 1

        data = Order.objects.create(
            customer_name=customer_name,
            is_paid=True,
            table=table,
            order_total=total,
            customer_number=current_date + next_id

        )
        table.is_reserved = True
        table.save()

        # ذخیره آیتم های سفارش جدید
        OrderItem.objects.bulk_create(
            [
                OrderItem(
                    order=data,
                    menu=cart_item.menu,
                    quantity=cart_item.quantity
                ) for cart_item in cart_items
            ]
        )

        self.get_queryset().delete()
        return redirect('checkout')

    def form_invalid(self, form):
        error_message = 'فرم نامعتبر است. لطفاً اطلاعات را به درستی وارد کنید.'
        return render(self.request, 'checkout.html', {'error_message': error_message, 'form': form})
