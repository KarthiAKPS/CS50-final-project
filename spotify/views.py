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

    handle_spotify_login(access_token=access_token)

    return HttpResponse('Access token set')

def is_spotify_authenticated( session_id):
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
    

def spotify_api_requests(session_id, endpoint, post_request=False, put_request=False):
    tokens = get_user_tokens(session_id)
    headers = {'Content-Type': 'application/json',
               'Authorization': "Bearer " + tokens.access_token}

    if post_request:
        post(BASE_URL + endpoint, headers=headers)
    if put_request:
        put(BASE_URL + endpoint, headers=headers)

    response = get(BASE_URL + endpoint, {}, headers=headers)
    try:
        return response.json()
    except:
        return {'Error': 'Issue with request'}

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
    
    handle_spotify_login( access_token = access_token, state = callback_state)

    return redirect('frontend:index')


class IsAuthenticated(APIView):
    def get(self, format=None):
        is_authenticated = is_spotify_authenticated(
            self.request.session.session_key)
        return Response({'status': is_authenticated}, status=status.HTTP_200_OK)
    
class CurrentSong(APIView):
    def get(self, format=None):
        if not self.request.session.exists(self.request.session.session_key):
            self.request.session.create()
        room_code = self.request.session.get('state')
        room = RoomPrivate.objects.filter(code=room_code)
        if room.exists():
            room = room[0]
        else:
            return Response({}, status=status.HTTP_404_NOT_FOUND)
        host = room.host
        endpoint = "me/player/currently-playing"
        response = spotify_api_requests(host, endpoint)

        if 'error' in response or 'item' not in response:
            return Response({}, status=status.HTTP_204_NO_CONTENT)

        item = response.get('item')
        duration = item.get('duration_ms')
        progress = response.get('progress_ms')
        album_cover = item.get('album').get('images')[0].get('url')
        is_playing = response.get('is_playing')
        song_id = item.get('id')

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
            'votes': 0,
            'id': song_id
        }
        
        return Response(song, content_type='application/json', status=status.HTTP_200_OK)


class UserProfile(APIView):
    def get(self, *args, **kwargs):
        if not self.request.session.exists(self.request.session.session_key):
            self.request.session.create()
        u_code = self.request.session.get('state')
        user = User.objects.filter(code=u_code)
        print("users: ", user)
        if user.exists():
            user = user[0]
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
        else:
            return Response({'Error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

def handle_spotify_login(request, access_token, state=None):
    profile = spotify_user_request(access_token, "me")
    needed_response = {
            'display_name': profile.get('display_name'),
            'followers': profile.get('followers').get('total'),
            'id': profile.get('id'),
            'image': profile.get('images')[0].get('url')}
    print(needed_response)
    profile_id = profile.get('id')
    user_id = User.objects.filter(username=profile_id)
    if user_id:
        token = SpotifyToken.objects.get(access_token = access_token)
        user = user_id[0]
        user.username = profile_id
        user.access_token = token.access_token
        user.refresh_token = token.refresh_token
        user.expires_in = token.expires_in
        user.save()
        auth_backend = UsernameBackend()
        user = auth_backend.authenticate(request, username=user.username)
        if user:
            login(request, user, backend='spotify.auth_backends.UsernameBackend')
            print(f'User logged in: {user.username}')
            if user.is_authenticated:
                print(f'User {user.username} is authenticated')
            else:
                print(f'User {user.username} is not authenticated')
        else:
            print('Failed to authenticate user')
    else:
        user = User.objects.filter(username = state)
        if user:
            token = SpotifyToken.objects.get(access_token=access_token)
            user = user[0]
            user.username = profile_id
            user.access_token = token.access_token
            user.refresh_token = token.refresh_token
            user.expires_in = token.expires_in
            user.save()
            auth_backend = UsernameBackend()
            user = auth_backend.authenticate(request, username=user.username)
            if user:
                login(request, user, backend='spotify.auth_backends.UsernameBackend')
                print(f'User logged in: {user.username}')
                if user.is_authenticated:
                    print(f'User {user.username} is authenticated')
                else:
                    print(f'User {user.username} is not authenticated')
            else:
                print('Failed to authenticate user')
        else:
            print('No user to change name')
    return needed_response
        

def spotify_user_request(accessToken, endpoint, post_request=False, put_request=False):
    headers = {'Content-Type': 'application/json',
               'Authorization': "Bearer " + accessToken}

    if post_request:
        post(BASE_URL + endpoint, headers=headers)
    if put_request:
        put(BASE_URL + endpoint, headers=headers)

    response = get(BASE_URL + endpoint, {}, headers=headers)
    try:
        return response.json()
    except:
        return {'Error': 'Issue with request'}