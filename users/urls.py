from django.urls import path, include
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

from django.conf import settings
from . import views

# app_name = 'users'

urlpatterns = [
    path('register/', views.register, name='register'),
    path('verification_form/', views.verification_form, name='verification_form'),
    path('resend_verification/', views.resend_verification_code, name='resend_verification'),
    path('log_in/', views.log_in, name="login"),
    path('log_out/', views.log_out, name="logout"),
    path('password_reset/', views.custom_password_reset, name='password_reset'),

    
    # Include all Django authentication URLs (this includes password reset)
    # path('password_reset/', 
    #     auth_views.PasswordResetView.as_view(
    #         success_url='/users/password_reset/done/'
    #     ), 
    #     name='password_reset'),
    
    path('password_reset/done/', 
        auth_views.PasswordResetDoneView.as_view(), 
        name='password_reset_done'),
    
    path('reset/<uidb64>/<token>/', 
        auth_views.PasswordResetConfirmView.as_view(
            success_url='/users/reset/done/'
        ), 
        name='password_reset_confirm'),
    
    path('reset/done/', 
        auth_views.PasswordResetCompleteView.as_view(), 
        name='password_reset_complete'),
 
]