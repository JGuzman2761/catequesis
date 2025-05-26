# urls.py
from django.urls import path
from ..views import (
    GrupoListView, GrupoDetailView,
    GrupoCreateView, GrupoUpdateView,
    GrupoDeleteView,
)

urlpatterns = [
    path('grupo/', GrupoListView.as_view(), name='grupo_list'),
    path('grupo/<int:pk>/', GrupoDetailView.as_view(), name='grupo_detail'),
    path('grupo/crear/', GrupoCreateView.as_view(), name='grupo_create'),
    path('grupo/<int:pk>/editar/', GrupoUpdateView.as_view(), name='grupo_update'),
    path('grupo/<int:pk>/eliminar/', GrupoDeleteView.as_view(), name='grupo_delete'),
]
