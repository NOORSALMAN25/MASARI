from django.contrib import admin
from django.urls import path 
from . import views

urlpatterns = [
path('', views.home , name='home'),
path('about/', views.about , name='about'),
path('universities/', views.universities_index, name='index'),
path('universities/<int:university_id>/', views.universities_detail, name='detail'),

#signup
path('accounts/signup/', views.signup, name='signup')
]