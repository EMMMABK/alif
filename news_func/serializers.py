from rest_framework import serializers
from .models import News

class NewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = News
        fields = '__all__'

class ContentItemSerializer(serializers.Serializer):
    type = serializers.ChoiceField(choices=["photo", "paragraph"])
    value = serializers.CharField()

class NewsCreateSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(write_only=True)
    content = ContentItemSerializer(many=True)

    class Meta:
        model = News
        fields = ['image', 'title', 'content']

    def create(self, validated_data):
        image = validated_data.pop('image')
        content_data = validated_data.pop('content')
        news = News.objects.create(**validated_data)

        news.image_url = self.context['request'].build_absolute_uri(image.url)
        news.save()

        for item in content_data:
            content_item_serializer = ContentItemSerializer(data=item)
            if content_item_serializer.is_valid():
                news.content.create(**content_item_serializer.validated_data)

        return news

    def validate(self, data):
        content_data = data.get('content')

        if not content_data:
            raise serializers.ValidationError("Content is required")

        for item in content_data:
            content_item_serializer = ContentItemSerializer(data=item)
            if not content_item_serializer.is_valid():
                raise serializers.ValidationError(content_item_serializer.errors)

        return data

