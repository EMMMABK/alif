from rest_framework import serializers
from .models import News

class NewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = News
        fields = '__all__'

class NewsCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = News
        fields = ['image', 'title', 'content']
