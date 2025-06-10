from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('gestion.api_urls')),  # Incluyendo las URLs de la aplicación gestion
]

