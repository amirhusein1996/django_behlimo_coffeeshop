from django.urls import path
from . import views


urlpatterns = [
    path('', views.AboutUsPage.as_view(), name='aboutus'),
    
]

