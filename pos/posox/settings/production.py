import os

from .base import *

DEBUG = False

ALLOWED_HOSTS = os.environ.get("DJANGO_ALLOWED_HOSTS", "localhost").split()


# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases

BASE_URL = os.environ.get("BASE_URL", "change me")

DATABASES = {
    'default': {
        "ENGINE": os.environ.get("SQL_ENGINE", "django.db.backends.sqlite3"),
        "NAME": os.environ.get("SQL_DATABASE", os.path.join(BASE_DIR)),
        "USER": os.environ.get("SQL_USER", "pos_user"),
        "PASSWORD": os.environ.get("SQL_PASSWORD", "pos_pass"),
        "HOST": os.environ.get("SQL_HOST", "posdb"),
        "PORT": os.environ.get("SQL_PORT", "5432"),
    }
}