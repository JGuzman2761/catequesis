
from django import forms
from ..models import Estudiante

class EstudianteForm(forms.ModelForm):
    class Meta:
        model = Estudiante
        exclude = [
            'creado_por',
            'actualizado_por',
            'fecha_creacion',
            'ultima_actualizacion']
        widgets = {
            'fecha_nacimiento': forms.DateInput(attrs={'type': 'date'}),
        }
