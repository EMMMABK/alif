from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email', 'name', 'surname', 'phone_number')

class UserRegistrationSerializer(serializers.ModelSerializer):
    repeat_password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('email', 'name', 'surname', 'phone_number', 'password', 'repeat_password')

    def create(self, validated_data):
        password = validated_data['password']
        repeat_password = validated_data.pop('repeat_password')

        if password != repeat_password:
            raise serializers.ValidationError({'message': 'Passwords do not match'})

        user = User.objects.create(**validated_data)
        user.set_password(password)
        user.save()
        return user

class EmailConfirmationSerializer(serializers.Serializer):
    email = serializers.EmailField()

class PasswordChangeSerializer(serializers.Serializer):
    old_password = serializers.CharField()
    new_password = serializers.CharField()

class PasswordResetSerializer(serializers.Serializer):
    email = serializers.EmailField()
