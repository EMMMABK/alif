from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.user_register, name='user_register'),
    path('login/', views.user_login, name='user_login'),
    path('profile/', views.user_profile, name='user_profile'),
    path('send-otp/', views.send_otp, name='send_otp'),
    path('change-password/', views.change_password, name='change_password'),
    path('password-reset/', views.password_reset_request, name='password_reset_request'),
    path('resend-otp/', views.resend_otp, name='resend_otp'),
]
