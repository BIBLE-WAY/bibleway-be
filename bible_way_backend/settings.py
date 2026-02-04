from pathlib import Path
import os
from dotenv import load_dotenv
from datetime import timedelta
import dj_database_url

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.getenv('SECRET_KEY')
if not SECRET_KEY:
    raise ValueError("SECRET_KEY environment variable is required")

DEBUG = os.getenv('DEBUG', 'False') == 'True'
ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', 'localhost,127.0.0.1').split(',')

DATA_UPLOAD_MAX_MEMORY_SIZE = 524288000
DATA_UPLOAD_MAX_NUMBER_FIELDS = 10000
FILE_UPLOAD_MAX_MEMORY_SIZE = 524288000

INSTALLED_APPS = [
    'daphne',
    'channels',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'corsheaders',
    'storages',
    'bible_way',
    'project_notifications',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'bible_way.middleware.DisableCSRFForAPI',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

CORS_ALLOW_ALL_ORIGINS = False
CORS_ALLOW_CREDENTIALS = True
CORS_ALLOWED_ORIGINS = os.getenv('CORS_ALLOWED_ORIGINS', 'http://localhost:5173').split(',')
CORS_ALLOW_METHODS = ['DELETE', 'GET', 'OPTIONS', 'PATCH', 'POST', 'PUT']
CORS_ALLOW_HEADERS = [
    'accept', 'accept-encoding', 'accept-language', 'authorization',
    'content-type', 'content-length', 'dnt', 'origin', 'referer',
    'user-agent', 'x-csrftoken', 'x-requested-with', 'x-forwarded-for',
    'x-forwarded-proto', 'cache-control', 'pragma', 'sec-ch-ua',
    'sec-ch-ua-mobile', 'sec-ch-ua-platform',
]
CORS_EXPOSE_HEADERS = ['content-type', 'authorization', 'x-csrftoken']
CORS_PREFLIGHT_MAX_AGE = 3600

CSRF_TRUSTED_ORIGINS = os.getenv('CSRF_TRUSTED_ORIGINS', 'http://localhost:5173').split(',')
CSRF_COOKIE_SECURE = not DEBUG
CSRF_COOKIE_SAMESITE = 'Lax' if DEBUG else 'None'
CSRF_USE_SESSIONS = False

ROOT_URLCONF = 'bible_way_backend.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'bible_way_backend.wsgi.application'
ASGI_APPLICATION = 'bible_way_backend.asgi.application'

DATABASES = {
    'default': dj_database_url.config(
        default='sqlite:///db.sqlite3',
        conn_max_age=600,
        conn_health_checks=True,
    )
}

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
AUTH_USER_MODEL = 'bible_way.User'

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
    ],
}

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(hours=7),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),
    'USER_ID_FIELD': 'user_id',
    'USER_ID_CLAIM': 'user_id',
    'AUTH_TOKEN_CLASSES': ('rest_framework_simplejwt.tokens.AccessToken',),
    'TOKEN_TYPE_CLAIM': 'token_type',
}

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Asia/Kolkata'
USE_I18N = True
USE_TZ = True

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID', '')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY', '')
AWS_STORAGE_BUCKET_NAME = os.getenv('AWS_STORAGE_BUCKET_NAME', '')
AWS_S3_REGION_NAME = os.getenv('AWS_S3_REGION_NAME', 'auto')
AWS_S3_ENDPOINT_URL = os.getenv('AWS_S3_ENDPOINT_URL', '')
AWS_S3_SIGNATURE_VERSION = 's3v4'
AWS_DEFAULT_ACL = 'public-read'

ZEPTOMAIL_API_TOKEN = os.getenv('ZEPTOMAIL_API_TOKEN', '')
ZEPTOMAIL_FROM_EMAIL = os.getenv('ZEPTOMAIL_FROM_EMAIL', 'noreply@bibleway.io')
ZEPTOMAIL_OTP_EXPIRY_MINUTES = int(os.getenv('ZEPTOMAIL_OTP_EXPIRY_MINUTES', '15'))

USE_REDIS = os.getenv('USE_REDIS', 'false').lower() == 'true'
REDIS_URL = os.getenv('REDIS_URL', 'redis://127.0.0.1:6379')

if USE_REDIS:
    CHANNEL_LAYERS = {
        "default": {
            "BACKEND": "channels_redis.core.RedisChannelLayer",
            "CONFIG": {"hosts": [REDIS_URL]},
        },
    }
else:
    CHANNEL_LAYERS = {
        "default": {"BACKEND": "channels.layers.InMemoryChannelLayer"},
    }

ELASTICSEARCH_HOST = os.getenv('ELASTICSEARCH_HOST', 'localhost')
ELASTICSEARCH_PORT = int(os.getenv('ELASTICSEARCH_PORT', '9200'))
ELASTICSEARCH_USE_SSL = os.getenv('ELASTICSEARCH_USE_SSL', 'false').lower() == 'true'
ELASTICSEARCH_VERIFY_CERTS = os.getenv('ELASTICSEARCH_VERIFY_CERTS', 'true').lower() == 'true'
ELASTICSEARCH_USERNAME = os.getenv('ELASTICSEARCH_USERNAME', '')
ELASTICSEARCH_PASSWORD = os.getenv('ELASTICSEARCH_PASSWORD', '')
ELASTICSEARCH_INDEX_NAME = os.getenv('ELASTICSEARCH_INDEX_NAME', 'chapters_index')

GOOGLE_CLIENT_ID = os.getenv('GOOGLE_CLIENT_ID', '')
