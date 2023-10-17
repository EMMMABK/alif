from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes
from .models import User
from .serializers import (
    UserSerializer,
    UserRegistrationSerializer,
    EmailConfirmationSerializer,
    PasswordChangeSerializer,
    PasswordResetSerializer,
)

class UserLogin(APIView):
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        # Проверка введенных данных и аутентификация пользователя
        user = User.objects.filter(email=email).first()
        if user and user.check_password(password):
            # Создание и возврат токена (если используется TokenAuthentication)
            # Вам также может потребоваться создать и вернуть OTP-код
            return Response({'message': 'Login successful'}, status=status.HTTP_200_OK)
        else:
            return Response({'message': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

class UserRegistration(CreateAPIView):
    serializer_class = UserRegistrationSerializer

    def perform_create(self, serializer):
        password = self.request.data.get('password')
        repeat_password = self.request.data.get('repeat_password')

        if password != repeat_password:
            return Response({'message': 'Passwords do not match'}, status=status.HTTP_400_BAD_REQUEST)

        serializer.save()


class EmailConfirmation(APIView):
    def post(self, request):
        email = request.data.get('email')
        # Логика для отправки OTP-кода на указанную почту
        # Включая проверку на интервал в 2 минуты
        # Отправка OTP-кода на почту
        return Response({'message': 'OTP code sent'}, status=status.HTTP_200_OK)

class PasswordChange(APIView):
    @permission_classes([IsAuthenticated])
    def post(self, request):
        user = request.user
        old_password = request.data.get('old_password')
        new_password = request.data.get('new_password')
        if user.check_password(old_password):
            user.set_password(new_password)
            user.save()
            return Response({'message': 'Password changed successfully'}, status=status.HTTP_200_OK)
        else:
            return Response({'message': 'Invalid old password'}, status=status.HTTP_401_UNAUTHORIZED)

class PasswordReset(APIView):
    def post(self, request):
        email = request.data.get('email')
        # Логика для отправки OTP-кода на указанную почту для сброса пароля
        # Включая проверку на интервал в 2 минуты
        # Отправка OTP-кода на почту
        return Response({'message': 'Password reset OTP code sent'}, status=status.HTTP_200_OK)
