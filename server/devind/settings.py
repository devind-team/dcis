"""
Django settings for devind project.

Generated by 'django-admin startproject' using Django 3.1.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.1/ref/settings/
"""

import os
from pathlib import Path

import sentry_sdk
from dotenv import load_dotenv
from sentry_sdk.integrations.django import DjangoIntegration


# Настройки базовой директории приложения
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve(strict=True).parent.parent


# Настройки окружения
ENV_PATH = BASE_DIR / '.env'
load_dotenv(dotenv_path=ENV_PATH)


# Вспомогательные настройки
# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv('SECRET_KEY', None)
assert SECRET_KEY, 'Не установлен SECRET_KEY в переменную окружения.'
# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.getenv('DEBUG', 'True') == 'True'

DATA_UPLOAD_MAX_MEMORY_SIZE = 250000000
AUTH_USER_MODEL = 'core.User'
ROOT_URLCONF = 'devind.urls'
WSGI_APPLICATION = 'devind.wsgi.application'
ASGI_APPLICATION = 'devind.asgi.application'


# Список установленных приложений
INSTALLED_APPS = [
    'channels',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.staticfiles',
    'django.contrib.postgres',
    'rest_framework',
    'graphene_django',
    'oauth2_provider',
    'corsheaders',
    'django_filters',
    'django_celery_results',
    'django_celery_beat',
    'django_seed',
    'devind_core',
    'devind_notifications',
    'devind_dictionaries',
    'apps.core',
    'apps.dashboard',
    'apps.dcis',
    'push_notifications',
    'drf_yasg',
    'auditlog',
]


# Список middleware
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.middleware.common.CommonMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'apps.dcis.middleware.ExternalTokenMiddleware',
    'oauth2_provider.middleware.OAuth2TokenMiddleware',
    'devind_core.middleware.SessionMiddleware',
    'devind_core.middleware.TimeRequestMiddleware',
    'devind_core.middleware.LangRequestMiddleware',
    'auditlog.middleware.AuditlogMiddleware',
]

# Список шаблонов
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
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


# Список бэкендов аутентификации
AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'oauth2_provider.backends.OAuth2Backend',
)


# Настройки базы данных
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'HOST': os.getenv('DB_APP_HOST', 'db_app'),
        'PORT': os.getenv('DB_APP_PORT', '5432'),
        'NAME': os.getenv('DB_APP_NAME', 'collect'),
        'USER': os.getenv('DB_APP_USER', 'postgres'),
        'PASSWORD': os.getenv('DB_APP_PASSWORD', '1234'),
    }
}

DEFAULT_AUTO_FIELD = 'django.db.models.AutoField'

# Настройки Cors
ALLOWED_HOSTS = ['*']
CORS_ORIGIN_ALLOW_ALL = True
CORS_ALLOW_CREDENTIALS = True
CORS_ORIGIN_WHITELIST = ['http://localhost:3000', 'http://localhost:8000']
CORS_ORIGIN_REGEX_WHITELIST = ['http://localhost:3000', 'http://localhost:8000']


# Настройки OAuth2
OAUTH2_PROVIDER = {
    'SCOPES': {'read': 'Read scope', 'write': 'Write scope', 'groups': 'Access to your groups'},
    'OAUTH2_BACKEND_CLASS': 'oauth2_provider.oauth2_backends.JSONOAuthLibCore'
}
OAUTH2_PROVIDER_ACCESS_TOKEN_MODEL = 'oauth2_provider.AccessToken'


# Настройки Graphene
GRAPHENE = {
    'SCHEMA': 'devind.schema.schema',
    'MIDDLEWARE': [
        'graphene_django.debug.DjangoDebugMiddleware',
    ],
}

# Настройка канальных слоев
CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            'hosts': [(os.getenv('REDIS_SERVER', 'localhost'), 6379)],
        },
    },
}


# Настройки Sentry
SENTRY_DNS: str or None = os.getenv('SENTRY_DNS', None)
if SENTRY_DNS:
    sentry_sdk.init(dsn=SENTRY_DNS, integrations=[DjangoIntegration()], traces_sample_rate=1., send_default_pii=True)


# Настройки Email
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = os.getenv('EMAIL_HOST', 'smtp.google.com')
EMAIL_USE_TLS = True
EMAIL_USE_SSL = False
EMAIL_PORT = 587
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD')


# Настройки Celery
CELERY_BROKER_URL = os.getenv('BROKER_URL')
CELERY_RESULT_BACKEND = os.getenv('BROKER_BACKEND')
CELERY_TASK_SERIALIZER = os.getenv('TASK_SERIALIZER', 'json')
CELERY_RESULT_SERIALIZER = os.getenv('RESULT_SERIALIZER', 'json')
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TIMEZONE = 'Europe/Moscow'
CELERY_ENABLE_UTC = True
CELERY_RESULT_EXPIRES = None


CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': os.getenv('CACHE_LOCATION'),
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        }
    }
}


# Настройки интернационализации
# https://docs.djangoproject.com/en/3.1/topics/i18n/
LANGUAGE_CODE = 'ru'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True


# Настройки проверки паролей
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]


# Настройки статических файлов
# https://docs.djangoproject.com/en/3.1/howto/static-files/
STATIC_URL = '/static/'
STATICFILES_DIRS = [
    BASE_DIR / 'dist',
    BASE_DIR / 'storage',
    BASE_DIR.parent / '.nuxt',
]


# Настройки вспомогательных директорий
USERS_DIR = BASE_DIR / 'storage' / 'user_files'
DOCUMENTS_DIR = BASE_DIR / 'storage' / 'documents'
if not DOCUMENTS_DIR.exists():
    os.makedirs(DOCUMENTS_DIR)
TEMP_FILES_DIR = BASE_DIR / 'storage' / 'temp_files'
if not TEMP_FILES_DIR.exists():
    os.makedirs(TEMP_FILES_DIR)


# Количество страниц, выгружаемое по умолчанию
DEFAULT_PAGE_SIZE = 12


DEVIND_CORE_USER_TYPE = 'apps.core.schema.UserType'
DEVIND_NOTIFICATION_NOTICE_INTERFACE = 'apps.notifications.schema.NoticeInterface'


EXTERNAL_URLS = {
    'cbias': 'https://cbias.ru/sso_app/remote_auth.spf?uid=%s&ris=61',
}

SSH_CONNECT = {
    'HOST': os.getenv('SSH_HOST'),
    'PORT': os.getenv('SSH_PORT'),
    'USERNAME': os.getenv('SSH_USER'),
    'PASSWORD': os.getenv('SSH_PASSWORD'),
    'DB_NAME': os.getenv('SSH_DB_NAME'),
}

EXTERNAL_TOKEN: str | None = os.getenv('EXTERNAL_TOKEN', None)
