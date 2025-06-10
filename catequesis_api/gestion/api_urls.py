from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .api_views import ParroquiaViewSet, CatequistaViewSet, PadrinoViewSet, PadreViewSet, EstudianteViewSet, CursoViewSet, CicloCatequesisViewSet, CursoAnualViewSet, GrupoViewSet, InscripcionViewSet

router = DefaultRouter()
router.register(r'parroquias', ParroquiaViewSet)
router.register(r'catequistas', CatequistaViewSet)
router.register(r'padrinos', PadrinoViewSet)
router.register(r'padres', PadreViewSet)
router.register(r'estudiantes', EstudianteViewSet)
router.register(r'cursos', CursoViewSet)
router.register(r'ciclos', CicloCatequesisViewSet)
router.register(r'cursos-anuales', CursoAnualViewSet)
router.register(r'grupos', GrupoViewSet)
router.register(r'inscripciones', InscripcionViewSet)

urlpatterns = [
    path('', include(router.urls)),
]