from django.urls import path
from ..views.padrino_views import (
    PadrinoListView, PadrinoCreateView, PadrinoUpdateView,
    PadrinoDeleteView, PadrinoDetailView
)

urlpatterns = [
    path('padrinos/', PadrinoListView.as_view(), name='padrino_list'),
    path('padrinos/nuevo/', PadrinoCreateView.as_view(), name='padrino_create'),
    path('padrinos/<int:pk>/editar/', PadrinoUpdateView.as_view(), name='padrino_update'),
    path('padrinos/<int:pk>/eliminar/', PadrinoDeleteView.as_view(), name='padrino_delete'),
    path('padrinos/<int:pk>/', PadrinoDetailView.as_view(), name='padrino_detail'),
]