from .base import *

DEBUG = False

ALLOWED_HOSTS = ['*']

# Base de datos para producción (ejemplo con PostgreSQL)
DATABASES['default'] = {
    'ENGINE': 'django.db.backends.postgresql',
    'NAME': os.getenv('POSTGRES_DB'),
    'USER': os.getenv('POSTGRES_USER'),
    'PASSWORD': os.getenv('POSTGRES_PASSWORD'),
    'HOST': os.getenv('POSTGRES_HOST', 'localhost'),
    'PORT': os.getenv('POSTGRES_PORT', '5432'),
}
