# gestion/urls.py
from django.urls import path, reverse_lazy
from ..views.inscripcion_views import CursoListView, EstudiantesPorCursoView,InscripcionCreateView,InscripcionUpdateView,InscripcionDeleteView

urlpatterns = [
    # Lista de cursos disponibles
    path('inscripciones/', CursoListView.as_view(), name='lista_cursos'),
    # lista estudiantes inscritos
    path('inscripciones/<int:pk>/estudiantes/', EstudiantesPorCursoView.as_view(),                          name='lista_inscritos'),
    # Inscribir nuevos estudiantes
    path('inscripciones/<int:pk>/nueva/', InscripcionCreateView.as_view(), name='nueva_inscripcion'),
    # Editar estudiantes inscritos
    path('inscripciones/<int:pk>/editar/', InscripcionUpdateView.as_view(), name='editar_inscripcion'),
    # Eliminar estudiantes inscritos
    path('inscripciones/<int:pk>/eliminar/', InscripcionDeleteView.as_view(), name='eliminar_inscripcion'),
]
