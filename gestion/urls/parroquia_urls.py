from django.urls import path
from ..views.parroquia_views import (
    ParroquiaListView, ParroquiaDetailView,
    ParroquiaCreateView, ParroquiaUpdateView, ParroquiaDeleteView
)

urlpatterns = [
    path('parroquias/', ParroquiaListView.as_view(), name='parroquia_list'),
    path('parroquias/<int:pk>/', ParroquiaDetailView.as_view(), name='parroquia_detail'),
    path('parroquias/crear/', ParroquiaCreateView.as_view(), name='parroquia_create'),
    path('parroquias/<int:pk>/editar/', ParroquiaUpdateView.as_view(), name='parroquia_update'),
    path('parroquias/<int:pk>/eliminar/', ParroquiaDeleteView.as_view(), name='parroquia_delete'),
]