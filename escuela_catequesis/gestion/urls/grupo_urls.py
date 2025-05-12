from django.urls import path
from gestion.views import GrupoListView, GrupoCreateView, GrupoUpdateView, GrupoDeleteView, GrupoDetailView


urlpatterns = [
    path('grupos/', GrupoListView.as_view(), name='grupo_list'),
    path('grupos/<int:pk>/', GrupoDetailView.as_view(), name='grupo_detail'),
    path('grupos/create/', GrupoCreateView.as_view(), name='grupo_create'),
    path('grupos/update/<int:pk>/', GrupoUpdateView.as_view(), name='grupo_update'),
    path('grupos/delete/<int:pk>/', GrupoDeleteView.as_view(), name='grupo_delete'),
]