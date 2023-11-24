from rest_framework import serializers
from .models import Room

class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = ('id', 'name', 'code', 'current_playlist', 'playlist_1', 'playlist_2', 'created_at')