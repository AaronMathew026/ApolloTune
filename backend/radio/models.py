from django.db import models
from django.contrib.auth.models import User
# Create your models here.

# User Profile Model
class UserProfile(models.Model):
    """
    This class extends Djangos built-in User model to  add Tuner/Creator distinction
    This follows a one-to-one relationship with the User model.
    """
    USER_TYPE_CHOICES = [
        ('tuner', 'Tuner'), #Listeners
        ('creator', 'Creator'), #Broadcasters
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES)
    bio = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f"{self.user.username} - {self.user_type}"
    
class Channel(models.Model):
    """
    Each Creator can have their own induvidual Channel.
    """
    creator = models.OneToOneField(
        User, 
        on_delete=models.CASCADE, 
        related_name='channel', 
        limit_choices_to={'profile__user_type': 'creator'}
    )
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    genre = models.CharField(max_length=50, blank=True, null=True)
    is_live = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} by {self.creator.username}"




class Broadcast(models.Model):
    """
    Individual Broadcast sessions for each Channel.
    Tracks when a creator goes live and the details of that session.
    """
    channel = models.ForeignKey(Channel, on_delete=models.CASCADE, related_name='broadcasts')
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    start_time = models.DateTimeField(auto_now_add=True)
    end_time = models.DateTimeField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    current_listeners = models.PositiveIntegerField(default=0)

    def __str__(self):
        status = "Live" if self.is_active else "Ended"
        return f"Broadcast: {self.title} on {self.channel.name} ({status})"



class ChatMessage(models.Model):
    """
    Chat Messages sent by Tuners during a broadcast
    """
    broadcast = models.ForeignKey(Broadcast, on_delete=models.CASCADE, related_name='messages')
    user = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'profile__user_type': 'tuner'},blank = True, null = True)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['timestamp']

    def __str__(self):
        return f"Message by {self.user.username} at {self.timestamp}"
    

class Listener(models.Model):
    """
    Tracks which Tuners are listening to which Broadcasts.
    """
    broadcast = models.ForeignKey(Broadcast, on_delete=models.CASCADE, related_name='listeners')
    user = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'profile__user_type': 'tuner'})
    joined_at = models.DateTimeField(auto_now_add=True)
    left_at = models.DateTimeField(blank=True, null=True)
   
    class Meta:
        unique_together = ('broadcast', 'user')

    def __str__(self):
        return f"{self.user.username} listening to {self.broadcast.title}"
