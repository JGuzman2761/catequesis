
from django.urls import path
from .views import (
    ParroquiaListView, ParroquiaDetailView, home_view,
    ParroquiaCreateView, ParroquiaUpdateView, ParroquiaDeleteView,
    CatequistaListView, CatequistaCreateView,CatequistaDetailView,
    CatequistaUpdateView, CatequistaDeleteView,
    PadreListView, PadreCreateView, PadreUpdateView,
    PadreDetailView, PadreDeleteView)
from .views import (
    PadrinoListView, PadrinoCreateView, PadrinoUpdateView,
    PadrinoDeleteView, PadrinoDetailView
)

urlpatterns = [
    path('', home_view, name='home'),
    path('home/', home_view, name='home'),
    path('parroquias/', ParroquiaListView.as_view(), name='parroquia_list'),
    path('parroquias/<int:pk>/', ParroquiaDetailView.as_view(), name='parroquia_detail'),
    path('parroquias/crear/', ParroquiaCreateView.as_view(), name='parroquia_create'),
    path('parroquias/<int:pk>/editar/', ParroquiaUpdateView.as_view(), name='parroquia_update'),
    path('parroquias/<int:pk>/eliminar/', ParroquiaDeleteView.as_view(), name='parroquia_delete'),
    # Catequistas
    path('catequistas/', CatequistaListView.as_view(), name='catequista_list'),
    path('catequistas/crear/', CatequistaCreateView.as_view(), name='catequista_create'),
    path('catequistas/editar/<int:pk>/', CatequistaUpdateView.as_view(), name='catequista_update'),
    path('catequistas/<int:pk>/', CatequistaDetailView.as_view(), name='catequista_detail'),
    path('catequistas/eliminar/<int:pk>/', CatequistaDeleteView.as_view(), name='catequista_delete'),
    # Padres
    path('padres/', PadreListView.as_view(), name='padre_list'),
    path('padres/crear/', PadreCreateView.as_view(), name='padre_create'),
    path('padres/<int:pk>/editar/', PadreUpdateView.as_view(), name='padre_update'),
    path('padres/<int:pk>/', PadreDetailView.as_view(), name='padre_detail'),
    path('padres/<int:pk>/eliminar/', PadreDeleteView.as_view(), name='padre_delete'),
    # Padrinos
    path('padrinos/', PadrinoListView.as_view(), name='padrino_list'),
    path('padrinos/nuevo/', PadrinoCreateView.as_view(), name='padrino_create'),
    path('padrinos/<int:pk>/editar/', PadrinoUpdateView.as_view(), name='padrino_update'),
    path('padrinos/<int:pk>/eliminar/', PadrinoDeleteView.as_view(), name='padrino_delete'),
    path('padrinos/<int:pk>/', PadrinoDetailView.as_view(), name='padrino_detail'),
   ]

