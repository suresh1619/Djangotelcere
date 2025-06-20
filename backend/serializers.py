# telegram_bot_app/serializers.py
from rest_framework import serializers
from .models import TelegramUser

class TelegramUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = TelegramUser
        fields = '__all__'


from rest_framework import serializers
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = [ 'username', 'email', 'password']

    def create(self, validated_data):
        # Use create_user to properly hash the password
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email'),
            password=validated_data['password']
        )
        return user
