from django.shortcuts import render
from rest_framework import generics
from .models import News
from .serializers import NewsSerializer, NewsCreateSerializer
from rest_framework.pagination import PageNumberPagination, LimitOffsetPagination

# Create your views here

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

class NewsDeleteView(generics.DestroyAPIView):
    queryset = News.objects.all()
    serializer_class = NewsSerializer
