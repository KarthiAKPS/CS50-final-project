from django.urls import path

from . import views

urlpatterns = [
    path("/room", views.RoomView.as_view(), name="room"),
    path("/create-room", views.CreateRoomView.as_view(), name="create-room"),
]