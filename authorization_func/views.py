from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.generics import ListAPIView, RetrieveAPIView, UpdateAPIView
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
import requests
from django.contrib.auth.tokens import default_token_generator
from rest_framework.generics import CreateAPIView
from rest_framework import permissions
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes
from django.core.mail import send_mail
from .models import User
from .models import PasswordResetToken  
from rest_framework.pagination import PageNumberPagination
import random
import string
from .serializers import (
    UserSerializer,
    UserRegistrationSerializer,
    EmailConfirmationSerializer,
    PasswordChangeSerializer,
    PasswordResetSerializer,
    UserUpdateSerializer,
    UserProfileSerializer,
)
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import update_session_auth_hash
from rest_framework.generics import RetrieveUpdateAPIView



def generate_otp_code(length=6):
    characters = string.digits
    return ''.join(random.choice(characters) for _ in range(length))

class UserLogin(TokenObtainPairView):
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        user = User.objects.filter(email=email).first()
        if user and user.check_password(password):
            if not user.email_confirmed:
                return Response({'message': 'Email not confirmed. Please provide OTP code for confirmation.'}, status=status.HTTP_200_OK)
            else:
                refresh = RefreshToken.for_user(user)
                access_token = str(refresh.access_token)
                refresh_token = str(refresh)
                
                user.access_token = access_token  
                user.refresh_token = refresh_token
                user.save()


                return Response({
                    'message': 'Login successful',
                    'access_token': access_token,
                    'refresh_token': refresh_token,
                    'name': user.name,
                    'surname': user.surname,
                    'email': user.email,
                    'phone_number': user.phone_number,
                }, status=status.HTTP_200_OK)
        else:
            return Response({'message': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)


class UserRegistration(CreateAPIView):
    serializer_class = UserRegistrationSerializer

    def perform_create(self, serializer):
        password = self.request.data.get('password')
        repeat_password = self.request.data.get('repeat_password')

        if password != repeat_password:
            return Response({'message': 'Passwords do not match'}, status=status.HTTP_400_BAD_REQUEST)

        user = serializer.save()
        otp_code = generate_otp_code()

        user.email_confirmation_code = otp_code
        user.save()

        subject = 'OTP Code Confirmation'
        message = f'Your OTP Code is: {otp_code}'
        from_email = 'sorana6950@wisnick.com'  # Замените на свой адрес электронной почты
        recipient_list = [user.email]
        send_mail(subject, message, from_email, recipient_list, fail_silently=False)

        return Response({'message': 'Registration successful. OTP code sent for email confirmation.'}, status=status.HTTP_201_CREATED)


class EmailConfirmation(APIView):
    def post(self, request):
        otp_code = request.data.get('otp_code')
        
        if not otp_code:
            return Response({'message': 'Требуется код OTP.'}, status=status.HTTP_400_BAD_REQUEST)
        user = User.objects.filter(email_confirmation_code=otp_code, email_confirmed=False).first()
        if user:
            user.email_confirmed = True
            user.save()
            return Response({'message': 'Email подтвержден. Теперь вы можете войти.'}, status=status.HTTP_200_OK)
        else:
            return Response({'message': 'Неверный код OTP.'}, status=status.HTTP_400_BAD_REQUEST)


class PasswordChange(UpdateAPIView):
    serializer_class = PasswordChangeSerializer
    permission_classes = [IsAuthenticated]
    
    def update(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        user = request.user

        # Получите новый пароль из сериализатора
        new_password = serializer.validated_data['new_password']
        # Установите новый пароль для пользователя
        user.set_password(new_password)
        user.save()

        return Response({'message': 'Password successfully changed'})

class PasswordReset(APIView):
    def post(self, request):
        email = request.data.get('email')
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({'message': 'Пользователь с этим email не найден'}, status=status.HTTP_400_BAD_REQUEST)
        def generate_random_otp(length=6):
            digits = string.digits  
            otp_code = ''.join(random.choice(digits) for _ in range(length))
            return otp_code
        # Создайте и сохраните OTP-код
        otp_code = generate_random_otp()
        user.password_reset_token = otp_code
        user.save()

        subject = 'Password Reset OTP Code'
        message = f'Your OTP Code for password reset is: {otp_code}'
        from_email = 'test05545350@gmail.com'  # Замените на свой адрес электронной почты
        recipient_list = [user.email]
        send_mail(subject, message, from_email, recipient_list, fail_silently=False)

        return Response({'message': 'Password reset OTP code sent'}, status=status.HTTP_200_OK)
        
class PasswordResetVerify(APIView):
    def post(self, request):
        otp_code = request.data.get('otp_code')

        try:
            user = User.objects.get(password_reset_token=otp_code)
        except User.DoesNotExist:
            return Response({'message': 'Неверный OTP-код'}, status=status.HTTP_400_BAD_REQUEST)

        if user.password_reset_token:
            def generate_random_password(length=12):
                characters = string.ascii_letters + string.digits
                password = ''.join(random.choice(characters) for _ in range(length))
                return password

            new_password = generate_random_password()
            user.set_password(new_password)
            user.password_reset_token = None  
            user.save()

            subject = 'New Password'
            message = f'Your new password is: {new_password}'
            from_email = 'test05545350@gmail.com'
            recipient_list = [user.email]
            send_mail(subject, message, from_email, recipient_list, fail_silently=False)

            return Response({'message': 'Password successfully reset. New password sent to your email.'}, status=status.HTTP_200_OK)
        else:
            return Response({'message': 'Неверный OTP-код или срок действия OTP-кода истек'}, status=status.HTTP_400_BAD_REQUEST)

class UserListView(ListAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all().order_by('name')  
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['name']
    ordering_fields = ['specialty', 'graduation_year', 'location']
    pagination_class = PageNumberPagination

    def get_serializer(self, *args, **kwargs):
        user = self.request.user
        if user.is_authenticated:
            self.serializer_class.Meta.fields = ('id', 'email', 'name', 'surname', 'phone_number', 'access_token')
        return super().get_serializer(*args, **kwargs)


class UserUpdateView(RetrieveUpdateAPIView):
    serializer_class = UserUpdateSerializer
    permission_classes = [IsAuthenticated]
    
    def get_object(self):
        return self.request.user

    def perform_update(self, serializer):
        serializer.save()


class UserDetailView(RetrieveAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()

class UserProfileDetailView(RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserProfileSerializer