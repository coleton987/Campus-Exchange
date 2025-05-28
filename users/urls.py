from django.urls import path, include
from . import views

app_name = 'users'

urlpatterns = [
    path('register/', views.register),
    path('verification_form/', views.verification_form, name='verification_form'),
    path('log_in/', views.log_in),
    path('log_out/', views.log_out),
]