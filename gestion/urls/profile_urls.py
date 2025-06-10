# gestion/urls/profile_urls.py
from django.urls import path
from gestion.views import profile_views

urlpatterns = [
    path('profile/edit/', profile_views.profile_update_view, name='profile_update'),
    # path('profile/', profile_views.profile_detail_view, name='profile_detail'), # URL para detalle del perfil si se implementa
]