from django.contrib import admin
from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.homepage),
    path('about/', views.about),
    path('users/', include('users.urls')),
    path('listing/', include('listings.urls')),
    path('messaging/', include('messaging.urls')),
    #path('payment/', include('payment.urls')),
    #path('seller/', include('seller.urls')),
] 
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) 