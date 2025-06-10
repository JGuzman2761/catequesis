from rest_framework import serializers
from .models import Parroquia, Catequista, Padrino, Padre, Estudiante, Curso, CicloCatequesis, CursoAnual, Grupo, Inscripcion

class ParroquiaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Parroquia
        fields = '__all__'

class CatequistaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Catequista
        fields = '__all__'

class PadrinoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Padrino
        fields = '__all__'

class PadreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Padre
        fields = '__all__'

class EstudianteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Estudiante
        fields = '__all__'

class CursoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Curso
        fields = '__all__'

class CicloCatequesisSerializer(serializers.ModelSerializer):
    class Meta:
        model = CicloCatequesis
        fields = '__all__'

class CursoAnualSerializer(serializers.ModelSerializer):
    class Meta:
        model = CursoAnual
        fields = '__all__'

class GrupoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Grupo
        fields = '__all__'

class InscripcionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Inscripcion
        fields = '__all__'