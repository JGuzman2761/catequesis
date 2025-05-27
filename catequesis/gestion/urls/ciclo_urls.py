from django.urls import path
from gestion.views.ciclo_views import (
    CicloListView, CicloCreateView, CicloUpdateView, CicloDeleteView, CicloDetailView
)

urlpatterns = [
    path('', CicloListView.as_view(), name='lista_ciclo'),
    path('nuevo/', CicloCreateView.as_view(), name='crear_ciclo'),
    path('editar/<int:pk>/', CicloUpdateView.as_view(), name='editar_ciclo'),
    path('eliminar/<int:pk>/', CicloDeleteView.as_view(), name='eliminar_ciclo'),
    path('ciclos/<int:pk>/', CicloDetailView.as_view(), name='detail_ciclo'),
]
