from django import forms
from ..models import Inscripcion

class InscripcionForm(forms.ModelForm):
    class Meta:
        model = Inscripcion
        fields = ['estudiante', 'grupo', 'documentos_entregados']  # Quitamos 'curso'
