from django.db import models
import string
import random
from django.contrib.auth.models import AbstractUser

def RoomCode():
    l = 8;
    while True:
        code = ''.join(random.choice(string.ascii_letters+string.digits) for i in range(l))
        if RoomPublic.objects.filter(code=code).count() == 0 or RoomPrivate.objects.filter(code=code).count():
            break
    return code


class User(AbstractUser):
    spotify_id = models.CharField(max_length=255, unique=True, default=None, null=True)
    email = models.EmailField()
    like_dislike_ratio = models.FloatField(default=0.5)
    
    
class Playlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255, default='default_name')
    spotify_playlist_id = models.CharField(max_length=255, default='default_id')
    
    
class PlaylistSong(models.Model):
    playlist = models.ForeignKey(Playlist, on_delete=models.CASCADE)
    song_id = models.CharField(max_length=255, default='default_song')
    

class UserAction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    song = models.ForeignKey(PlaylistSong, on_delete=models.CASCADE)
    action_type = models.CharField(max_length=255, choices=[('like', 'Like'), ('dislike', 'Dislike')])  # 'like' or 'dislike'
    

class RoomPublic(models.Model):
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=8, unique=True, default=RoomCode)
    current_playlist = models.ForeignKey(Playlist, on_delete=models.CASCADE, null=True, related_name='current_playlist')
    playlist_1 = models.ForeignKey(Playlist, on_delete=models.CASCADE, null=True, related_name='playlist_1')
    playlist_2 = models.ForeignKey(Playlist, on_delete=models.CASCADE, null=True, related_name='playlist_2')
    rank = models.IntegerField(default=0)  # 1 for first choice, 2 for second choice


class RoomPrivate(models.Model):
    name = models.CharField(max_length=255)
    host = models.CharField(max_length=50, unique=True)
    created_user = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE)
    code = models.CharField(max_length=8, unique=True, default=RoomCode)
    playlist = models.ForeignKey(Playlist, null=True, on_delete=models.CASCADE)
    created_time = models.DateTimeField(auto_now_add=True)
    votes_to_skip = models.IntegerField(default=1)
    guest_can_pause = models.BooleanField(default=False)
    is_public = models.BooleanField(default=True)
    current_song_id = models.CharField(max_length=255, default=None, null=True, blank=True)
    
     
class CommentPrivate(models.Model):
    room = models.ForeignKey(RoomPrivate, on_delete=models.CASCADE, related_name='room_private')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

class CommentPublic(models.Model):
    room = models.ForeignKey(RoomPublic, on_delete=models.CASCADE, related_name= 'room_public')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    