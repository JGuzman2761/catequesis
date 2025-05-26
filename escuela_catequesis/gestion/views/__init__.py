import importlib
from django.conf import settings

ENABLED_VIEWS = getattr(settings, 'ENABLED_VIEWS', None)

view_files = [
    'catequista_views',
    'ciclo_views',
    'curso_views',
    'cursoAnual_views',
    'estudiante_views',
    'grupo_views',
    'inscripcion_views',
    'padre_views',
    'padrino_views',
    'parroquia_views',
]

if ENABLED_VIEWS is None:
    for view_file in view_files:
        module = importlib.import_module(f'.{view_file}', __package__)
        globals().update(module.__dict__)
else:
    for view_file in ENABLED_VIEWS:
        module = importlib.import_module(f'.{view_file}', __package__)
        globals().update(module.__dict__)
