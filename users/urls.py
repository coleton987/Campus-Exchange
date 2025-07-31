from django.urls import path, include
from django.conf.urls.static import static

from django.conf import settings
from . import views

# app_name = 'users'

urlpatterns = [
    path('register/', views.register, name='register'),
    path('verification_form/', views.verification_form, name='verification_form'),
    path('resend_verification/', views.resend_verification_code, name='resend_verification'),
    path('log_in/', views.log_in, name="login"),
    path('log_out/', views.log_out, name="logout"),
    path('password_reset/', include('django.contrib.auth.urls')),
]
