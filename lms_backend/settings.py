"""
Django settings for lms_backend project.
"""

from pathlib import Path
from datetime import timedelta
import os
from decouple import config

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config('SECRET_KEY', default='django-insecure-your-secret-key-here-change-in-production')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config('DEBUG', default=True, cast=bool)

ALLOWED_HOSTS = [
    'localhost',
    '127.0.0.1',
    'pheedev.pythonanywhere.com',
    '.pythonanywhere.com',
    'algaddaftechhub.vercel.app',
    'algaddaftechnologyhub.com',
    'athub-beige.vercel.app'
]

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'rest_framework_simplejwt',
    'corsheaders',
    'authentication',
    'courses',
    'blog',
    'contacts',
    'management',
    'support',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
]

ROOT_URLCONF = 'lms_backend.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'lms_backend.wsgi.application'

# Database — selected by env with no code change.
# If MYSQL_DATABASE is set → MySQL (utf8mb4, strict mode); otherwise → SQLite.
# Keep local .env on SQLite (leave MYSQL_* unset) and set MYSQL_* only on the server.
if config('MYSQL_DATABASE', default=''):
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': config('MYSQL_DATABASE'),
            'USER': config('MYSQL_USER', default=''),
            'PASSWORD': config('MYSQL_PASSWORD', default=''),
            'HOST': config('MYSQL_HOST', default='localhost'),
            'PORT': config('MYSQL_PORT', default='3306'),
            'OPTIONS': {
                'charset': 'utf8mb4',
                'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
            },
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        'OPTIONS': {'min_length': 12},
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Custom User Model
AUTH_USER_MODEL = 'authentication.User'

# Django REST Framework
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
    ],
    'DEFAULT_THROTTLE_CLASSES': [
        'rest_framework.throttling.AnonRateThrottle',
        'rest_framework.throttling.UserRateThrottle',
    ],
    'DEFAULT_THROTTLE_RATES': {
        'anon': '60/minute',
        'user': '300/minute',
        'login': '5/minute',
        'register': '3/minute',
        'otp_verify': '5/minute',
        'otp_resend': '3/hour',
        'support_chat': '15/minute',
        'support_contact': '5/hour',
    },
}

# JWT Settings
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=60),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,
    'UPDATE_LAST_LOGIN': True,
    'ALGORITHM': 'HS256',
    'SIGNING_KEY': SECRET_KEY,
    'VERIFYING_KEY': None,
    'AUDIENCE': None,
    'ISSUER': None,
    'JWK_URL': None,
    'LEEWAY': 0,
    'AUTH_HEADER_TYPES': ('Bearer',),
    'AUTH_HEADER_NAME': 'HTTP_AUTHORIZATION',
    'USER_ID_FIELD': 'id',
    'USER_ID_CLAIM': 'user_id',
    'USER_AUTHENTICATION_RULE': 'rest_framework_simplejwt.authentication.default_user_authentication_rule',
    'AUTH_TOKEN_CLASSES': ('rest_framework_simplejwt.tokens.AccessToken',),
    'TOKEN_TYPE_CLAIM': 'token_type',
    'JTI_CLAIM': 'jti',
    'SLIDING_TOKEN_REFRESH_EXP_CLAIM': 'refresh_exp',
    'SLIDING_TOKEN_LIFETIME': timedelta(minutes=5),
    'SLIDING_TOKEN_REFRESH_LIFETIME': timedelta(days=1),
}

# CORS Settings
CORS_ALLOWED_ORIGINS = [
    "http://localhost:5173",  # Vite default port
    "http://127.0.0.1:5173",
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "https://algaddaftechnologyhub.com",  # Your Vercel domain
    "https://algaddaftechhub.vercel.app",
    "https://athub-beige.vercel.app",
]

CORS_ALLOW_CREDENTIALS = True

CORS_ALLOW_ALL_ORIGINS = False  # Never reflect arbitrary origins, even in development

# Email Configuration
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = config('EMAIL_HOST_USER', default='lemuelemmanuel29@gmail.com')
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD', default='rpdceoywlbcxddoy')
DEFAULT_FROM_EMAIL = config('DEFAULT_FROM_EMAIL', default='lemuelemmanuel29@gmail.com')

# Flutterwave Configuration
FLUTTERWAVE_PUBLIC_KEY = config('FLUTTERWAVE_PUBLIC_KEY', default='')
FLUTTERWAVE_SECRET_KEY = config('FLUTTERWAVE_SECRET_KEY', default='')
FLUTTERWAVE_ENCRYPTION_KEY = config('FLUTTERWAVE_ENCRYPTION_KEY', default='')

# Frontend URL for payment redirects
FRONTEND_URL = config('FRONTEND_URL', default='http://localhost:3000')

# ── Support AI chat ──────────────────────────────────────────────────────────
# OpenAI-chat-compatible provider (Groq by default). Key stays server-side;
# if empty the chat endpoint returns 503 and the widget offers the contact form.
SUPPORT_AI_API_KEY = config('SUPPORT_AI_API_KEY', default='')
SUPPORT_AI_API_URL = config('SUPPORT_AI_API_URL',
                            default='https://api.groq.com/openai/v1/chat/completions')
SUPPORT_AI_MODEL = config('SUPPORT_AI_MODEL', default='llama-3.3-70b-versatile')

# ── Admin handoff alerts ─────────────────────────────────────────────────────
# Comma-separated recipient list; if empty, active superusers are alerted.
ADMIN_ALERT_EMAILS = [e.strip() for e in config('ADMIN_ALERT_EMAILS', default='').split(',') if e.strip()]
# Used to build the admin change-URL inside alert emails.
BASE_URL = config('BASE_URL', default='http://localhost:8000')

# WhiteNoise Configuration
# STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Serve media files with WhiteNoise
# WHITENOISE_USE_FINDERS = True
# WHITENOISE_AUTOREFRESH = True



