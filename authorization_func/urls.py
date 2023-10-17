from django.urls import path
from .views import UserLogin, UserRegistration, EmailConfirmation, PasswordChange, PasswordReset

urlpatterns = [
    path('login/', UserLogin.as_view(), name='login'),
    path('register/', UserRegistration.as_view(), name='register'),
    path('email-confirmation/', EmailConfirmation.as_view(), name='email-confirmation'),
    path('password-change/', PasswordChange.as_view(), name='password-change'),
    path('password-reset/', PasswordReset.as_view(), name='password-reset'),
]
