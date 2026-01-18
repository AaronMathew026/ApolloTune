from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.decorators import action, api_view
from rest_framework.response import Response
from .models import UserProfile, Channel, Broadcast, ChatMessage, Listener
# Create your views here.

from .serializers import (
    UserProfileSerializer, 
    ChannelSerializer, 
    BroadcastSerializer, 
    ChatMessageSerializer, 
    ListenerSerializer
)

class UserProfileViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing User Profiles (Tuner/Creator).
    API endpoints for CRUD operations on UserProfile model.
    This is the basic setup, as Django Rest Framework's ModelViewSet provides
    default implementations for list, create, retrieve, update, and destroy actions.
    when we want to customize behavior, we can override these methods or add new actions. 
    """
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer

class ChannelViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing Channels.
    API endpoints for CRUD operations on Channel model.
    """
    queryset = Channel.objects.all()
    serializer_class = ChannelSerializer
    @action(detail = False, methods = ['get'])
    def live(self, request):
        """
        This is a custom action to get all live channels.
        we dont want to grab non-live channels if we want to display currently live channels.
        :param self: Description
        :param request: Description
        custom endpoint: /api/channels/live/
        """
        live_channels = Channel.objects.filter(is_live = True)
        ChannelSerializer = self.get_serializer(live_channels, many = True)
        return Response(ChannelSerializer.data)

class BroadcastViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing Broadcasts.
    API endpoints for CRUD operations on Broadcast model.
    """
    queryset = Broadcast.objects.all()
    serializer_class = BroadcastSerializer

    @action(detail = False, methods=['get'])
    def live(self, request):
        """
        This is a custom action to get all live broadcasts.
        We don't want to grab non-live broadcasts if we want to display currently live broadcasts.
        :param self: Description
        :param request: Description
        custom endpoint: /api/broadcasts/live/
        """
        live_broadcasts = Broadcast.objects.filter(is_active = True, end_time__isnull = True)
        BroadcastSerializer = self.get_serializer(live_broadcasts, many = True)
        return Response(BroadcastSerializer.data)
    
    @action(detail=False, methods=['get'])
    def by_channel(self,request):
        """
        This is a custom action to get broadcasts by channel.
        :param self: Description
        :param request: Description
        custom endpoint: /api/broadcasts/by_channel/?channel_id=<channel_id>
        """
        channel_id = request.query_params.get('channel_id')
        if not channel_id:
            return Response({"error": "channel_id is required."}, status=status.HTTP_400_BAD_REQUEST)
        
        broadcasts = Broadcast.objects.filter(channel__id=channel_id)
        serializer = self.get_serializer(broadcasts, many=True)
        return Response(serializer.data)
    

class ChatMessageViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing Chat Messages.
    API endpoints for CRUD operations on ChatMessage model.
    """
    queryset = ChatMessage.objects.all()
    serializer_class = ChatMessageSerializer

    @action(detail=False, methods=['get'])
    def by_broadcast(self, request):
        """
        This is a custom action to get chat messages by broadcast.
        :param self: Description
        :param request: Description
        custom endpoint: /api/chatmessages/by_broadcast/?broadcast_id=<broadcast_id>
        """
        broadcast_id = request.query_params.get('broadcast_id')
        if not broadcast_id:
            return Response({"error": "broadcast_id is required."}, status=status.HTTP_400_BAD_REQUEST)
        
        chat_messages = ChatMessage.objects.filter(broadcast__id=broadcast_id)
        serializer = self.get_serializer(chat_messages, many=True)
        return Response(serializer.data)
    

class ListenerViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing Listeners.
    API endpoints for CRUD operations on Listener model.

    """
    queryset = Listener.objects.all()
    serializer_class = ListenerSerializer

    @action(detail = False, methods = ['post'])
    def join(self,request):
        """
        Custom action for a user to join a broadcast as a listener.
        :param self: Description
        :param request: Description
        custom endpoint: /api/listeners/join/
        """
        user_id = request.data.get('user_id')
        broadcast_id = request.data.get('broadcast_id')

        if not user_id or not broadcast_id:
            return Response({"error": "user_id and broadcast_id are required."}, status=status.HTTP_400_BAD_REQUEST)
        
        existing = Listener.objects.filter(
            user__id = user_id, 
            broadcast__id = broadcast_id, 
            left_at__isnull = True
        ).first()

        if existing:
            return Response({"error": "User is already listening to this broadcast."}, status=status.HTTP_400_BAD_REQUEST)
        
        listener = Listener.objects.create(
            user_id = user_id,
            broadcast_id = broadcast_id
        )

        broadcast = Broadcast.objects.get(id = broadcast_id)
        broadcast.current_listeners += 1
        broadcast.save()

        serializer = self.get_serializer(listener)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    @action(detail=False, methods = ['post'])
    def leave(self, request):
        """

        Custom action for a user to leave a broadcast as a listener.
        custom endpoint: /api/listeners/leave/        
        :param self: Description
        :param request: Description
        """
        from django.utils import timezone

        broadcast_id = request.data.get('broadcast_id')
        user_id = request.data.get('user_id')
        if not user_id or not broadcast_id:
            return Response({"error": "user_id and broadcast_id are required."}, status=status.HTTP_400_BAD_REQUEST)
        
        listener = Listener.objects.filter(
            user__id = user_id, 
            broadcast__id = broadcast_id, 
            left_at__isnull = True
        ).first()

        if not listener:
            return Response({"error": "Listener record not found."}, status=status.HTTP_404_NOT_FOUND)
        

        listener.left_at = timezone.now()
        listener.save()

        broadcast = Broadcast.objects.get(id = broadcast_id)
        if broadcast.current_listeners > 0:
            broadcast.current_listeners -= 1
            broadcast.save()
        return Response({"message": "Successfully left the broadcast."}, status=status.HTTP_200_OK)