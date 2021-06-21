"""
Django settings for backend project.

Generated by 'django-admin startproject' using Django 3.1.3.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.1/ref/settings/
"""
from pathlib import Path
import os, sys
from datetime import timedelta
import django_heroku


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'by@m!qdo1!hyzx75$zuyp-#*-#09958x1@4x!bbv6icjw*+w=0'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# Application definition

INSTALLED_APPS = [
    
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'djoser',
    'rest_framework.authtoken',
    'django_filters',
    'psycopg2',
    'users',
    'corsheaders',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'corsheaders.middleware.CorsMiddleware',
]

ROOT_URLCONF = 'backend.urls'

#DATETIME_FORMAT = 'N j, Y, P'

ALLOWED_HOSTS=['*']
CORS_ORIGIN_ALLOW_ALL = True

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'templates'),
        ],
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

WSGI_APPLICATION = 'backend.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

DATABASES = {
    'default': {
        #'ENGINE': 'django.db.backends.postgresql_psycopg2',
        #'NAME': 'proj_db',
        #'USER' : 'postgres',
        #'PASSWORD' : 'password',
        #'HOST' : 'localhost',
        #'PORT': '5432',
        'ENGINE': 'django.db.backends.sqlite3',
                'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),

    }
}


# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

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

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES' : (
            'rest_framework.authentication.TokenAuthentication',
            'rest_framework_simplejwt.authentication.JWTAuthentication',
        ),
    'DEFAULT_FILTER_BACKENDS' : (
            'django_filters.rest_framework.DjangoFilterBackend',
        ), 
}

DJOSER = {
    'PASSWORD_RESET_CONFIRM_URL' : '#/password/reset/confirm/{uid}/{token}',
    #'USERNAME_RESET_CONFIRM_URL' : '#/username/reset/confirm/{uid}/{token}',
    'ACTIVATION_URL' : 'api/v1/activate/{uid}/{token}',
    'SEND_ACTIVATION_EMAIL' : True,
    'LOGIN_FIELD' : 'email',
    'SERIALIZERS' : {
        'current_user' : 'users.serializers.DetailUserSerializer',
        'user' : 'users.serializers.PartialUserSerializer',
    },
    'HIDE_USERS': False,
    'PERMISSIONS': {
        'user': ['rest_framework.permissions.AllowAny'],
    }
}

AUTH_USER_MODEL = 'users.Account'

EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'mailbot.maxim@gmail.com'
EMAIL_HOST_PASSWORD = 'B1234f_1'
EMAIL_PORT = 587

'''
MAILCHIMP_API_KEY = "d734e120952f5ff05372be27b9cbccfd-us1"
MAILCHIMP_DATA_CENTER = "us1"
MAILCHIMP_EMAIL_LIST_ID = "582e337829"
'''



SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME' : timedelta(minutes=5),
    'REFRESH_TOKEN_LIFETIME' : timedelta(days=1),
    'ROTATE_REFRESH_TOKENS' : False,
    'BLACKLIST_AFTER_ROTATION' : True,

    'ALGHORITHM' : 'HS256',
    'SIGNING_KEY' : SECRET_KEY,
    'VERIFYING_KEY' : None,
    'AUDIENCE' : None,
    'ISSUER' : None,

    'AUTH_HEADER_TYPES' : ('Bearer',),
    'USER_ID_FIELD' : 'id',
    'USER_ID_CLAIM' : 'user_id',

    'AUTH_TOKEN_CLASSES' : ('rest_framework_simplejwt.tokens.AccessToken'),
    'TOKEN_TYPE_CLAIM' : 'token_type',

    'JTI_CLAIM' : 'jti',

    'SLIDING_TOKEN_REFRESH_EXP_CLAIM' : 'refresh_exp',
    'SLIDING_TOKEN_LIFETIME' : timedelta(minutes=5),
    'SLIDING_TOKEN_REFRESH_LIFETIME' : timedelta(days=1),
}



# Internationalization
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

django_heroku.settings(locals())