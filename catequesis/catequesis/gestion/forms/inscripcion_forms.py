from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, Row, Column, Submit
from ..models import Inscripcion

class InscripcionForm(forms.ModelForm):
    """
    Formulario para inscribir estudiantes en un grupo.
    El grupo se pasa por argumento y no es editable en el formulario.
    Incluye validación para evitar inscripciones duplicadas.
    """
    class Meta:
        model = Inscripcion
        fields = ['estudiante', 'aprobado']  # 'grupo' se asigna por la vista

    def __init__(self, *args, **kwargs):
        self.grupo = kwargs.pop('grupo', None)
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            Fieldset(
                f'Inscripción al grupo: {self.grupo.nombre if self.grupo else ""}',
                Row(
                    Column('estudiante', css_class='col-md-6'),
                ),
                Row(
                    Column('aprobado', css_class='col-md-6'),
                ),
            ),
            Submit('submit', 'Guardar', css_class='btn btn-primary')
        )

    def clean(self):
        cleaned_data = super().clean()
        estudiante = cleaned_data.get('estudiante')
        if estudiante and self.grupo:
            qs = Inscripcion.objects.filter(estudiante=estudiante, grupo=self.grupo)
            if self.instance.pk:
                qs = qs.exclude(pk=self.instance.pk)
            if qs.exists():
                raise forms.ValidationError("Este estudiante ya está inscrito en este grupo.")
        return cleaned_data

