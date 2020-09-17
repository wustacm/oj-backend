"""
Django settings for ddl project.

Generated by 'django-admin startproject' using Django 3.0.8.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.0/ref/settings/
"""

import os

import sentry_sdk
from django.utils.translation import gettext_lazy as _
from sentry_sdk.integrations.celery import CeleryIntegration
from sentry_sdk.integrations.django import DjangoIntegration
from sentry_sdk.integrations.redis import RedisIntegration

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv('SECRET_KEY', 'THIS_IS_A_SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DDL_ENV = os.getenv('DDL_ENV', 'development')
DDL_DEBUG = os.getenv('DDL_DEBUG', 'True') == 'True'
if DDL_DEBUG:
    DEBUG = True
else:
    DEBUG = False
ALLOWED_HOSTS = ['*']

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'django_filters',
    'problem.apps.ProblemConfig',
    'user.apps.UserConfig',
    'submission.apps.SubmissionConfig',
    'utils.apps.UtilsConfig',
    'system.apps.SystemConfig'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

]

ROOT_URLCONF = 'ddl.urls'

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
                'django.template.context_processors.i18n'
            ],
        },
    },
]

WSGI_APPLICATION = 'ddl.wsgi.application'

# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('POSTGRES_DB', 'ddl'),
        'USER': os.getenv('POSTGRES_USER', 'user'),
        'PASSWORD': os.getenv('POSTGRES_PASSWORD', 'pass'),
        'HOST': os.getenv('POSTGRES_HOST', '127.0.0.1'),
        'PORT': os.getenv('POSTGRES_PORT', 5432),
    }
}

# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.0/topics/i18n/


LANGUAGE_CODE = 'en'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True
LANGUAGES = (
    ('zh-hans', _('Simplified Chinese')),
    ('en', _('English')),
)
LOCALE_PATHS = (os.path.join(BASE_DIR, 'locale'),)

LANGUAGE_SESSION_KEY = '_language'
LANGUAGE_COOKIE_NAME = '_language'
# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/

STATIC_URL = '/static/'

AUTH_USER_MODEL = 'user.User'
CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': f"redis://{os.getenv('REDIS_HOST', '127.0.0.1')}:{os.getenv('REDIS_PORT', 6379)}/1",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        },
    },
    "session": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": f"redis://{os.getenv('REDIS_HOST', '127.0.0.1')}:{os.getenv('REDIS_PORT', 6379)}/2",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    },
    "page": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": f"redis://{os.getenv('REDIS_HOST', '127.0.0.1')}:{os.getenv('REDIS_PORT', 6379)}/3",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    }
}
SESSION_ENGINE = "django.contrib.sessions.backends.cache"
SESSION_CACHE_ALIAS = "session"
SESSION_COOKIE_AGE = 60 * 60 * 12

# SMTP相关设置
if os.getenv('EMAIL_ENABLE', 'False') == 'True':
    EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
    EMAIL_HOST = os.getenv('EMAIL_HOST', '')
    EMAIL_PORT = os.getenv('EMAIL_PORT', 465)
    EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER', '')
    EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD', '')
    EMAIL_USE_SSL = (EMAIL_PORT == 465)
    DEFAULT_FROM_EMAIL = EMAIL_HOST_USER
else:
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
# 验证码的有效时间（秒）
CAPTCHA_AGE = 60 * 5
# 缓存页面的时间
PAGE_CACHE_AGE = 10
# 验证邮箱的有效时间
ACTIVATE_CODE_AGE = 10 * 60

if os.getenv('SENTRY_ENABLE', 'False') == 'True':
    sentry_sdk.init(
        dsn="https://03eb7f0b0aaf4a31b548639bea76c910@o428533.ingest.sentry.io/5374065",
        integrations=[DjangoIntegration(), CeleryIntegration(), RedisIntegration()],
        # If you wish to associate users to errors (assuming you are using
        # django.contrib.auth) you may enable sending PII data.
        send_default_pii=True
    )
# celery 配置
CELERY_BROKER_URL = f"amqp://{os.getenv('RABBITMQ_USER', 'guest')}:{os.getenv('RABBITMQ_PASS', 'guest')}" \
                    f"@{os.getenv('RABBITMQ_HOST', '127.0.0.1')}:{os.getenv('RABBITMQ_PORT', 5672)}/"
CELERY_BROKER_SERIALIZER = 'json'

REST_FRAMEWORK = {
    'EXCEPTION_HANDLER': 'utils.exception.custom_exception_handler',
    'DEFAULT_PAGINATION_CLASS': 'utils.pagination.CustomPagination',
    'DEFAULT_FILTER_BACKENDS': ['django_filters.rest_framework.DjangoFilterBackend'],
    'DEFAULT_PARSER_CLASSES': [
        'rest_framework.parsers.JSONParser',
        'rest_framework.parsers.MultiPartParser',
    ]
}

if DDL_ENV != 'production':
    DATA_DIR = os.path.join(BASE_DIR, 'data')
    TMP_DIR = os.path.join(DATA_DIR, 'tmp')
else:
    DATA_DIR = '/data'
    TMP_DIR = '/tmp'

PROBLEM_IMAGE_DIR = os.path.join(DATA_DIR, 'image')
PROBLEM_PDF_DIR = os.path.join(DATA_DIR, 'pdf')
PROBLEM_TEST_CASES_DIR = os.path.join(DATA_DIR, 'test_cases')
X_FRAME_OPTIONS = 'SAMEORIGIN'

JUDGE_TOKEN = os.getenv('JUDGE_TOKEN', 'JUDGE_TOKEN')
