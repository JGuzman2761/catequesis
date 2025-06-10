from django.urls import path
from ..views.padre_views import (
    PadreListView, PadreCreateView, PadreUpdateView,
    PadreDetailView, PadreDeleteView
)

urlpatterns = [
    path('padres/', PadreListView.as_view(), name='padre_list'),
    path('padres/crear/', PadreCreateView.as_view(), name='padre_create'),
    path('padres/<int:pk>/editar/', PadreUpdateView.as_view(), name='padre_update'),
    path('padres/<int:pk>/', PadreDetailView.as_view(), name='padre_detail'),
    path('padres/<int:pk>/eliminar/', PadreDeleteView.as_view(), name='padre_delete'),
]