from django.db import models
from django.utils import timezone


class User(models.Model):
    spotify_id = models.CharField(max_length=255, unique=True)
    username = models.CharField(max_length=255)
    email = models.EmailField()
    like_dislike_ratio = models.FloatField(default=0.5)
    
    
class Playlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    spotify_playlist_id = models.CharField(max_length=255)
    
    
class PlaylistSong(models.Model):
    playlist = models.ForeignKey(Playlist, on_delete=models.CASCADE)
    song_id = models.CharField(max_length=255)
    

class UserAction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    song = models.ForeignKey(PlaylistSong, on_delete=models.CASCADE)
    action_type = models.CharField(max_length=255, choices=[('like', 'Like'), ('dislike', 'Dislike')])  # 'like' or 'dislike'
    

class Room(models.Model):
    name = models.CharField(max_length=255)
    current_playlist = models.ForeignKey(Playlist, on_delete=models.CASCADE, null=True, related_name='current_playlist')
    playlist_1 = models.ForeignKey(Playlist, on_delete=models.CASCADE, null=True, related_name='playlist_1')
    playlist_2 = models.ForeignKey(Playlist, on_delete=models.CASCADE, null=True, related_name='playlist_2')


class RoomVote(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    playlist = models.ForeignKey(Playlist, on_delete=models.CASCADE)
    rank = models.IntegerField(default=0)  # 1 for first choice, 2 for second choice
    

class Comment(models.Model):
    room = models.ForeignKey('rooms.Room', on_delete=models.CASCADE)
    user = models.ForeignKey('users.User', on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    