from django.contrib import admin
from django.urls import path 
from . import views

urlpatterns = [
path('', views.home , name='home'),
path('about/', views.about , name='about'),
path('universities/', views.universities_index, name='index'),
path('universities/<int:university_id>/', views.universities_detail, name='detail'),

# if need programs shown in another page not in uni
# path('universities/<int:university_id>/programs/', views.programs_index, name='program_index'),

path('universities/<int:university_id>/programs/<int:program_id>/', views.programs_detail, name='program_detail'),

path('universities/<int:university_id>/programs/<int:program_id>/toggle_favorite/', views.favorite_program, name='toggle_favorite_program'),

path('favorites/', views.favorites_list, name='favorites_list'),

#signup
path('accounts/signup/', views.signup, name='signup')
]