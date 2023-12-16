from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('join/', views.index, name='join'),
    path('profile/', views.index, name='profile'),
    path('room/<str:roomCode>', views.index, name='room'),
    path('login/', views.index, name='login'),
    path('create/', views.index, name='create'),
    path('join/', views.index, name='join'),
    
]