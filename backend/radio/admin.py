from django.contrib import admin
from .models import UserProfile, Channel, Broadcast, ChatMessage, Listener


#list_display: fields to display in the admin list view
#list_filter: fields to filter by in the admin list view
#search_fields: enables search box for specified fields
#readonly_fields: fields that are read-only in the admin detail view

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'user_type', 'created_at']
    list_filter = ['user_type']
    search_fields = ['user__username', 'bio']

@admin.register(Channel)
class ChannelAdmin(admin.ModelAdmin):
    list_display = ['name', 'creator', 'genre', 'is_live', 'created_at']
    list_filter = ['is_live', 'genre']
    search_fields = ['name', 'description', 'creator__username']
    readonly_fields = ['created_at']

@admin.register(Broadcast)
class BroadcastAdmin(admin.ModelAdmin):
    list_display = ['title', 'channel', 'is_active', 'current_listeners', 'start_time']
    list_filter = ['is_active', 'start_time']
    search_fields = ['title', 'description', 'channel__name']
    readonly_fields = ['start_time']

@admin.register(ChatMessage)
class ChatMessageAdmin(admin.ModelAdmin):
    list_display = ['user', 'broadcast', 'message_preview', 'timestamp']
    list_filter = ['timestamp']
    search_fields = ['user__username', 'message']
    readonly_fields = ['timestamp']
    
    def message_preview(self, obj):
        return obj.message[:50] + '...' if len(obj.message) > 50 else obj.message
    message_preview.short_description = 'Message'

@admin.register(Listener)
class ListenerAdmin(admin.ModelAdmin):
    list_display = ['user', 'broadcast', 'joined_at', 'left_at']
    list_filter = ['joined_at']
    search_fields = ['user__username', 'broadcast__title']
    readonly_fields = ['joined_at']
