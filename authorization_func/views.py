from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.generics import ListAPIView, RetrieveAPIView, UpdateAPIView
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes
from django.core.mail import send_mail
from .models import User, AccessToken
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
)
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken

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

class PasswordChange(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def post(self, request):
        user = request.user
        old_password = request.data.get('old_password')
        new_password = request.data.get('new_password')
        repeat_new_password = request.data.get('repeat_new_password')

        if user.check_password(old_password):
            if new_password == repeat_new_password:
                user.set_password(new_password)
                user.save()
                return Response({'message': 'Password changed successfully'}, status=status.HTTP_200_OK)
            else:
                return Response({'message': 'New password and repeat password do not match'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'message': 'Invalid old password'}, status=status.HTTP_401_UNAUTHORIZED)

class PasswordReset(APIView):
    def post(self, request):
        email = request.data.get('email')
        return Response({'message': 'Password reset OTP code sent'}, status=status.HTTP_200_OK)

class UserUpdateView(UpdateAPIView):
    serializer_class = UserUpdateSerializer
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated]


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

class UserDetailView(RetrieveAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()
