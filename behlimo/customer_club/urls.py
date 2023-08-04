from django.urls import path
from . import views


urlpatterns = [
    path('', views.RegisterCustomerView.as_view(), name='register_customer'),
]

