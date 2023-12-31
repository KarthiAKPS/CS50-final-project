from django.shortcuts import render, redirect
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from main.models import RoomPrivate, User, RoomCode
from .models import SpotifyToken
from .auth_backends import UsernameBackend
from django.utils import timezone
from datetime import timedelta, datetime
from requests import post, put, get, Request
from django.contrib.auth import authenticate, login
import os
from django.http import HttpResponse
from .models import Vote
import json

BASE_URL = "https://api.spotify.com/v1/"

REDIRECT_URI = os.environ.get('REDIRECT_URI')
CLIENT_SECRET = os.environ.get('CLIENT_SECRET')
CLIENT_ID = os.environ.get('CLIENT_ID')

def get_user_tokens(session_id):
    tokens = SpotifyToken.objects.filter(user=session_id)
    if tokens.exists():
        return tokens[0]
    else:
        return None

def update_or_create_user_tokens(session_id, access_token, token_type, expires_in, refresh_token):
    expires_in = datetime.now() + timedelta(seconds=expires_in)
    tokens, created = SpotifyToken.objects.get_or_create(user=session_id,
                                                         defaults={'access_token': access_token,
                                                                   'refresh_token': refresh_token,
                                                                   'token_type': token_type,
                                                                   'expires_in': expires_in})

    if not created and (tokens.access_token != access_token or
                        tokens.refresh_token != refresh_token or
                        tokens.token_type != token_type or
                        tokens.expires_in != expires_in):
        tokens.access_token = access_token
        tokens.refresh_token = refresh_token
        tokens.token_type = token_type
        tokens.expires_in = expires_in
        tokens.save(update_fields=['access_token', 'refresh_token', 'expires_in', 'token_type'])


    return HttpResponse('Access token set')

def is_spotify_authenticated(session_id):
    tokens = get_user_tokens(session_id)
    if tokens:
        expiry = tokens.expires_in
        if expiry <= timezone.now():
            refresh_spotify_token(session_id)
        return True
    return False

def refresh_spotify_token(session_id):
    refresh_token = get_user_tokens(session_id).refresh_token

    response = post('https://accounts.spotify.com/api/token', data={
        'grant_type': 'refresh_token',
        'refresh_token': refresh_token,
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET
    }).json()

    access_token = response.get('access_token')
    token_type = response.get('token_type')
    expires_in = response.get('expires_in')
    new_refresh_token = response.get('refresh_token')
    
    if not new_refresh_token :
        # If a new refresh token is returned, update the stored refresh token
        new_refresh_token = refresh_token
    
    update_or_create_user_tokens(
        session_id=session_id, access_token=access_token, token_type=token_type, expires_in=expires_in, refresh_token=new_refresh_token)
    

def spotify_api_requests(session_id, endpoint,  data={}, put_request=False, post_request=False):
    tokens = get_user_tokens(session_id)
    if tokens is None:
        return None
    headers = {'Content-Type': 'application/json',
               'Authorization': "Bearer " + tokens.access_token}

    response_get = None
    response_post = None
    response_put = None
    if put_request:
        response_put = put(BASE_URL + endpoint, headers=headers, data=data)
        print(response_put)
        try:
            print(response_put.json())
            return response_put
        except Exception as e:
            print("Error:", e)
            return None
    elif post_request:
        response_post = post(BASE_URL + endpoint, headers=headers)
        print(response_post)
        try:
            return response_post
        except Exception as e:
            print("Error:", e)
            return None
    else:
        response_get = get(BASE_URL + endpoint, {}, headers=headers)
        try:
            return response_get.json()
        except Exception as e:
            print("Error:", e)
            return None

