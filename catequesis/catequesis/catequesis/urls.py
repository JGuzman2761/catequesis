from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from gestion.views.home_view import home_view


urlpatterns = [
    path('', home_view, name='home'),
    path('home/', home_view, name='home'),
    path('admin/', admin.site.urls),
    path('ciclo/', include('gestion.urls.ciclo_urls')),
    path('curso/', include('gestion.urls.curso_urls')),
    path('cursoanual/', include('gestion.urls.cursoanual_urls')),
    path('grupo/', include('gestion.urls.grupo_urls')),
    path('inscripcion/', include('gestion.urls.inscripcion_urls')),
    path('estudiante/', include('gestion.urls.estudiante_urls')),
    path('catequista/', include('gestion.urls.catequista_urls')),
    path('parroquia/', include('gestion.urls.parroquia_urls')),
    path('padre/', include('gestion.urls.padre_urls')),
    path('padrino/', include('gestion.urls.padrino_urls')),
]

# Agregar rutas para servir archivos media en desarrollo
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
