from django.contrib import admin
from django.urls import path 
from . import views

urlpatterns = [
path('', views.home , name='home'),
path('about/', views.about , name='about'),
path('edit_user/', views.edit_user, name='edit_user'),
path('universities/', views.universities_index, name='index'),
path('universities/<int:university_id>/', views.universities_detail, name='detail'),

# if need programs shown in another page not in uni
# path('universities/<int:university_id>/programs/', views.programs_index, name='program_index'),

path('universities/<int:university_id>/programs/<int:program_id>/', views.programs_detail, name='program_detail'),

#Q&A
path('question/<int:pk>/delete/', views.question_delete, name='question_delete'),
path('answer/<int:pk>/delete/', views.answer_delete, name='answer_delete'),


path('universities/<int:university_id>/programs/<int:program_id>/toggle_favorite/', views.favorite_program, name='toggle_favorite_program'),


path('favorites/', views.favorites_list, name='favorites_list'),


#signup
path('accounts/signup/', views.signup, name='signup')
]