from django.urls import path
from ..views.estudiante_views import (
    EstudianteListView, EstudianteDetailView,
    EstudianteCreateView, EstudianteUpdateView, EstudianteDeleteView
)

urlpatterns = [
    path('estudiantes/', EstudianteListView.as_view(), name='estudiante_list'),
    path('estudiantes/<int:pk>/', EstudianteDetailView.as_view(), name='estudiante_detail'),
    path('estudiantes/crear/', EstudianteCreateView.as_view(), name='estudiante_create'),
    path('estudiantes/<int:pk>/editar/', EstudianteUpdateView.as_view(), name='estudiante_update'),
    path('estudiantes/<int:pk>/eliminar/', EstudianteDeleteView.as_view(), name='estudiante_delete'),
]