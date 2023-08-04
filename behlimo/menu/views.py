from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, TemplateView
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

    def get_queryset(self):
        category_slug = self.kwargs.get('category_slug')
        if category_slug:
            if Category.objects.filter(slug__iexact=category_slug).exists():
                return self.model.objects.filter(category_slug=category_slug)
            raise Http404

        return self.model.objects.all()

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['items_count'] = self.get_queryset().count()
        return context


def item_detail(request, category_slug, item_slug):
    try:
        single_item = Menu.objects.get(category__slug=category_slug, slug=item_slug)
        in_cart = CartItem.objects.filter(cart__cart_id=_get_cart_id(request), menu=single_item).exists()

    except Exception as e:
        raise e

    form_class = CommentModelForm
    comments = Comment.objects.filter(is_active=True, menu=single_item)
    comment_count = comments.count()
    if request.method == "POST":
        form = form_class(data=request.POST)
        if form.is_valid():
            comment_obj = form.save(commit=False)
            comment_obj.menu = single_item

            comment_obj.save()
            request.session['current_url'] = request.get_full_path()
            return redirect('messages')

    context = {
        'single_item': single_item,
        'in_cart': in_cart,
        'comments': comments,
        'comment_count': comment_count

    }

    return render(request, 'item_detail.html', context=context)


def search(request):
    if 'keyword' in request.GET:
        keyword = request.GET['keyword']
        if keyword:
            items = Menu.objects.order_by('id').filter(titel__icontains=keyword)
            items_count = items.count()
            context = {
                'items': items,
                'items_count': items_count,

            }
    return render(request, 'home.html', context or {})


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
