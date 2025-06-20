from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.conf import settings

from .models import TelegramUser
from .serializers import TelegramUserSerializer, UserSerializer
from .tasks import send_welcome_email

import telebot
import json
import os
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# Use environment variable for bot token
BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "")
bot = telebot.TeleBot(BOT_TOKEN)


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    user = message.from_user
    username = user.username
    first_name = user.first_name

    telegram_user, created = TelegramUser.objects.get_or_create(
        telegram_id=user.id,
        defaults={
            'username': username,
            'first_name': first_name,
            'last_name': user.last_name,
        }
    )

    if not created:
        telegram_user.username = username
        telegram_user.first_name = first_name
        telegram_user.last_name = user.last_name
        telegram_user.save()

    name_to_use = f"@{username}" if username else first_name
    bot.reply_to(message, f"Hello {name_to_use}, how are you doing?")


@csrf_exempt
@api_view(['POST'])
@permission_classes([AllowAny])
def telegram_webhook(request):
    try:
        data = request.body.decode('utf-8')
        update = telebot.types.Update.de_json(data)
        username = update.message.from_user.username
        first_name = update.message.from_user.first_name
        # print(username, first_name)

        bot.process_new_updates([update])
        return JsonResponse({'status': 'ok'})

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def usernames(request):
    data = TelegramUser.objects.all()
    serializer = TelegramUserSerializer(data, many=True)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([AllowAny])
def register_user(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        send_welcome_email(user.email)
        return Response({'message': 'User registered successfully'}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


@api_view(['POST'])
@permission_classes([AllowAny])
def login_user(request):
    username = request.data.get('username')
    password = request.data.get('password')

    if not username or not password:
        return Response({'error': 'Username and password are required.'}, status=status.HTTP_400_BAD_REQUEST)

    user = authenticate(username=username, password=password)
    if user is None:
        return Response({'error': 'Invalid credentials.'}, status=status.HTTP_401_UNAUTHORIZED)

    tokens = get_tokens_for_user(user)

    return Response({
        'message': 'Login successful.',
        'username': user.username,
        'email': user.email,
        'tokens': tokens
    }, status=status.HTTP_200_OK)
