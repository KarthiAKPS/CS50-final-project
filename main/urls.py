from django.urls import path

from . import views

urlpatterns = [
    path("/room", views.RoomView.as_view(), name="room"),
    path("/create-room", views.CreateRoomView.as_view(), name="create-room"),
    path("/get-room", views.GetRoom.as_view(), name="get-room"),
    path("/join-room", views.JoinRoom.as_view(), name="join-room"),
    path("/in-room", views.InRoom.as_view(), name="in-room"),
    path("/leave-room", views.LeaveRoom.as_view(), name="leave-room"),
    path("/edit-room", views.EditRoom.as_view(), name="edit-room"),
]