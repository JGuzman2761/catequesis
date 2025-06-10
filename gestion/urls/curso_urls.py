from django.urls import path
from ..views.curso_views import (
    CursoListView, CursoDetailView,
    CursoCreateView, CursoUpdateView, CursoDeleteView)


urlpatterns = [
    path('cursos/', CursoListView.as_view(), name='curso_list'),
    path('cursos/<int:pk>/', CursoDetailView.as_view(), name='curso_detail'),
    path('cursos/crear/', CursoCreateView.as_view(), name='curso_create'),
    path('cursos/<int:pk>/editar/', CursoUpdateView.as_view(), name='curso_update'),
    path('cursos/<int:pk>/eliminar/', CursoDeleteView.as_view(), name='curso_delete'),
]