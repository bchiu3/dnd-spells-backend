"""
Django settings for dndSpellsBackend project.

Generated by 'django-admin startproject' using Django 5.0.1.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.0/ref/settings/
"""

import os
from pathlib import Path
import mongoengine
from dotenv import load_dotenv

load_dotenv(override=True)

PATH_TO_MONGO_PEM = os.getenv('PATH_TO_MONGO_PEM')
MONGO_HOST_URL = os.getenv('MONGO_HOST_URL')
MONGO_DB_NAME = os.getenv('MONGO_DB_NAME')
MONGO_USERNAME = os.getenv('MONGO_USERNAME')
MONGO_PASSWORD = os.getenv('MONGO_PASSWORD')

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv('DJANGO_SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.getenv('DJANGO_DEBUG') == "True"

if DEBUG:
    ALLOWED_HOSTS = ['localhost', '127.0.0.1']
else:
    ALLOWED_HOSTS = ['.vercel.app', '.now.sh']

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'corsheaders',
    'rest_framework',
    'storages',
    'spells.apps.SpellsConfig',
]

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    'django.middleware.security.SecurityMiddleware',
    "whitenoise.middleware.WhiteNoiseMiddleware",
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'dndSpellsBackend.urls'

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

WSGI_APPLICATION = 'dndSpellsBackend.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases
DATABASE_NAME = os.environ.get("POSTGRES_DATABASE")
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        'USER': os.environ.get("POSTGRES_USER"),
        'PASSWORD': os.environ.get("POSTGRES_PASSWORD"),
        'HOST': os.environ.get("POSTGRES_HOST"),
        'PORT': os.environ.get("POSTGRES_PORT"),
    }
}

if DATABASE_NAME:
    DATABASES['default']['NAME'] = DATABASE_NAME


# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

DEFAULT_FILE_STORAGE = "storages.backends.s3.S3Storage"
AWS_S3_ACCESS_KEY_ID = os.getenv('AWS_S3_ACCESS_KEY_ID')
AWS_S3_SECRET_ACCESS_KEY = os.getenv('AWS_S3_SECRET_ACCESS_KEY')
# AWS_DEFAULT_ACL = 'public-read'
AWS_S3_REGION_NAME = os.getenv('AWS_S3_REGION_NAME')
AWS_STORAGE_BUCKET_NAME = os.getenv('AWS_STORAGE_BUCKET_NAME')
AWS_OBJECT_PARAMETERS = {'CacheControl': 'max-age=86400'}
    
# STATIC_URL = f'https://{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com/static/'
# STATIC_URL = "https://1.bp.blogspot.com/-Yx8sfH4iJ-E/T0NFB_DEhrI/AAAAAAAAskY/iaHoqbb-2Xk/s1600/"
# STATIC_ROOT = os.path.join(
#     BASE_DIR, 'staticfiles', 'static')

# STATICFILES_DIRS = [BASE_DIR/'static',]
STATIC_ROOT = BASE_DIR.parent / "staticfiles" / "static"

# MEDIA_URL = '/media/'

MEDIA_URL = f'https://{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com/media/'

REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
    'PAGE_SIZE': 100
}

WSGI_APPLICATION = 'dndSpellsBackend.wsgi.app'

if DEBUG:
    CORS_ALLOW_ALL_ORIGINS = True
else:
    frontend_urls = os.getenv("FRONTEND_URLS")
    if frontend_urls:
        CORS_ALLOWED_ORIGINS = frontend_urls.split(",")

mongoengine.connect(db=MONGO_DB_NAME, 
                    host=MONGO_HOST_URL, 
                    username=MONGO_USERNAME,
                    password=MONGO_PASSWORD)