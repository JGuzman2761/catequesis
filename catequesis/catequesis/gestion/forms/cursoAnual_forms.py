from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Fieldset, Submit, Row, Column, HTML, Div
from ..models import CursoAnual

class CursoAnualForm(forms.ModelForm):
    """
    Formulario para crear y editar cursos anuales.
    Refleja la estructura actual del modelo CursoAnual.
    """
    class Meta:
        model = CursoAnual
        fields = ['curso', 'ciclo', 'cupo_maximo', 'cerrado']
        widgets = {
            'curso': forms.Select(attrs={'class': 'form-control'}),
            'ciclo': forms.Select(attrs={'class': 'form-control'}),
            'cupo_maximo': forms.NumberInput(attrs={'placeholder': 'Ej. 20'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # BooleanField checkbox estilo Bootstrap 5
        self.fields['cerrado'].widget.attrs.update({'class': 'form-check-input'})

        self.helper = FormHelper(self)
        self.helper.form_method = 'post'
        self.helper.form_tag = True

        self.helper.layout = Layout(
            Fieldset(
                'Información del Curso Anual',
                Row(
                    Column(Field('curso'), css_class='col-md-6 mb-2'),
                    Column(Field('ciclo'), css_class='col-md-6 mb-2'),
                ),
                Row(
                    Column(Field('cupo_maximo'), css_class='col-md-4 mb-2'),
                    Column(Field('cerrado'), css_class='col-md-2 mb-2 mt-4'),
                ),
                Div(
                    Submit('submit', 'Guardar', css_class='btn btn-primary'),
                    HTML('<a class="btn btn-danger ms-2" href="{% url \'cursoanual_list\' %}">Cancelar</a>'),
                    css_class='mt-3'
                ),
            ),
            
        )
