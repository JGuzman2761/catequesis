from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Fieldset, Submit, Row, Column, HTML, Div
from ..models import Curso

class CursoForm(forms.ModelForm):
    class Meta:
        model = Curso
        fields = '__all__'  # O puedes especificar los campos manualmente si lo prefieres

        widgets = {
            'codigo': forms.TextInput(attrs={'placeholder': 'Código del curso'}),
            'nombre': forms.TextInput(attrs={'placeholder': 'Nombre del curso'}),
            'descripcion': forms.TextInput(attrs={'placeholder': 'Breve descripción del curso'}),
            'costo': forms.NumberInput(attrs={'placeholder': 'Costo en $ CAD'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = FormHelper(self)
        self.helper.form_method = 'post'
        self.helper.form_tag = True

        self.helper.layout = Layout(
            Fieldset(
                'Información del Curso',
                Row(
                    Column(Field('codigo'), css_class='col-md-2 mb-2'),
                    Column(Field('nombre'), css_class='col-md-8 mb-2'),
                ),
                Row(
                Field('descripcion', css_class='col-md-8 mb-2'),
                ),
                Row(
                Field('costo', css_class='col-md-2 mb-2'),
                ),
            ),
            Fieldset(
                'Documentos Requeridos para los Estudiantes',
                HTML('<p class="text-muted">Seleccione los documentos que serán obligatorios para los estudiantes que se inscriban en este curso.</p>'),
                Row(
                    Column(Field('acta_nacimiento'), css_class='col-md-3 mb-2'),
                    Column(Field('acta_bautizmo'), css_class='col-md-3 mb-2'),
                    Column(Field('acta_comunion'), css_class='col-md-3 mb-2'),
                    Column(Field('acta_matrimonio'), css_class='col-md-3 mb-2'),
                ),
                Div(
                    Submit('submit', 'Guardar', css_class='btn btn-primary'),
                    HTML('<a class="btn btn-danger ms-2" href="{% url \'curso_list\' %}">Cancelar</a>'
                    ),
                ),
            ),
           
        )
