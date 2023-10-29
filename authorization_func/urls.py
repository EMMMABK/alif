from django.urls import path
from .views import UserLogin, UserRegistration, EmailConfirmation, PasswordChange, PasswordReset, UserUpdateView, UserListView, UserDetailView, PasswordResetVerify 

urlpatterns = [
    path('login/', UserLogin.as_view(), name='login'),
    path('register/', UserRegistration.as_view(), name='register'),
    path('email-confirmation/', EmailConfirmation.as_view(), name='email-confirmation'),
    path('password-change/', PasswordChange.as_view(), name='password-change'),
    path('password-reset/', PasswordReset.as_view(), name='password-reset'),
    path('password-reset-verify/', PasswordResetVerify.as_view(), name='password-reset-verify'),
    path('user/update/<int:pk>/', UserUpdateView.as_view(), name='user-update'),
    path('users/', UserListView.as_view(), name='user-list'),
    path('user/<int:pk>/', UserDetailView.as_view(), name='user-detail'),
]