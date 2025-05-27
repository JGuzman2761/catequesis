from django import forms
import re
from django.core.exceptions import ValidationError
from django.core.validators import validate_email, EmailValidator
from crispy_forms.helper import FormHelper
# Asegúrate de importar los elementos necesarios de layout
from crispy_forms.layout import Layout, Field, Fieldset, Submit, Row, Column, HTML,Div
from ..models import Padre 
class PadreForm(forms.ModelForm):
    """
    Formulario para crear y editar padres/madres/tutores.
    Incluye validaciones personalizadas y presentación con Crispy Forms.
    """
    class Meta:
        model = Padre
        exclude = ['creado_por', 'actualizado_por', 'fecha_creacion', 'ultima_actualizacion']
        widgets = {
            'nombres': forms.TextInput(attrs={'placeholder': 'Nombre(s) del padre/madre/tutor'}),
            'apellidos': forms.TextInput(attrs={'placeholder': 'Apellido(s)'}),
            'direccion': forms.TextInput(attrs={'placeholder': 'Calle, número, apartamento (si aplica)'}),
            'codigo_postal': forms.TextInput(attrs={'placeholder': 'Ej: H2X 1Y1'}),
            'telefono': forms.TextInput(attrs={'placeholder': '(514) 555-1234'}),
            'email': forms.EmailInput(attrs={'placeholder': 'correo@ejemplo.com'}),
        }

    def __init__(self, *args, **kwargs):
        # MUY IMPORTANTE: Llamar al __init__ de la clase padre PRIMERO
        super().__init__(*args, **kwargs)

        # Inicializar el helper DESPUÉS de super()
        self.helper = FormHelper(self) # Pasar self para que se asocie al formulario
        self.helper.form_method = 'post'
        self.helper.form_tag = True # Asegura que Crispy genere <form> tags
        # Definir el Layout estructurado
        self.helper.layout = Layout(
            Fieldset(
                # Primer grupo: Información Personal
                'Información Personal',
                Row(
                    # Nombre y Apellido en la misma fila
                    Column(Field('nombres'), css_class='col-md-6 mb-3'), # mb-3 para espacio inferior
                    Column(Field('apellidos'), css_class='col-md-6 mb-3'),
                ),
                  # Dirección puede ir sola o con código postal
                Field('direccion', css_class='mb-3'),
                Row(
                    Column(Field('codigo_postal'), css_class='col-md-4 mb-3'),
                    # Podrías añadir ciudad/provincia si existen en el modelo
                    # Column(Field('ciudad'), css_class='col-md-8 mb-3'),
                ),
            ),
            Fieldset(
                # Segundo grupo: Información de Contacto
                'Contacto',
              
                Row(
                    # Teléfono y Email en la misma fila
                    Column(Field('telefono'), css_class='col-md-4 mb-3'),
                    Column(Field('email'), css_class='col-md-8 mb-3'),
                ),
            ),
      
            Div(
                Submit('submit', 'Guardar', css_class='btn btn-primary'),
                HTML('<a class="btn btn-danger ms-2" href="{% url \'padre_list\' %}">Cancelar</a>'
                ),
            ),
        )

    def clean_nombres(self):
        nombres = self.cleaned_data.get('nombres', '').strip()
        if not nombres:
            raise ValidationError("Este campo es obligatorio.")
        if any(char.isdigit() for char in nombres):
            raise ValidationError("El nombre no debe contener números.")
        return nombres

    def clean_apellidos(self):
        apellidos = self.cleaned_data.get('apellidos', '').strip()
        if not apellidos:
            raise ValidationError("Este campo es obligatorio.")
        if any(char.isdigit() for char in apellidos):
            raise ValidationError("El apellido no debe contener números.")
        return apellidos

    def clean_email(self):
        email = self.cleaned_data.get('email', '').strip().lower()
        if not email:
            raise ValidationError("El correo electrónico es obligatorio.")
        try:
            validate_email(email)
        except ValidationError:
            raise ValidationError("Debe ingresar un correo electrónico válido.")
        # Validación de unicidad
        query = Padre.objects.filter(email__iexact=email)
        if self.instance and self.instance.pk:
            query = query.exclude(pk=self.instance.pk)
        if query.exists():
            raise ValidationError("Ya existe un padre/madre/tutor con este correo electrónico.")
        return email
