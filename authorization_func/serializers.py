from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email', 'name', 'surname', 'phone_number', 'access_token')

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
    otp_code = serializers.CharField(max_length=6)

class PasswordChangeSerializer(serializers.Serializer):
    old_password = serializers.CharField()
    new_password = serializers.CharField()
    repeat_new_password = serializers.CharField()

    def validate(self, data):
        user = self.context['request'].user

        old_password = data.get('old_password')
        new_password = data.get('new_password')
        repeat_new_password = data.get('repeat_new_password')

        if not user.check_password(old_password):
            raise serializers.ValidationError({'message': 'Invalid old password'})

        if new_password != repeat_new_password:
            raise serializers.ValidationError({'message': 'New passwords do not match'})

        return data


class PasswordResetSerializer(serializers.Serializer):
    email = serializers.EmailField()

class PasswordResetVerifySerializer(serializers.Serializer):
    otp_code = serializers.CharField(max_length=6)
    

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email', 'name', 'surname', 'phone_number', 'photo',
                  'university', 'faculty', 'specialty', 'graduation_year',
                  'email', 'phone_number', 'social_links',
                  'workplace', 'position', 'short_info', 'achievements')

class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('name', 'surname', 'photo', 'university', 'faculty', 'specialty', 'graduation_year',
                  'email', 'phone_number', 'social_links',
                  'workplace', 'position', 'short_info', 'achievements')
                  
class UserFilterSerializer(serializers.Serializer):
    name = serializers.CharField(required=False)
    specialty = serializers.CharField(required=False)
    education_year = serializers.IntegerField(required=False)
    location = serializers.CharField(required=False)

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'id', 'email', 'name', 'surname', 'phone_number',
            'university', 'faculty', 'specialty', 'graduation_year',
            'social_links', 'workplace', 'position', 'short_info', 'achievements'
        )