from django.utils import timezone
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .models import RoomPublic, User, Playlist, RoomPrivate, PlaylistSong, UserAction
from rest_framework import generics, status
from .serializer import RoomSerializer, CreateRoomSerializer
from rest_framework.views import APIView
from rest_framework.response import Response


# Create your views here.

class RoomView(generics.ListAPIView):
    queryset = RoomPrivate.objects.all()
    serializer_class = RoomSerializer
    
class CreateRoomView(APIView):
    serializer_class = CreateRoomSerializer
    def post(self, request, format=None):
        if not self.request.session.exists(self.request.session.session_key):
            self.request.session.create()
              
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            guest_can_pause = serializer.data.get('guest_can_pause')
            name = serializer.data.get('name')
            votes_to_skip = serializer.data.get('votes_to_skip')
            host = self.request.session.session_key
            is_public = serializer.data.get('is_public')
            queryset = RoomPrivate.objects.filter(host=host)
            if queryset.exists():
               room = queryset[0]
               room.name = name
               room.is_public = is_public
               room.guest_can_pause = guest_can_pause
               room.votes_to_skip = votes_to_skip
               room.created_time = timezone.now()
               room.save(update_fields=['votes_to_skip', 'guest_can_pause', 'created_time', 'is_public'])
               return Response(RoomSerializer(room).data, status=status.HTTP_200_OK)
            else:
                room = RoomPrivate(
                    host=host,
                    guest_can_pause=guest_can_pause,
                    votes_to_skip=votes_to_skip,
                    created_time= timezone.now(),
                    name =name,
                    # created_user=request.user
                    )
                room.save()
                    
            return Response(RoomSerializer(room).data, status=status.HTTP_200_OK)
        return Response({'Bad Request': 'Invalid data'}, status=status.HTTP_400_BAD_REQUEST)
            

def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "main/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "main/login.html")

def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))

def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "main/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "main/register.html")
    
# User Views
def login_view(request):
    if request.method == 'POST':
        # Handle Spotify authentication and user login
        ...
    else:
        return render(request, 'login.html')

def logout_view(request):
    logout(request)
    return redirect('index')

@login_required
def user_profile_view(request):
    user = request.user
    like_dislike_ratio = user.like_dislike_ratio
    return render(request, 'user_profile.html', {'user': user, 'like_dislike_ratio': like_dislike_ratio})

# Playlist View (Users Playlists)
@login_required
def playlist_view(request):
    user = request.user
    playlists = Playlist.objects.filter(user=user)
    return render(request, 'playlist_view.html', {'playlists': playlists})

# Room View
@login_required
def public_room_view(request, room_name):
    room = RoomPublic.objects.get(name=room_name)
    current_playlist = room.current_playlist
    playlist_1 = room.playlist_1
    playlist_2 = room.playlist_2

    # Check if user has already voted for a playlist in this room
    user_vote = RoomPublic.objects.filter(user=request.user, room=room).first()

    # Handle user vote for playlist
    if request.method == 'POST':
        playlist_id = request.POST.get('playlist_id')
        rank = request.POST.get('rank')  # 1 for first choice, 2 for second choice
        if playlist_id and rank:
            room_vote, _ = RoomPublic.objects.get_or_create(user=request.user, room=room, playlist_id=playlist_id, rank=rank)
            room_vote.save()

    # Determine the next playlist to play based on votes and daily performance
    if not current_playlist or not playlist_1 or not playlist_2 or request.method == 'POST':
        # Calculate daily like/dislike ratio for each playlist's songs
        today = timezone.now().date()
        playlist_performance = {}
        for playlist in Playlist.objects.all():
            total_likes = 0
            total_dislikes = 0
            for song in playlist.playlistsongs.all():
                actions = UserAction.objects.filter(song=song, action_type='like').filter(created_at__date=today)
                total_likes += actions.count()

                actions = UserAction.objects.filter(song=song, action_type='dislike').filter(created_at__date=today)
                total_dislikes += actions.count()

            if total_likes + total_dislikes > 0:
                like_dislike_ratio = total_likes / (total_likes + total_dislikes)
                playlist_performance[playlist.id] = like_dislike_ratio

        # Select the top two playlists based on daily performance
        top_playlists = sorted(playlist_performance.items(), key=lambda x: x[1], reverse=True)[:2]
        playlist_1_id, playlist_1_score = top_playlists[0]
        playlist_2_id, playlist_2_score = top_playlists[1]

        # Update the playlists in the room
        playlist_1 = Playlist.objects.get(id=playlist_1_id)
        playlist_2 = Playlist.objects.get(id=playlist_2_id)
        room.playlist_1 = playlist_1
        room.playlist_2 = playlist_2
        room.save()

    return render(request, 'room.html', {'room': room, 'current_playlist': current_playlist, 'playlist_1': playlist_1, 'playlist_2': playlist_2, 'user_vote': user_vote})