class AuthURL(APIView):
    def get(self, request, format=None):
        if not request.session.exists(request.session.session_key):
            request.session.create()
    
        c = request.session.get('u_code')
        if c is None:
            self.request.session['u_code'] = RoomCode()                                                                       
            code = self.request.session.get('u_code')
            user = User(username = code, code = code)
            user.save()
        scope = 'user-read-playback-state user-modify-playback-state user-read-currently-playing playlist-read-private'
        state = self.request.session.get('u_code')
        self.request.session['state'] = state

        url = Request('GET', 'https://accounts.spotify.com/authorize', params={
            'scope': scope,
            'response_type': 'code',
            'redirect_uri': REDIRECT_URI,
            'client_id': CLIENT_ID,
            'state': state
        }).prepare().url

        return Response({'url': url}, status=status.HTTP_200_OK)


def spotify_callback(request, format=None):
    code = request.GET.get('code')
    error = request.GET.get('error')

    response = post('https://accounts.spotify.com/api/token', data={
        'grant_type': 'authorization_code',
        'code': code,
        'redirect_uri': REDIRECT_URI,
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
    }).json()

    print(response) 

    access_token = response.get('access_token')
    token_type = response.get('token_type')
    refresh_token = response.get('refresh_token')
    expires_in = response.get('expires_in')
    error = response.get('error')
    callback_state = request.GET.get('state')
    
    session_state = request.session.get('state')
    
    if not request.session.exists(request.session.session_key):
        request.session.create()
    
    if callback_state != session_state:
        # The state parameters do not match, handle the error
        request.session['state'] = callback_state
        
    update_or_create_user_tokens( 
        request.session.session_key,  access_token=access_token, token_type=token_type, expires_in=expires_in, refresh_token=refresh_token)

    return redirect('frontend:index')


class IsAuthenticated(APIView):
    def get(self,request, format=None):
        is_authenticated = is_spotify_authenticated(
            self.request.session.session_key)
        return Response({'status': is_authenticated}, status=status.HTTP_200_OK)
    
class CurrentSong(APIView):
    def get(self, request, format=None):
        if not self.request.session.exists(self.request.session.session_key):
            self.request.session.create()
        room_code = self.request.session.get('state')
        rooms = RoomPrivate.objects.filter(code=room_code)
        if rooms.exists():
            room = rooms[0]
            host = room.host
            endpoint = "me/player/currently-playing"
            v_t_s = room.votes_to_skip
            response = spotify_api_requests(host, endpoint)
            
        else:
            host = self.request.session.session_key
            endpoint = "me/player/currently-playing"
            votes = 1
            v_t_s = 1
            response = spotify_api_requests(host, endpoint)
        
        if 'error' in response or 'item' not in response:
            return Response({}, status=status.HTTP_204_NO_CONTENT)
        
        
        item = response.get('item')
        duration = item.get('duration_ms')
        progress = response.get('progress_ms')
        album_cover = item.get('album').get('images')[0].get('url')
        is_playing = response.get('is_playing')
        song_id = item.get('id')
        
        if rooms.exists():
            votes = len(Vote.objects.filter(room=room, song_id=song_id))
            

        artist_string = ""

        for i, artist in enumerate(item.get('artists')):
            if i > 0:
                artist_string += ", "
            name = artist.get('name')
            artist_string += name

        song = {
            'title': item.get('name'),
            'artist': artist_string,
            'duration': duration,
            'time': progress,
            'image_url': album_cover,
            'is_playing': is_playing,
            'id': song_id,
            'votes': votes,
            'votes_required': v_t_s,
        }
        
        if rooms.exists():
            self.update_room_song(room, song_id)
        
        return Response(song, content_type='application/json', status=status.HTTP_200_OK)
        
    def update_room_song(self, room, song_id):
        current_song = room.current_song_id

        if current_song != song_id:
            room.current_song_id = song_id
            room.save(update_fields=['current_song_id'])
            Vote.objects.filter(room=room).delete()


