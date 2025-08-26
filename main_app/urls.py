from django.contrib import admin
from django.urls import path 
from . import views

urlpatterns = [
path('', views.home , name='home'),
path('about/', views.about , name='about'),
path('universities/', views.cats_index, name='index'),

#signup
path('accounts/signup', views.signup, name='signup')
]