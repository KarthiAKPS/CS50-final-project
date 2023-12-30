from rest_framework import serializers
from .models import RoomPrivate

   
class RoomSerializer(serializers.ModelSerializer):
    playlist_cover = serializers.SerializerMethodField()

    class Meta:
        model = RoomPrivate
        fields = ('id', 'code', 'name', 'guest_can_pause', 'votes_to_skip', 'created_time', 'playlist','created_user', 'host', 'is_public', 'is_creator', 'playlist_cover')

    def get_playlist_cover(self, obj):
        if obj.playlist and obj.playlist.playlist_cover:
            return obj.playlist.playlist_cover.url 
        else:
            return None     

class CreateRoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = RoomPrivate
        fields = ('name', 'votes_to_skip', 'guest_can_pause', 'is_public' )
        
        
class EditRoomSerializer(serializers.ModelSerializer):
    code = serializers.CharField(validators=[])
    class Meta:
        model = RoomPrivate
        fields = ('name', 'votes_to_skip', 'guest_can_pause', 'is_public', 'code' )