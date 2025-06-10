from django.urls import path
from ..views.representante_views import (
    RepresentanteListView, RepresentanteDetailView,
    RepresentanteCreateView, RepresentanteUpdateView, RepresentanteDeleteView
)

urlpatterns = [
    path('representantes/', RepresentanteListView.as_view(), name='representante_list'),
    path('representantes/<int:pk>/', RepresentanteDetailView.as_view(), name='representante_detail'),
    path('representantes/crear/', RepresentanteCreateView.as_view(), name='representante_create'),
    path('representantes/<int:pk>/editar/', RepresentanteUpdateView.as_view(), name='representante_update'),
    path('representantes/<int:pk>/eliminar/', RepresentanteDeleteView.as_view(), name='representante_delete'),
]