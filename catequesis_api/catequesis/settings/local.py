from .base import *

# Configuraciones específicas para el entorno local
DEBUG = True
ALLOWED_HOSTS = ['localhost', '127.0.0.1']

# Base de datos para desarrollo (utiliza SQLite por simplicidad)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Configuración de archivos estáticos y media para el entorno local
STATIC_URL = '/static/'
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'