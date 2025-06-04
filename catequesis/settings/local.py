from .base import *

DEBUG = True

ALLOWED_HOSTS = ['*']


# Base de datos para desarrollo (utiliza SQLite por simplicidad)

DATABASES['default'] = {
    'ENGINE': 'django.db.backends.sqlite3',
    'NAME': BASE_DIR / 'db.sqlite3',
    }   