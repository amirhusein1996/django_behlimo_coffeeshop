from django.db.models import F, Sum
from django.http import Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
from django.urls import reverse_lazy
from django.views.generic import View, RedirectView, TemplateView
from ..base.cart import get_cart_id
from ..menu.models import Menu
from .models import Cart, CartItem
from ..tables.models import Table


class AddCartRedirectView(RedirectView):
    url = reverse_lazy('cart')

    def get(self, request, menu_id, *args, **kwargs):
        has_menu = Menu.objects.filter(menu_id=menu_id).exists()
        if not has_menu:
            raise Http404
        self.increment_quantity()
        return super().get(request, *args, **kwargs)

    def increment_quantity(self):
        cart_id = get_cart_id(self.request)
        menu_id = self.kwargs.get('menu_id')

        cart_item, created = CartItem.objects.get_or_create(
            menu_id=menu_id,
            cart=cart_id,
            defaults={'quantity': 1},
        )

        if not created:
            CartItem.objects.filter(
                menu_id=menu_id,
                cart=cart_id,
            ).update(quantity=F('quantity') + 1)


class RemoveCartRedirectView(RedirectView):
    url = reverse_lazy('cart')

    def get(self, request, menu_id, *args, **kwargs):
        has_menu = Menu.objects.filter(menu_id=menu_id).exists()
        if not has_menu:
            raise Http404
        self.decrement_quantity()
        return super().get(request, *args, **kwargs)

    def decrement_quantity(self):
        cart_id = get_cart_id(self.request)
        menu_id = self.kwargs.get('menu_id')

        is_updated = CartItem.objects.filter(
            menu_id=menu_id,
            cart_id=cart_id,
            quantity__gt=0  # Ensures the quantity is always greater than 0 (1 or more)
        ).update(
            quantity=F('quantity') - 1
        )

        if not is_updated:
            # It means the quantity of the object is 0
            CartItem.objects.filter(
                menu_id=menu_id,
                cart_id=cart_id,
                quantity__lte=0
            ).delete()


class RemoveCartItemRedirectView(RedirectView):
    url = reverse_lazy('cart')

    def get(self, request, menu_id, *args, **kwargs):
        has_menu = Menu.objects.filter(menu_id=menu_id).exists()
        if not has_menu:
            raise Http404
        self.remove_cart_item()
        return super().get(request, *args, **kwargs)

    def remove_cart_item(self):
        cart_id = get_cart_id(self.request)
        menu_id = self.kwargs.get('menu_id')
        CartItem.objects.filter(menu_id=menu_id, cart_id=cart_id).delete()


def cart(request, total=0, quantity=0, cart_items=None):
    try:
        cart = Cart.objects.get(cart_id=get_cart_id(request))
        cart_items = CartItem.objects.filter(cart=cart, is_active=True)
        for cart_item in cart_items:
            total += (cart_item.menu.price * cart_item.quantity)
            quantity += cart_item.quantity
    except ObjectDoesNotExist:
        pass

    context = {
        'total': total,
        'quantity': quantity,
        'cart_items': cart_items,

    }
    return render(request, 'cart.html', context=context)


class CheckOutView(TemplateView):
    template_name = 'checkout.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(self.get_tables())
        context.update(self.get_cart_context())
        return context

    def get_tables(self):
        tables = Table.objects.exclude(is_reserved=True)
        return {
            'tables': tables,
        }

    def get_cart_context(self):
        cart_id = get_cart_id(self.request)
        cart_items = CartItem.objects.filter(cart_id=cart_id, is_active=True)

        return {
            'total': self.get_total_price(cart_items),
            'quantity': self.get_quantity(cart_items),
            'cart_items': cart_items,
        }

    def get_total_price(self, cart_items):
        total_price = cart_items.annotate(
            item_price=F('menu__price') * F('quantity')
        ).aggregate(total_price=Sum('item_price'))['total_price'] or 0

        return total_price

    def get_quantity(self, cart_items):
        quantity = cart_items.aggregate(Sum('quantity'))['quantity__sum']
        return quantity
