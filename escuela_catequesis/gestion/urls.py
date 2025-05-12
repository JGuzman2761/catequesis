from django.urls import path, include

# Importar las urlpatterns individuales de cada archivo
from gestion.urls.home_urls import urlpatterns as home_urls
from gestion.urls.curso_urls import urlpatterns as curso_urls
from gestion.urls.grupo_urls import urlpatterns as grupo_urls
from gestion.urls.estudiante_urls import urlpatterns as estudiante_urls
from gestion.urls.catequista_urls import urlpatterns as catequista_urls
from gestion.urls.padre_urls import urlpatterns as padre_urls
from gestion.urls.padrino_urls import urlpatterns as padrino_urls
from gestion.urls.inscripcion_urls import urlpatterns as inscripcion_urls
from gestion.urls.parroquia_urls import urlpatterns as parroquia_urls

# Unir todas las rutas en una sola lista
urlpatterns = []
urlpatterns += home_urls
urlpatterns += curso_urls
urlpatterns += grupo_urls
urlpatterns += estudiante_urls
urlpatterns += catequista_urls
urlpatterns += padre_urls
urlpatterns += padrino_urls
urlpatterns += inscripcion_urls
urlpatterns += parroquia_urls
