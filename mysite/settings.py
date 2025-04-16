"""
Django settings for mysite project.

Generated by 'django-admin startproject' using Django 5.1.7.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.1/ref/settings/
"""
import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-%e0=45c$rp9c=)!v!28r-m-qz_tvh_9f4lmss%-xv+6c3r7a-$"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ["localhost", "127.0.0.1", ".pythonanywhere.com"]


# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "celery",
    "blog",
    "disc",
    "base",
    "customer",
    "taskManager",
    "rest_framework",  # Django REST Framework
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    
]

ROOT_URLCONF = "mysite.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "mysite.wsgi.application"


# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "Asia/Calcutta"

USE_I18N = True

USE_TZ = True

#--------------------------------------------------
# Celery Settings
#---------------------------------------------------
BROKER_URL = "redis://localhost:6379/0"
CELERY_BROKER_URL = "redis://localhost:6379/0"
CELERY_RESULT_BACKEND = "redis://localhost:6379/0"
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = "Asia/Kolkata"


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = "static/"

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# from .celery_routes import CELERY_REGULAR_ROUTES
# from .celery_routes import CELERYBEAT_SCHEDULE

log_level = "DEBUG"

# List of apps
APPS = ["taskManager","description"]

# Ensure logs directory exists
logs_dir = os.path.join(BASE_DIR, "logs")
print(logs_dir,"----------------------------------------------------")
os.makedirs(logs_dir, exist_ok=True)

# Create directories for each app
for directory in APPS:
    dir_path = os.path.join(logs_dir, directory)
    if not os.path.exists(dir_path):
        os.makedirs(dir_path, exist_ok=True)
        print(f"Log directory {dir_path} not found, creating now...")
    else:
        pass

# Logging formatters
FORMATTERS = {
    "verbose": {
        "format": '{"level": "%(levelname)s", "message": "%(message)s", "time": "%(asctime)s", "function": "%(funcName)s", "correlation_id": "%(correlation_id)s"}'
    },
}

# Dynamic handlers and loggers
HANDLERS = {
    "console": {
        "level": "INFO",
        "class": "logging.StreamHandler",
    },
}
LOGGERS = {}

for app in APPS:
    handler_name = f"{app}_handler"
    log_file = os.path.join(logs_dir, app, f"{app}.log")

    HANDLERS[handler_name] = {
        "level": log_level,
        "class": "logging.handlers.TimedRotatingFileHandler",
        "filename": log_file,
        "when": "midnight",
        "interval": 1,
        "backupCount": 2,
        "formatter": "verbose",
        "filters": ["correlation_id"],
    }
 
    LOGGERS[app] = {
        "handlers": [handler_name, "console"],
        "level": log_level,
        "propagate": False,  # Prevents logs from being duplicated
    }
 
# Logging configuration
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": FORMATTERS,
    "handlers": HANDLERS,
    "loggers": LOGGERS,
    "filters": {
        "correlation_id": {"()": "django_guid.log_filters.CorrelationId"},
    },
}