from django import forms
from crispy_forms.helper import FormHelper
# Importa más elementos de layout
from crispy_forms.layout import Layout, Field, Fieldset, Submit, Row, Column, HTML
# Opcional: Para agrupar botones al final
from crispy_forms.bootstrap import FormActions
from django.urls import reverse_lazy 
from ..models import Grupo, Catequista, Curso

class GrupoForm(forms.ModelForm):
    # curso = forms.ModelChoiceField(
    #     queryset=Curso.objects.all(),
    #     to_field_name="codigo",
    #     widget=forms.Select(attrs={'class': 'form-control'}) # Ejemplo de añadir clases
    # )
    catequistas = forms.ModelMultipleChoiceField(
        queryset=Catequista.objects.all(),
        widget=forms.SelectMultiple, # Usamos el widget base, lo reemplazaremos en HTML
        required=False # O True según tu lógica de negocio
    )

    class Meta:
        model = Grupo
        fields = ['codigo', 'nombre', 'descripcion', 'curso', 'catequistas', 'max_estudiantes']
        widgets = {
            'codigo': forms.TextInput(attrs={'class': 'form-control'}),
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'curso': forms.Select(attrs={'class': 'form-control'}),
            'max_estudiantes': forms.NumberInput(attrs={'class': 'form-control'}),
            # No definimos widget para catequistas aquí, lo haremos en HTML/JS
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_tag = True
        self.helper.layout = Layout(
            Fieldset(
            # Leyenda del grupo
            'Información Principal',
                Row(
                    Column(Field('codigo', maxlength='10'), css_class='col-md-3'),
                    Column(Field('nombre', maxlength='100'), css_class='col-md-6'),
                ),
                Row(
                    Column(Field('descripcion', css_class='col-md-6'),),
                ),
                
                Row(
                    Column(Field('curso', maxlength='30'),),  
                    Column(Field('max_estudiantes'), css_class='col-md-2'),
                ),
            ),
            # Opción 1: Botón Submit simple (el enlace se pone en la plantilla) - RECOMENDADO
            Submit('submit', 'Guardar', css_class='btn btn-primary mt-4'),
            )