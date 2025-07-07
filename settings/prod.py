from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

STATIC_ROOT = BASE_DIR / 'staticfiles'

ALLOWED_HOSTS = ['137.184.221.100']

# Database
# https://docs.djangoproject.com/en/5.2/ref/settings/#databases

# settings.py
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": "game_browser_prod_db",
        'USER': "django",
        'PASSWORD': "franco123",
        'HOST': "localhost",
        'PORT': '3306'
    }
}