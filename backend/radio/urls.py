from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views


router = DefaultRouter() #Created a Router object to automatically handle URL routing for our ViewSets.

router.register('profiles', views.UserProfileViewSet, basename='profile')
router.register('channels', views.ChannelViewSet, basename='channel')
router.register('broadcasts', views.BroadcastViewSet, basename='broadcast')
router.register('chat-messages', views.ChatMessageViewSet, basename='chat')
router.register('listeners', views.ListenerViewSet, basename='listener')


# The router generates these URLs automatically:
# /profiles/              → List/Create profiles
# /profiles/{id}/         → Retrieve/Update/Delete profile
# /channels/              → List/Create channels
# /channels/live/         → Custom action (channels that are live)
# /broadcasts/live/       → Custom action (live broadcasts)
# /broadcasts/by_channel/ → Custom action (broadcasts filtered by channel)
# /chat/by_broadcast/     → Custom action (chat filtered by broadcast)
# /listeners/join/        → Custom action (join broadcast)
# /listeners/leave/       → Custom action (leave broadcast)


urlpatterns = router.urls