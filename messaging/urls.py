from django.contrib import admin
from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('', views.conversation_list), 
    path('start_conv', views.start_conversation), 
    path('conversation/<int:conversation_id>/', views.conversation_detail, name='conversation_detail'),
    path('delete_conversation/<int:conversation_id>/', views.delete_conversation, name='delete_conversation'),
] 
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) 