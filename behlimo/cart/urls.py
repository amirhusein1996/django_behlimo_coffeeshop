from django.urls import path
from . import views


urlpatterns = [
    path('', views.cart, name='cart'),
    path('add_cart/<int:menu_id>/',views.AddCartRedirectView.as_view(), name='add_cart'),
    path('remove_cart/<int:menu_id>/',views.RemoveCartItemRedirectView.as_view(), name='remove_cart'),
    path('remove_cart_item/<int:menu_id>/',views.RemoveCartItemRedirectView.as_view(), name='remove_cart_item'),
    path('checkout/', views.CheckOutView.as_view(), name='checkout')
   
]

