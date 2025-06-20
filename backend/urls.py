from django.urls import path
from .views import telegram_webhook ,usernames,register_user,login_user

app_name = 'telebot_app'

urlpatterns = [
    path('bot/telegramwebhook/', telegram_webhook, name='telegram_webhook'),        #webhook
    path('users/',usernames,name='username'),                                       #authentication needed endpoint
    path('api/register/', register_user, name='register-user'),                     #public endpoint
    path('login/', login_user, name='login'),                                       #login url
    
]