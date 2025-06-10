from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import validate_email, EmailValidator
from crispy_forms.helper import FormHelper
# Importamos los elementos necesarios, incluyendo Fieldset y HTML (por si acaso)
from crispy_forms.layout import Layout, Field, Fieldset, Submit, Row, Column, HTML,Div
# from core.forms import BaseCrispyModelForm # Descomenta si tienes una clase base
from ..models import Padrino

# Hereda de BaseCrispyModelForm si la tienes, si no, de forms.ModelForm
# class PadrinoForm(BaseCrispyModelForm):
class PadrinoForm(forms.ModelForm):
    """
    Formulario para crear y editar padrinos/madrinas.
    Incluye validaciones personalizadas, campo tipo_documento y presentación con Crispy Forms.
    """
    class Meta:
        model = Padrino
        exclude = ['creado_por', 'actualizado_por', 'fecha_creacion', 'ultima_actualizacion']
        widgets = {
            'nombres': forms.TextInput(attrs={'placeholder': 'Nombre(s) del padrino/madrina'}),
            'apellidos': forms.TextInput(attrs={'placeholder': 'Apellido(s)'}),
            'telefono': forms.TextInput(attrs={'placeholder': '(XXX) XXX-XXXX'}),
            'email': forms.EmailInput(attrs={'placeholder': 'correo.electronico@ejemplo.com'}),
            'direccion': forms.TextInput(attrs={'placeholder': 'Dirección completa (Calle, Número, Ciudad, etc.)'}),
            'tipo_documento': forms.Select(),
            'documento_validacion': forms.ClearableFileInput(attrs={'accept': 'image/*,application/pdf'}), # Ejemplo: limitar tipos de archivo
        }

    def __init__(self, *args, **kwargs):
        # Llamar a super() primero
        super().__init__(*args, **kwargs)

        # Inicializar el helper
        self.helper = FormHelper(self) # Pasar self
        self.helper.form_method = 'post'
        self.helper.form_tag = True # Generar tags <form>

        # Definir el Layout estructurado
        self.helper.layout = Layout(
            Fieldset(
                # Grupo para Información Personal
                'Información Personal del Padrino/Madrina',
                Row(
                    # Nombres y Apellidos
                    Column(Field('nombres'), css_class='col-md-6 mb-3'), # Añadir mb-3 para espacio
                    Column(Field('apellidos'), css_class='col-md-6 mb-3'),
                ),
                   # Dirección (puede ocupar toda la fila)
                Field('direccion', css_class='mb-3'), # Se mostrará como un campo de ancho completo
            ), # Fin del primer Fieldset

            Fieldset(
                # Grupo para Contacto
                'Información de Contacto',
                Row(
                     # Teléfono y Email
                    Column(Field('telefono'), css_class='col-md-6 mb-3'),
                    Column(Field('email'), css_class='col-md-6 mb-3'),
                ),
                
            ), # Fin del segundo Fieldset

            Fieldset(
                # Grupo para Documentación o Validación
                'Documentación / Validación',
                Row(
                    Column(Field('tipo_documento'), css_class='col-md-4 mb-3'),
                    Column(Field('documento_validacion'), css_class='col-md-8 mb-3'),
                ),
            ), # Fin del tercer Fieldset

            Div(
                Submit('submit', 'Guardar', css_class='btn btn-primary'),
                HTML('<a class="btn btn-danger ms-2" href="{% url \'padrino_list\' %}">Cancelar</a>'
                ),
            ),
        )
    def clean_nombres(self):
        nombres = self.cleaned_data.get('nombres', '').strip()
        if not nombres:
            raise ValidationError("Este campo es obligatorio.")
        if not re.match(r"^[a-zA-ZáéíóúÁÉÍÓÚñÑ\s'-]+$", nombres):
            raise ValidationError("El nombre solo puede contener letras, espacios, apóstrofes o guiones.")
        return nombres.title()

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
        query = Padrino.objects.filter(email__iexact=email)
        if self.instance and self.instance.pk:
            query = query.exclude(pk=self.instance.pk)
        if query.exists():
            raise ValidationError("Ya existe un padrino/madrina con este correo electrónico.")
        return email