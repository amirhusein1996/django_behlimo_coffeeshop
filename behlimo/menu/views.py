from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, TemplateView, DetailView
from django.views.generic.edit import ModelFormMixin, FormMixin

from .models import Menu
from ..category.models import Category
from ..cart.models import CartItem
from ..cart.views import _get_cart_id
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.http import HttpResponse, Http404
from ..comments.forms import CommentModelForm
from ..comments.models import Comment


class MenuListView(ListView):
    model = Menu
    template_name = 'home.html'
    context_object_name = 'items'
    paginate_by = 3
    ordering = ['id']

    def get_queryset(self):
        category_slug = self.kwargs.get('category_slug')
        if category_slug:
            if Category.objects.filter(slug__iexact=category_slug).exists():
                return self.model.objects.filter(category_slug=category_slug).order_by(*self.ordering)
            raise Http404

        return super().get_queryset()

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['items_count'] = self.get_queryset().count()
        return context


class ItemDetailView(FormMixin, DetailView):
    model = Menu
    form_class = CommentModelForm
    success_url = reverse_lazy('messages')
    context_object_name = 'single_item'
    template_name = 'item_detail.html'

    def get_object(self, queryset=None):
        category_slug = self.kwargs.get('category_slug')
        item_slug = self.kwargs.get('item_slug')
        return get_object_or_404(
            klass=self.model,
            category__slug=category_slug,
            slug=item_slug
        )

    def form_valid(self, form):
        comment_obj = form.save(commit=False)
        comment_obj.menu = self.object
        comment_obj.save()
        self.request.session['current_url'] = self.request.get_full_path()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(self.get_comments())
        context.update(self.get_in_cart())
        return context

    def get_comments(self):
        comments = Comment.objects.filter(is_active=True, menu=self.object)
        comment_count = comments.count()
        return {
            'comments': comments,
            'comment_count': comment_count
        }

    def get_in_cart(self):
        cart_id = _get_cart_id(self.request)
        in_cart = CartItem.objects.filter(cart__cart_id=cart_id, menu=self.object).exists()
        return {
            'in_cart': in_cart,
        }


class SearchView(ListView):
    model = Menu
    template_name = 'home.html'
    context_object_name = 'items'
    ordering = ['id']

    def get_queryset(self):
        keyword = self.request.GET.get('keyword')
        if keyword:
            return self.model.objects.filter(title__contains=keyword)
        raise Http404

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            {
                'items_count': self.get_queryset().count()
            }
        )
        return context


class MessageView(TemplateView):
    template_name = "messages.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            {
                'url': self.get_url()
            }
        )
        return context

    def get_url(self):
        url = self.request.session.get('current_url')
        if not url:
            raise Http404
        self.request.session['current_url'] = None
        return url
