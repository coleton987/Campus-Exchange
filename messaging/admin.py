from django.contrib import admin
from .models import Conversation, Message

@admin.register(Conversation)
class ConversationAdmin(admin.ModelAdmin):
    list_display = ('id', 'get_participants', 'created_at')  # Customize fields to display
    search_fields = ('participants__email',)  # Allow searching by participant email
    filter_horizontal = ('participants',)  # Better UI for ManyToMany fields
    
    def get_participants(self, obj):
        return ", ".join([str(user) for user in obj.participants.all()])
    get_participants.short_description = 'Participants'


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('id', 'conversation', 'sender', 'timestamp')
    search_fields = ('sender__email', 'content')