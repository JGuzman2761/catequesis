from rest_framework import viewsets
from .models import Parroquia, Catequista, Padrino, Padre, Estudiante, Curso, CicloCatequesis, CursoAnual, Grupo, Inscripcion
from .serializers import ParroquiaSerializer, CatequistaSerializer, PadrinoSerializer, PadreSerializer, EstudianteSerializer, CursoSerializer, CicloCatequesisSerializer, CursoAnualSerializer, GrupoSerializer, InscripcionSerializer

class ParroquiaViewSet(viewsets.ModelViewSet):
    queryset = Parroquia.objects.all()
    serializer_class = ParroquiaSerializer

class CatequistaViewSet(viewsets.ModelViewSet):
    queryset = Catequista.objects.all()
    serializer_class = CatequistaSerializer

class PadrinoViewSet(viewsets.ModelViewSet):
    queryset = Padrino.objects.all()
    serializer_class = PadrinoSerializer

class PadreViewSet(viewsets.ModelViewSet):
    queryset = Padre.objects.all()
    serializer_class = PadreSerializer

class EstudianteViewSet(viewsets.ModelViewSet):
    queryset = Estudiante.objects.all()
    serializer_class = EstudianteSerializer

class CursoViewSet(viewsets.ModelViewSet):
    queryset = Curso.objects.all()
    serializer_class = CursoSerializer

class CicloCatequesisViewSet(viewsets.ModelViewSet):
    queryset = CicloCatequesis.objects.all()
    serializer_class = CicloCatequesisSerializer

class CursoAnualViewSet(viewsets.ModelViewSet):
    queryset = CursoAnual.objects.all()
    serializer_class = CursoAnualSerializer

class GrupoViewSet(viewsets.ModelViewSet):
    queryset = Grupo.objects.all()
    serializer_class = GrupoSerializer

class InscripcionViewSet(viewsets.ModelViewSet):
    queryset = Inscripcion.objects.all()
    serializer_class = InscripcionSerializer