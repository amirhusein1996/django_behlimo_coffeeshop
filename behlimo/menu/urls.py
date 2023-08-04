from django.urls import path
from . import views


urlpatterns = [
    path('', views.MenuListView, name='menu'),
    path('search/',views.SearchView.as_view(), name='search'),
    path('<slug:category_slug>/', views.MenuListView.as_view(), name='menu_by_category'),
    path('<slug:category_slug>/<slug:item_slug>/', views.ItemDetailView.as_view(), name='item_detail'),
    path('messages', views.MessageView.as_view(), name='messages'),
    


]

