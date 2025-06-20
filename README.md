
# 📘 Telcere Django Project - Complete Setup Guide

This guide walks you through setting up the **Telcere Django project** with the following components:

- Django + DRF (Django REST Framework)
- JWT-based authentication
- Celery for asynchronous tasks
- Redis as a message broker
- Ngrok for exposing local development server
- Telegram bot webhook integration
- Secure secrets via .env

---

## 🧰 Requirements

Ensure the following are installed:

- Python 3.9+
- pip
- virtualenv (recommended)
- Redis (locally or via WSL on Windows)
- Ngrok

---

## 🔧 Project Setup

### 1. Clone and Setup Environment

```bash
git clone <your-repo-url>
cd telcere
python -m venv venv
venv\Scripts\activate    # On Windows
# or
source venv/bin/activate   # On Mac/Linux
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Create `.env` File

At the project root (`telcere/.env`):

```env
SECRET_KEY=your-django-secret-key
DEBUG=True

# Email Configuration
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password

# Telegram Bot
TELEGRAM_BOT_TOKEN=your-telegram-bot-token
```

> ⚠️ Add `.env` to `.gitignore` to keep secrets secure.

---

## ⚙️ Django Setup

### 1. Apply Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 2. Create Superuser

```bash
python manage.py createsuperuser
```

### 3. Run Server

```bash
python manage.py runserver
```

Visit: [http://127.0.0.1:8000/](http://127.0.0.1:8000/)

---

## 🌐 Expose Server via Ngrok

Ngrok is used to expose your local server to the internet for Telegram webhook testing.

```bash
ngrok http 8000
```

You’ll get a URL like: `https://<your-ngrok-id>.ngrok-free.app`

---

## 🤖 Telegram Webhook Setup

Set the webhook URL like:

```bash
https://<your-ngrok-id>.ngrok-free.app/bot/telegramwebhook/
```

Your `apps.py` or setup script should send a `POST` request to:

```bash
https://api.telegram.org/bot<your-token>/setWebhook
```

With JSON body:

```json
{ "url": "https://<your-ngrok-id>.ngrok-free.app/bot/telegramwebhook/" }
```

---

## ✉️ Email Backend Configuration

Used for sending welcome emails via Celery.

### `settings.py`:

```python
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = config('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD')
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER
```

---

## 🧵 Celery + Redis Setup

### 1. Install & Run Redis

#### Windows:
Use [Memurai](https://www.memurai.com/) or Redis via WSL.

#### Linux/Mac:
```bash
sudo apt install redis-server
redis-server
```

### 2. Celery Settings (`settings.py`)

```python
CELERY_BROKER_URL = 'redis://localhost:6379/0'
CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
```

### 3. Start Celery Worker

```bash
celery -A telcere worker --loglevel=info
```

---

## 🔐 JWT Authentication

### Install Simple JWT

```bash
pip install djangorestframework-simplejwt
```

### Configure DRF in `settings.py`:

```python
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ),
}

from datetime import timedelta

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=30),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
}
```

### Endpoints

- `POST /register/` — Register user
- `POST /login/` — Return access/refresh tokens

---

## 🧪 Test Webhook
Note : to set webhook to your endpoint
```bash
https://api.telegram.org/bot<YOUR_BOT_TOKEN>/setWebhook?url=<YOUR_PUBLIC_URL>
```
To check if Telegram webhook is set correctly:

```bash
https://api.telegram.org/bot<your-token>/getWebhookInfo
```

You should receive a JSON response with the webhook URL.

---

## 📁 Folder Structure

```
telcere/
├── backend/
│   ├── views.py
│   ├── tasks.py
│   ├── urls.py
│   ├── apps.py
├── telcere/
│   ├── settings.py
│   ├── celery.py
│   ├── __init__.py
├
│  
├── .env
├── manage.py
```

---

## 🛠 Common Commands

| Description        | Command                                  |
|--------------------|-------------------------------------------|
| Run Django server  | `python manage.py runserver`              |
| Start Celery       | `celery -A telcere worker --loglevel=info`|
| Start Redis        | `redis-server`                            |
| Run Ngrok          | `ngrok http 8000`                         |
| Create Superuser   | `python manage.py createsuperuser`        |

---

## ✅ You're All Set!

Your Django app now supports:

- JWT login/logout 🔐
- Asynchronous email via Celery ✉️
- Telegram bot integration via webhook 🤖
- Ngrok tunnel for public testing 🌍
- Secure secrets with .env 🛡


