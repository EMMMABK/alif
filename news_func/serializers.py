from rest_framework import serializers
from .models import News

class NewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = News
        fields = '__all__'

class ContentItemSerializer(serializers.Serializer):
    def to_representation(self, instance):
        item_type = instance['type']
        if item_type == 'photo':
            serializer = ImageContentItemSerializer(instance)
        elif item_type == 'paragraph':
            serializer = TextContentItemSerializer(instance)
        return serializer.data

class ImageContentItemSerializer(serializers.Serializer):
    type = serializers.ChoiceField(choices=["photo"])
    image = serializers.ImageField()

class TextContentItemSerializer(serializers.Serializer):
    type = serializers.ChoiceField(choices=["paragraph"])
    text = serializers.CharField()

class ContentItemSerializer(serializers.Serializer):
    def to_representation(self, instance):
        if instance['type'] == 'photo':
            return ImageContentItemSerializer(instance).data
        elif instance['type'] == 'paragraph':
            return TextContentItemSerializer(instance).data

class NewsCreateSerializer(serializers.ModelSerializer):
    content = ContentItemSerializer(many=True)
    
    class Meta:
        model = News
        fields = ['title', 'content']

    def create(self, validated_data):
        content_data = validated_data.pop('content')
        news = News.objects.create(**validated_data)

        for item in content_data:
            if item['type'] == 'photo':
                image_serializer = ImageContentItemSerializer(data=item)
                if image_serializer.is_valid():
                    news.content.create(**image_serializer.validated_data)
            elif item['type'] == 'paragraph':
                text_serializer = TextContentItemSerializer(data=item)
                if text_serializer.is_valid():
                    news.content.create(**text_serializer.validated_data)

        return news

    def validate(self, data):
        content_data = data.get('content')

        if not content_data:
            raise serializers.ValidationError("Content is required")

        for item in content_data:
            if item['type'] == 'photo':
                image_serializer = ImageContentItemSerializer(data=item)
                if not image_serializer.is_valid():
                    raise serializers.ValidationError(image_serializer.errors)
            elif item['type'] == 'paragraph':
                text_serializer = TextContentItemSerializer(data=item)
                if not text_serializer.is_valid():
                    raise serializers.ValidationError(text_serializer.errors)

        return data