class UserProfile(APIView):
    def get(self, *args, **kwargs):
        if not self.request.session.exists(self.request.session.session_key):
            self.request.session.create()
        endpoint = "me"
        session_key = self.request.session.session_key
        response = spotify_api_requests(session_key, endpoint)
        needed_response = {
            'display_name': response.get('display_name'),
            'followers': response.get('followers').get('total'),
            'id': response.get('id'),
            'image': response.get('images')[0].get('url')}
        print(needed_response)
        return Response(needed_response, content_type='application/json', status=status.HTTP_200_OK)


class Playlist(APIView):
    def get(self, *args, **kwargs):
        if not self.request.session.exists(self.request.session.session_key):
            self.request.session.create()
        endpoint = "me/playlists"
        session_key = self.request.session.session_key
        response = spotify_api_requests(session_key, endpoint)
        return Response(response, content_type='application/json', status=status.HTTP_200_OK)
    

class PauseSong(APIView):
    def put(self, response, format=None):
        room_code = self.request.session.get('state')
        room = RoomPrivate.objects.filter(code=room_code)
        if room.exists():
            room = room[0]
            if self.request.session.session_key == room.host or room.guest_can_pause:
                pause_song(room.host)
            else:
                return Response({}, status=status.HTTP_204_NO_CONTENT)
        else:
            pause_song(self.request.session.session_key)
        return Response({}, status=status.HTTP_200_OK)
    
class PlaySong(APIView):
    def put(self, response, format=None):
        room_code = self.request.session.get('state')
        room = RoomPrivate.objects.filter(code=room_code)
        if room.exists():
            room = room[0]
            if self.request.session.session_key == room.host or room.guest_can_pause:
                play_song(room.host)
            else:
                return Response({}, status=status.HTTP_204_NO_CONTENT)
        else:
            play_song(self.request.session.session_key) 
        return Response({}, status=status.HTTP_200_OK)
    
    
class SkipSong(APIView):
    def post(self, request, format=None):
        room_code = self.request.session.get('state')
        rooms = RoomPrivate.objects.filter(code=room_code)
        if rooms.exists():
            room = rooms[0]
            votes = Vote.objects.filter(room=room, song_id=room.current_song_id)
            votes_needed = room.votes_to_skip
            if self.request.session.session_key == room.host or len(votes) + 1 >= votes_needed:
                votes.delete()
                skip_song(room.host)
            else:
                if room.current_song_id is not None:
                    vote = Vote(user=self.request.session.session_key, room=room, song_id=room.current_song_id)
                    vote.save()
                    return Response({}, status=status.HTTP_200_OK)
                else:
                    # Handle the case where current_song_id is null
                    # For example, you could return an error response
                    return Response({'message': 'Current song ID is null'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            votes = 1
            votes_needed = 1
            skip_song(self.request.session.session_key)

        return Response({}, status.HTTP_204_NO_CONTENT)


def play_song(session_id):
    return spotify_api_requests(session_id, "me/player/play", put_request=True)


def pause_song(session_id):
    return spotify_api_requests(session_id, "me/player/pause", put_request=True)


def skip_song(session_id):
    return spotify_api_requests(session_id, "me/player/next", post_request=True)


def play_playlist(session_id, playlist_id):
    endpoint = "me/player/play"
    data = {
        "context_uri": f"spotify:playlist:{playlist_id}"
    }
    response = spotify_api_requests(session_id, endpoint, data=json.dumps(data), put_request=True)

    return response


class PlayPlaylist(APIView):
    def post(self, request, playlist_id, format=None):
        if not self.request.session.exists(self.request.session.session_key):
            self.request.session.create()
            
        room_code = self.request.session.get('state')
        room = RoomPrivate.objects.filter(code=room_code)
        endpoint = "me/player/play"
        data = {
            "context_uri": f"spotify:playlist:{playlist_id}"
        }
        if room.exists():
            room = room[0]
            response = spotify_api_requests(room.host, endpoint, data=json.dumps(data), put_request=True)
        else:
            return Response({'message':'not in a room'}, status=status.HTTP_204_NO_CONTENT)
        
        return Response(response, content_type='application/json', status=status.HTTP_200_OK)