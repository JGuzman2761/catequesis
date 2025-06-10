"""
ASGI config for catequesis project.
It exposes the ASGI callable as a module-level variable named ``application``.
For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/asgi/
"""
import os
from django.core.asgi import get_asgi_application

# Determinar el entorno basado en una variable de entorno
django_env = os.environ.get('DJANGO_ENV', 'local')

if django_env == 'production':
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'catequesis.settings_production')
else:
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'catequesis.settings_local')

application = get_asgi_application()