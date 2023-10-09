from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from .serializers import UserSerializer, UserLoginSerializer
from django.core.exceptions import PermissionDenied
from django.utils import timezone
import pyotp

# Create your views here.


@api_view(['POST'])
@permission_classes([AllowAny])
def user_register(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        user.set_password(request.data['password'])
        user.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([AllowAny])
def user_login(request):
    serializer = UserLoginSerializer(data=request.data)
    if serializer.is_valid():
        user = authenticate(request, email=serializer.validated_data['email'], password=serializer.validated_data['password'])
        if user is not None:
            login(request, user)
            return Response({'message': 'Login successful'})
    return Response({'message': 'Login failed'}, status=status.HTTP_401_UNAUTHORIZED)

@login_required
@api_view(['GET'])
def user_profile(request):
    serializer = UserSerializer(request.user)
    return Response(serializer.data)



@api_view(['POST'])
@login_required
def send_otp(request):
    user = request.user
    if not user.can_resend_otp():
        raise PermissionDenied("Too many requests")

    otp_secret = user.otp_secret
    if not otp_secret:
        otp_secret = pyotp.random_base32()
        user.otp_secret = otp_secret
        user.save()

    totp = pyotp.TOTP(otp_secret)
    otp = totp.now()

    user.last_otp_sent = timezone.now()
    user.save()

    return Response({'message': 'OTP code sent successfully'})

