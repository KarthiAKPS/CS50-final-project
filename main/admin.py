from django.contrib import admin
from .models import RoomPublic, User, Playlist, RoomPrivate, PlaylistSong, UserAction, CommentPublic, CommentPrivate

# Register your models here.
admin.site.register(User)
admin.site.register(RoomPublic)
admin.site.register(Playlist)
admin.site.register(RoomPrivate)
admin.site.register(CommentPublic)
admin.site.register(PlaylistSong)
admin.site.register(UserAction)
admin.site.register(CommentPrivate)
