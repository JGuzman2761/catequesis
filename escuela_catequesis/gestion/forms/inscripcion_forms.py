from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, Row, Column, Submit
from ..models import Inscripcion

class InscripcionForm(forms.ModelForm):
    class Meta:
        model = Inscripcion
        fields = ['estudiante', 'aprobado']  # eliminamos 'grupo' porque viene por URL

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
            # Al hacer update, self.instance.pk es el id del objeto que editamos
            qs = Inscripcion.objects.filter(estudiante=estudiante, grupo=self.grupo)
            if self.instance.pk:
                qs = qs.exclude(pk=self.instance.pk)  # excluye el registro actual
            if qs.exists():
                raise forms.ValidationError("Este estudiante ya está inscrito en este grupo.")
        return cleaned_data

