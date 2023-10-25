from rest_framework import serializers
from .models import News

class NewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = News
        fields = '__all__'

class NewsCreateSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(write_only=True)
    
    class Meta:
        model = News
        fields = ['image', 'title', 'content']
    
    def create(self, validated_data):
        image = validated_data.pop('image')
        news = News.objects.create(**validated_data)

        news.image_url = self.context['request'].build_absolute_uri(image.url)
        news.save()

        return news
