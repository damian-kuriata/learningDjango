"""
Django settings for learningDjango project.

Generated by 'django-admin startproject' using Django 3.1.3.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.1/ref/settings/
"""
import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
from django.urls import reverse, reverse_lazy
from django.utils.translation import gettext_lazy as _
import django_heroku
import dj_database_url

BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get("DJANGO_SECRET_KEY", "SECRET")

# SECURITY WARNING: don't run with debug turned on in production!
#DEBUG = os.environ.get('DJANGO_DEBUG', '') != 'False'
DEBUG = False
# Application definition

ALLOWED_HOSTS = ["*"]
INSTALLED_APPS = [
    'corsheaders',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'catalog',
    'djangolearn',
    'storages',
    'boto'
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware'
]

ROOT_URLCONF = 'learningDjango.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates']
        ,
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

WSGI_APPLICATION = 'learningDjango.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': "deibbr7o045r51",
        'USER': 'xavzajlciugzjf',
        'PASSWORD': 'dc87d16ecd859877b7140b1e77dfc72b9bba8bfc267d6f7470058f2648db2e7a',
        'HOST': "ec2-54-211-99-192.compute-1.amazonaws.com",
        'PORT': '5432',
        'OPTIONS': {'sslmode': 'require'}
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


# Internationalization
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Europe/Warsaw'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
LOGIN_REDIRECT_URL = reverse_lazy("index")

if DEBUG:
    EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
else:
    EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = "smtp.gmail.com"
EMAIL_PORT = 587
EMAIL_HOST_USER = "damian.kuriata2001@gmail.com"
EMAIL_HOST_PASSWORD = os.environ.get("EMAIL_PASSWORD")
EMAIL_USE_TLS = True
ADMINS = [("Damian", "damian11131@gmail.com")]

MEDIA_ROOT = "C:\\Users\\damia\\PycharmProjects\\learningDjango\\media"
MEDIA_URL = "/uploaded/"

# Custom setting. Restricts the maximum size of uploaded file.
# When exceeded, ValidationError should be raised.
MAX_UPLOAD_SIZE = 16 * 1024 * 1024 #16MB

LOGOUT_REDIRECT_URL = reverse_lazy("login")
LANGUAGES = (
    ("en-us", _("English")),
    ("pl", _("Polish"))
)
LOCALE_PATHS = [
    os.path.join(BASE_DIR, 'locale')
]
LANG_ENGLISH = "en"
LANG_GERMAN = "de"
LANG_FRENCH = "fr"
LANG_SPANISH = "es"
LANG_POLISH = "pl"
LANG_CHOICES = (
    (LANG_ENGLISH, _("English")),
    (LANG_GERMAN, _("German")),
    (LANG_FRENCH, _("French")),
    (LANG_SPANISH, _("Spanish")),
    (LANG_POLISH, _("Polish"))
    )
db_from_env = dj_database_url.config(conn_max_age=500)
DATABASES['default'].update(db_from_env)
'''
if not DEBUG:
   AWS_STORAGE_BUCKET_NAME = os.environ['AWS_STORAGE_BUCKET_NAME']
   AWS_ACCESS_KEY_ID = os.environ['AWS_ACCESS_KEY_ID']
   AWS_SECRET_ACCESS_KEY = os.environ['AWS_SECRET_ACCESS_KEY']
   STATICFILES_STORAGE = 'storages.backends.s3boto.S3BotoStorage'
   S3_URL = 'http://%s.s3.amazonaws.com/' % AWS_STORAGE_BUCKET_NAME
   STATIC_URL = S3_URL
'''
django_heroku.settings(locals())
