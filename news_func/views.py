from django.shortcuts import render
from rest_framework import generics
from .models import News
from .serializers import NewsSerializer, NewsCreateSerializer
from rest_framework.pagination import PageNumberPagination, LimitOffsetPagination
from rest_framework import permissions
from rest_framework.exceptions import PermissionDenied

# Create your views here
from rest_framework import permissions

class CanCreateNews(permissions.BasePermission):
    def has_permission(self, request, view):
        if view.__class__ == NewsCreateView:
            print("Permission granted for NewsCreateView")  # Добавьте эту строку для отладки
            return True
        else:
            print("Permission denied")
        return False

class CustomLimitOffsetPagination(LimitOffsetPagination):
    default_limit = 10  
    max_limit = 50  

class NewsListCreateView(generics.ListCreateAPIView):
    queryset = News.objects.all().order_by('-created_at')
    serializer_class = NewsSerializer
    pagination_class = CustomLimitOffsetPagination  
    
class NewsRetrieveUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = News.objects.all()
    serializer_class = NewsSerializer

class NewsCreateView(generics.CreateAPIView):
    queryset = News.objects.all()
    serializer_class = NewsCreateSerializer
    permission_classes = [CanCreateNews]

class NewsDeleteView(generics.DestroyAPIView):
    queryset = News.objects.all()
    serializer_class = NewsSerializer
