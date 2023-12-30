from django.urls import path

from . import views

app_name = 'frontend'

urlpatterns = [
    path('', views.index, name='index'),
    path('join/', views.index, name='join'),
    path('profile/', views.index, name='profile'),
    path('room/<str:roomCode>', views.index, name='room'),
    path('create/', views.index, name='create'),
]