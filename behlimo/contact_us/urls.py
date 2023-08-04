from django.urls import path
from . import views


urlpatterns = [
    path('', views.ContactUsPage.as_view(), name='contactus'),
    
]

