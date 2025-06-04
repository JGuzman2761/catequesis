# gestion/urls.py
from django.urls import path, reverse_lazy, reverse
from ..views import ( InscripcionListView, InscripcionDetailView, InscripcionCreateView, InscripcionUpdateView, InscripcionDeleteView, InscripcionGrupoCardListView )

from ..views import (
    InscripcionListView,
    InscripcionDetailView,
    InscripcionCreateView,
    InscripcionUpdateView,
    InscripcionDeleteView,
    InscripcionGrupoCardListView,
)

urlpatterns = [
    # Lista de grupos (tarjetas)
    path('inscripciones/', InscripcionGrupoCardListView.as_view(), name='inscripcion_card_list'),

    # Lista de inscripciones para un grupo
    path('inscripciones/grupo/<int:grupo_id>/', InscripcionListView.as_view(), name='inscripcion_list'),

    # Crear inscripción para un grupo
    path('inscripciones/grupo/<int:grupo_id>/crear/', InscripcionCreateView.as_view(), name='inscripcion_create'),

    # Detalle de una inscripción
    path('inscripciones/grupo/<int:grupo_id>/detalle/<int:pk>/', InscripcionDetailView.as_view(), name='inscripcion_detail'),


    # Editar inscripción: se requiere grupo_id y pk
    path('inscripciones/grupo/<int:grupo_id>/editar/<int:pk>/', InscripcionUpdateView.as_view(), name='inscripcion_update'),
   
    # Eliminar inscripción: se requiere grupo_id y pk
    path('inscripciones/grupo/<int:grupo_id>/eliminar/<int:pk>/', InscripcionDeleteView.as_view(), name='inscripcion_delete'),
    
]
