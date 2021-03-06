"""
Django settings for yevent project.

Generated by 'django-admin startproject' using Django 1.10.3.

For more information on this file, see
https://docs.djangoproject.com/en/1.10/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.10/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import logging

import dj_database_url

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.10/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = getattr(os.environ, 'SECRET_KEY', 'ohyav@yf+nx1wn-ygmfnmtyd%qf*h=c@6&c_l+sl$fv7babl+*')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.environ.get('ENV', None) != "production"

ALLOWED_HOSTS = ['dev.y.bde-insa-lyon.fr', 'gala.y.bde-insa-lyon.fr', 'yevent', os.environ.get('HOST', 'localhost')]

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_forms_bootstrap',
    'compressor',
    'easy_select2',
    'import_export',
    'django_premailer',
    'anymail',
    'legal',
    'invitation',
    'waitlist'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'yevent.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')]
        ,
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'invitation.context.user_code'
            ]
        },
    },
]


ANYMAIL = {
    # (exact settings here depend on your ESP...)
    "MAILGUN_API_KEY": os.environ.get('MAILGUN_API_KEY', ''),
    "MAILGUN_SENDER_DOMAIN":
        os.environ.get('MAILGUN_SENDER_DOMAIN', 'sandboxfbe8feabbcc44995a1bf0646a5e85a18.mailgun.org'),  # your Mailgun domain, if needed
}

EMAIL_BACKEND = "anymail.backends.mailgun.MailgunBackend"
DEFAULT_FROM_EMAIL = os.environ.get('EMAIL_FROM', 'Gala INSA Lyon (DEV) <gala@bde-insa-lyon.fr>')
SHOP_CHECK_CODE = os.environ.get('SHOP_PASS', 'devpass')

WSGI_APPLICATION = 'yevent.wsgi.application'

PREMAILER_OPTIONS = dict(base_url='http://example.com',
                         remove_classes=False, cssutils_logging_level=logging.ERROR)

# Database
# https://docs.djangoproject.com/en/1.10/ref/settings/#databases

DATABASES = {
    'default': dj_database_url.config(default='sqlite:///{}'.format(os.path.join(BASE_DIR, "db.sqlite3")))
}

# Password validation
# https://docs.djangoproject.com/en/1.10/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/1.10/topics/i18n/

LANGUAGE_CODE = 'fr-fr'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.10/howto/static-files/

STATIC_URL = '/static/'

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static"),
    os.path.join(BASE_DIR, "invitation/static")
]

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'compressor.finders.CompressorFinder',
)

STATIC_ROOT = os.path.join(BASE_DIR, "static_root")

COMPRESS_JS_FILTERS = ['compressor.filters.yuglify.YUglifyJSFilter']
COMPRESS_YUGLIFY_BINARY = 'yuglify'
if os.environ.get('HOST', 'localhost') == 'gala.dev.bde-insa-lyon.fr':
    # Do not compress assets for local dev
    COMPRESS_ENABLED = False
    COMPRESS_OFFLINE = False
else:
    COMPRESS_ENABLED = True
    COMPRESS_OFFLINE = True

GOOGLE_ANALYTICS = os.environ.get('GOOGLE_ANALYTICS', 'UA-71047487-8')
YURPLAN_EVENT_ID = os.environ.get('YURPLAN_EVENT_ID', '1')
YURPLAN_APP_ID = os.environ.get('YURPLAN_APP_ID', '1')
YURPLAN_APP_SECRET = os.environ.get('YURPLAN_APP_SECRET', '1')
