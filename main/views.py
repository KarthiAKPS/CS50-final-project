from django.utils import timezone
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .models import RoomPublic, User, Playlist, RoomPrivate, PlaylistSong, UserAction
from rest_framework import generics, status
from .serializer import RoomSerializer, CreateRoomSerializer, EditRoomSerializer
from rest_framework.views import APIView
from rest_framework.response import Response

# Create your views here.

class RoomView(generics.ListAPIView):
    queryset = RoomPrivate.objects.all()
    serializer_class = RoomSerializer


class GetRoom(APIView):
    serializer_class = RoomSerializer
    lookup_url_kwarg = 'code'
    def get(self, request, format=None, *args, **kwargs):
        code = request.GET.get(self.lookup_url_kwarg)
        if code != None:
            room = RoomPrivate.objects.filter(code=code)
            if len(room)!=0:
                room = room[0]
                serializer = self.serializer_class(room)
                created_user = serializer.data.get('created_user')
                if created_user == request.user:
                    serializer.data['is_creator'] = True
                else:
                    serializer.data['is_creator'] = False
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response({'Bad Request': 'Invalid code'}, status=status.HTTP_404_NOT_FOUND)
        return Response({'Bad Request': 'Code parameter not found in request'}, status=status.HTTP_400_BAD_REQUEST)    
            
        
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
               self.request.session['code'] = room.code
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
                self.request.session['code'] = room.code
                room.save()
                    
            return Response(RoomSerializer(room).data, status=status.HTTP_200_OK)
        return Response({'Bad Request': 'Invalid data'}, status=status.HTTP_400_BAD_REQUEST)


class InRoom(APIView):
    def get(self, request, format=None, *args, **kwargs):
        if not self.request.session.exists(self.request.session.session_key):
            self.request.session.create()
        if self.request.session.get('code'):
            data = {
                'code': self.request.session.get('code')
            }
            return JsonResponse(data, status=status.HTTP_200_OK)
        else:
            return Response({'message':'Room Not Found'}, status=status.HTTP_200_OK)
            
class JoinRoom(APIView):
    lookup_url_kwarg = 'code'
    def post(self, request, format=None, *args, **kwargs):
        if not self.request.session.exists(self.request.session.session_key):
            self.request.session.create()
        code = request.data.get(self.lookup_url_kwarg)
        if code != None:
            room = RoomPrivate.objects.filter(code=code)
            if len(room)!=0:
                room = room[0]
                self.request.session['code'] = code
                return Response({'message':'Room Joined!'}, status=status.HTTP_200_OK)
            else:
                return Response({'Bad Request': 'No Room Found'}, status=status.HTTP_404_NOT_FOUND)
        if code:
            print(code)
        else:
            print('------------------No code---------------------')
        return Response({'Bad Request': 'Code parameter not found in request'}, status=status.HTTP_400_BAD_REQUEST)
    

class LeaveRoom(APIView):
    def post(self, request, format=None, *args, **kwargs):
        user = request.user
        room_code = request.data.get('code')
        print(user)
        if 'code' in self.request.session:
            self.request.session.pop('code')
            host_id = self.request.session.session_key
            room = RoomPrivate.objects.filter(host=host_id)
            if len(room)!=0:
                room = room[0]
                room.delete()
            return Response({'message':'Success'}, status=status.HTTP_200_OK)
        room = RoomPrivate.objects.filter(created_user=user, code=room_code)
        if room.exists():
            room = room[0]
            room.delete()
            return Response({'message': 'Success'}, status=status.HTTP_200_OK)
        return Response({'Bad Request': 'Error'}, status=status.HTTP_400_BAD_REQUEST)


class EditRoom(APIView):
    serializer_class = EditRoomSerializer
    def patch(self, request, format=None, *args, **kwargs):
        print(request.data)
        if(request.data):
            serializer = self.serializer_class(data = request.data)
        else:
            return Response({"detail": "No data provided"}, status=400)
        user = request.user
        if serializer.is_valid():
            name = serializer.data.get('name')
            guest_can_pause = serializer.data.get('guest_can_pause')
            votes_to_skip = serializer.data.get('votes_to_skip')
            is_public = serializer.data.get('is_public')
            code = serializer.data.get('code')
            room = RoomPrivate.objects.filter(code = code) # if room already exists
            if room.exists():
                room = room[0]
                #if user != serializer.data.get('created_user'):
                    #return Response({'message': 'Not the host'}, status=status.HTTP_403_FORBIDDEN)
                room.name = name
                room.guest_can_pause = guest_can_pause
                room.votes_to_skip = votes_to_skip
                room.is_public = is_public
                room.save(update_fields=['name', 'guest_can_pause', 'votes_to_skip', 'is_public'])
                self.request.session['code'] = room.code
                return Response(RoomSerializer(room).data, status=status.HTTP_200_OK)
            return Response({'message': 'Room not found'}, status=status.HTTP_404_NOT_FOUND)
        return Response({'Bad Request.. serializer not valid': 'Error'}, status=status.HTTP_400_BAD_REQUEST)
    


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
