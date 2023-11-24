from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('join', views.index, name='index'),
    path('profile', views.index, name='index'),
    path('room', views.index, name='index'),
    path('login', views.index, name='index'),
]