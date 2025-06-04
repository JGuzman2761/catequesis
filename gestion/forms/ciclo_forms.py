from django import forms
from django.core.exceptions import ValidationError
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Fieldset, Submit, Row, Column, HTML, Div
from ..models import CicloCatequesis
import datetime

class CicloForm(forms.ModelForm):
    """
    Formulario para crear y editar ciclos de catequesis.
    Incluye validaciones de fechas y presentación con Crispy Forms.
    """
    class Meta:
        model = CicloCatequesis
        fields = ['nombre_ciclo', 'descripcion','fecha_inicio', 'fecha_fin', 'activo','observaciones']
        widgets = {
            'nombre_ciclo': forms.TextInput(attrs={'placeholder': 'Nombre del ciclo', 'maxlength': 100}),
            'descripcion': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Descripción opcional'}),
            'fecha_inicio': forms.DateInput(attrs={'type': 'date'}),
            'fecha_fin': forms.DateInput(attrs={'type': 'date'}),
            'activo': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'observaciones': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Observaciones'}),
        }
        labels = {
            'nombre_ciclo': 'Nombre del Ciclo',
            'descripcion': 'Descripción del Ciclo',
            'fecha_inicio': 'Fecha de Inicio',
            'fecha_fin': 'Fecha de Fin',
            'activo': '¿Está activo?',
            'observaciones': 'Observaciones',
        }
        help_texts = {
            'activo': 'Indica si el ciclo está activo actualmente.',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_method = 'post'
        self.helper.form_enctype = 'multipart/form-data'
        self.helper.form_tag = True

        self.helper.layout = Layout(
            Fieldset(
                'Información del Ciclo',
                Row(
                    Column(Field('nombre_ciclo'), css_class='col-md-6 mb-3'),
                    Column(Field('activo'), css_class='col-md-6 mb-3'),
                ),
                Row(
                    Column(Field('descripcion'), css_class='col-12 mb-3'),
                ),
                Row(
                    Column(Field('fecha_inicio'), css_class='col-md-6 mb-3'),
                    Column(Field('fecha_fin'), css_class='col-md-6 mb-3'),
                ),
                Row(
                    Column(Field('observaciones'), css_class='col-md-10 mb-3'),
                ),
            ),
            Div(
                Submit('submit', 'Guardar', css_class='btn btn-primary'),
                HTML('<a href="{% url \'lista_ciclo\' %}" class="btn btn-danger ms-2">Cancelar</a>'),
                css_class='mt-3'
            )
        )

    # Validación personalizada para el nombre del ciclo
    def clean_nombre_ciclo(self):
        nombre = self.cleaned_data.get('nombre_ciclo')
        if not nombre or not nombre.strip():
            raise ValidationError("El nombre del ciclo no puede estar vacío.")
        return nombre.strip().title()

    def clean(self):
        cleaned_data = super().clean()
        fecha_inicio = cleaned_data.get('fecha_inicio')
        fecha_fin = cleaned_data.get('fecha_fin')

        # La validación principal de fechas ya está en el modelo, pero aquí puedes agregar reglas adicionales
        if fecha_inicio and fecha_inicio < datetime.date(2000, 1, 1):
            self.add_error('fecha_inicio', "La fecha de inicio es demasiado antigua.")

        return cleaned_data
