from django.urls import path
from ..views.catequista_views import (
    CatequistaListView, CatequistaCreateView,CatequistaDetailView,
    CatequistaUpdateView, CatequistaDeleteView
)

urlpatterns = [
    path('catequistas/', CatequistaListView.as_view(), name='catequista_list'),
    path('catequistas/crear/', CatequistaCreateView.as_view(), name='catequista_create'),
    path('catequistas/editar/<int:pk>/', CatequistaUpdateView.as_view(), name='catequista_update'),
    path('catequistas/<int:pk>/', CatequistaDetailView.as_view(), name='catequista_detail'),
    path('catequistas/eliminar/<int:pk>/', CatequistaDeleteView.as_view(), name='catequista_delete'),
]