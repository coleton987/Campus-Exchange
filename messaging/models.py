from django.db import models
from django.conf import settings  
from django.utils.timezone import now
from listings.models import Product

class Conversation(models.Model):
    participants = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='conversations')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='conversations')
    created_at = models.DateTimeField(auto_now_add=True)
    display = models.BooleanField(default=True)
    
    def get_unread_count_for_user(self, user):
        """Get the count of unread messages for a specific user in this conversation"""
        return self.messages.filter(is_read=False).exclude(sender=user).count()
    
    def get_latest_message(self):
        """Get the latest message in this conversation"""
        return self.messages.last()
    
    def get_other_participant(self, user):
        """Get the other participant in the conversation (not the current user)"""
        return self.participants.exclude(id=user.id).first()

class Message(models.Model):
    conversation = models.ForeignKey(Conversation, related_name='messages', on_delete=models.CASCADE)
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='sent_messages')
    text = models.TextField()
    timestamp = models.DateTimeField(default=now)
    is_read = models.BooleanField(default=False)

    class Meta:
        ordering = ['timestamp']
        
    def mark_as_read(self):
        """Mark this message as read"""
        self.is_read = True
        self.save()
