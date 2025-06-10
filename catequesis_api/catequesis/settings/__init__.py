import os
from dotenv import load_dotenv

# Cargar variables de entorno desde el archivo .env
load_dotenv()

# Determinar el entorno basado en una variable de entorno
django_env = os.environ.get('DJANGO_ENV', 'local')

if django_env == 'production':
    from .production import *
else:
    from .local import *