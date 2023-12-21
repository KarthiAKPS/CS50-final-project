from rest_framework import serializers
from .models import RoomPrivate

class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = RoomPrivate
        fields = ('id', 'name', 'code', 'playlist', 'created_time', 'votes_to_skip', 'guest_can_pause', 'created_user', 'host', 'is_public', 'is_creator')
        

class CreateRoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = RoomPrivate
        fields = ('name', 'votes_to_skip', 'guest_can_pause', 'is_public' )
        
        
class EditRoomSerializer(serializers.ModelSerializer):
    code = serializers.CharField(validators=[])
    class Meta:
        model = RoomPrivate
        fields = ('name', 'votes_to_skip', 'guest_can_pause', 'is_public', 'code' )