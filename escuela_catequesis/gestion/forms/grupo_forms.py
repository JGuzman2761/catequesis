from django import forms
from django.contrib.admin.widgets import FilteredSelectMultiple
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Fieldset, Submit, Row, Column, Div, HTML
from ..models import Grupo

class GrupoForm(forms.ModelForm):
    class Meta:
        model = Grupo
        fields = ['curso_anual', 'nombre', 'cupo_maximo', 'catequistas']

        widgets = {
            'catequistas': FilteredSelectMultiple("catequistas", is_stacked=False),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Estilos para los campos
        self.fields['curso_anual'].widget.attrs.update({'class': 'form-control'})
        self.fields['nombre'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Nombre del grupo'})
        self.fields['cupo_maximo'].widget.attrs.update({'class': 'form-control', 'placeholder': '20'})
        # Personaliza el widget para catequistas
        # self.fields['catequistas'].widget = FilteredSelectMultiple("catequistas", is_stacked=False)

        # Helper de crispy
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_tag = True

        self.helper.layout = Layout(
            Fieldset(
                'Información del Grupo',
                Row(
                    Column(Field('curso_anual'), css_class='col-md-5'),
                    Column(Field('nombre'), css_class='col-md-5'),
                ),
                Row(
                    Column(Field('cupo_maximo'), css_class='col-md-3'),
                ),
                Row(
                  
                    Column(Field('catequistas'), css_class='col-md-12'),
                ),
                Div(
                    Submit('submit', 'Guardar', css_class='btn btn-primary'),
                    HTML('<a class="btn btn-danger ms-2" href="{% url \'grupo_list\' %}">Cancelar</a>'),
                    css_class='mt-3'
                ),
            ),
        )
