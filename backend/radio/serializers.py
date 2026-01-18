from rest_framework import serializers
from django.contrib.auth.models import User
from .models import UserProfile, Channel, Broadcast, ChatMessage, Listener
# Serializers convert the Django models to JSON format for API responses and vice-versa.
# Why? because API's communicate via JSON, so we need to serialize our data. but also
# we need to deserialize JSON data from API requests back into Django models.


class UserSerializer(serializers.ModelSerializer):
    """Serializes Djangos built in User model, used for authentication and API responses."""
    class Meta:
        model = User
        fields = ['id', 'username', 'email']


class UserProfileSerializer(serializers.ModelSerializer):
    """Serializes the UserProfile model."""
    user = UserSerializer(read_only=True)

    class Meta:
        model = UserProfile
        fields = ['id', 'user', 'user_type', 'bio', 'created_at']

class ChannelSerializer(serializers.ModelSerializer):
    """ Serializes the Channel model, including the username for display purposes."""

    creator_username = serializers.CharField(source='creator.username', read_only=True) # Allows us to display the creator's username 
    class Meta:
        model = Channel
        fields = ['id', 'creator', 'creator_username', 'name', 'description', 'genre', 'frequency', 'is_live', 'created_at']
        read_only_fields = ['creator', 'created_at']

class BroadcastSerializer(serializers.ModelSerializer):
    """ Serializes the Broadcast model, including the channel name for display purposes."""
    channel_name = serializers.CharField(source='channel.name', read_only=True) # Allows us to display the channel name
    class Meta:
        model = Broadcast
        fields = ['id', 'channel', 'channel_name', 'title', 'description', 'start_time', 'end_time', 'is_active', 'current_listeners']
        read_only_fields = ['channel', 'start_time', 'current_listeners']

class ChatMessageSerializer(serializers.ModelSerializer):
    """ Serializes the ChatMessage model, including the username for display purposes."""
    user_username = serializers.CharField(source='user.username', read_only=True) # Allows us to display the user's username
    class Meta:
        model = ChatMessage
        fields = ['id', 'user', 'user_username', 'broadcast', 'message', 'timestamp']
        read_only_fields = ['user', 'timestamp']


class ListenerSerializer(serializers.ModelSerializer):
    """ Serializes the Listener model, including the username for display purposes."""
    user_username = serializers.CharField(source='user.username', read_only=True) # Allows us to display the user's username
    broadcast_title = serializers.CharField(source='broadcast.title', read_only=True) # Allows us to display the broadcast title
    class Meta:
        model = Listener
        fields = ['id', 'user', 'user_username', 'broadcast', 'broadcast_title', 'joined_at', 'left_at']
        read_only_fields = ['user', 'joined_at', 'left_at']