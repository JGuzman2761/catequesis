from django.urls import path
from ..views import (
    CursoAnualListView, CursoAnualCreateView, CursoAnualUpdateView,
    CursoAnualDeleteView, CursoAnualDetailView
)

urlpatterns = [
    path('cursoanual/', CursoAnualListView.as_view(), name='cursoanual_list'),
    path('cursoanual/nuevo/', CursoAnualCreateView.as_view(), name='cursoanual_create'),
    path('cursoanual/<int:pk>/editar/', CursoAnualUpdateView.as_view(), name='cursoanual_update'),
    path('cursoanual/<int:pk>/eliminar/', CursoAnualDeleteView.as_view(), name='cursoanual_delete'),
    path('cursoanual/<int:pk>/', CursoAnualDetailView.as_view(), name='cursoanual_detail'),
]
