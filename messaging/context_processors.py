from .models import Message, Conversation
from django.db.models import Q

def unread_messages_count(request):
    """
    Context processor to add unread message count to all templates
    """
    if request.user.is_authenticated:
        # Count unread messages in conversations where the user is a participant
        # but not the sender of the message
        unread_count = Message.objects.filter(
            conversation__participants=request.user,
            is_read=False
        ).exclude(sender=request.user).count()
        
        return {'unread_messages_count': unread_count}
    
    return {'unread_messages_count': 0}
