from django import forms
from django.urls import reverse_lazy # Para generar la URL del enlace (alternativa menos recomendada)
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from crispy_forms.helper import FormHelper
# Importa más elementos de layout
from crispy_forms.layout import Layout, Field, Fieldset, Submit, Row, Column, HTML, Div
# Opcional: Para agrupar botones al final
from crispy_forms.bootstrap import FormActions
from ..models import Parroquia

class ParroquiaForm(forms.ModelForm):
    """
    Formulario para crear y editar parroquias.
    Incluye validaciones personalizadas y presentación con Crispy Forms.
    """
    class Meta:
        model = Parroquia
        fields = [
            'nombre',
            'direccion',
            'codigo_postal',
            'telefono',
            'email',
            'parroco',
        ]
        widgets = {
            'nombre': forms.TextInput(attrs={'placeholder': 'Ej: Parroquia San Juan Bautista', 'maxlength': 100}),
            'direccion': forms.TextInput(attrs={'placeholder': 'Ej: rue Ontario', 'maxlength': 250}),
            'codigo_postal': forms.TextInput(attrs={'placeholder': 'Ej: J5G 1R9', 'maxlength': 10}),
            'telefono': forms.TextInput(attrs={'placeholder': '(819)555-5555)', 'maxlength': 15}),
            'email': forms.EmailInput(attrs={'placeholder': 'ejemplo@email.com'}),
            'parroco': forms.TextInput(attrs={'placeholder': 'Ej: Juan de los palotes', 'maxlength': 150}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_tag = True
        self.helper.label_class = 'form-label'
        self.helper.field_class = 'form-control'
        self.helper.layout = Layout(
            Fieldset(
                'Información Principal',
                Row(
                    Column(Field('nombre'), css_class='col-md-6'),
                    Column(Field('parroco'), css_class='col-md-6'),
                ),
                Row(
                    Column(Field('direccion'), css_class='col-md-8'),
                    Column(Field('codigo_postal'), css_class='col-md-4'),
                ),
                HTML('<hr>'),
                HTML('<h4>Contacto</h4>'),
                Row(
                    Column(Field('telefono'), css_class='col-md-3'),
                    Column(Field('email'), css_class='col-md-7'),
                ),
            ),
            Div(
                Submit('submit', 'Guardar', css_class='btn btn-primary'),
                HTML('<a class="btn btn-danger ms-2" href="{% url \'parroquia_list\' %}">Cancelar</a>'),
            ),
        )

    # Validación para que el campo parroco no esté vacío
    def clean_parroco(self):
        parroco = self.cleaned_data.get('parroco')
        if not parroco or not parroco.strip():
            raise ValidationError("El campo 'Párroco' es obligatorio.")
        return parroco.strip().title()

    # Validación para email válido
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email:
            try:
                validate_email(email)
            except ValidationError:
                raise ValidationError("Por favor, introduce un correo electrónico válido.")
            # Validación de unicidad
            query = Parroquia.objects.filter(email__iexact=email)
            if self.instance and self.instance.pk:
                query = query.exclude(pk=self.instance.pk)
            if query.exists():
                raise ValidationError("Ya existe una parroquia con este correo electrónico.")
        return email