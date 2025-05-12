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
    class Meta:
        model = Padrino
        # Mantenemos tu exclude original
        exclude = ['creado_por', 'actualizado_por', 'fecha_creacion', 'ultima_actualizacion']
        # Añadimos widgets para placeholders
        widgets = {
            'nombres': forms.TextInput(attrs={'placeholder': 'Nombre(s) del padrino/madrina'}),
            'apellidos': forms.TextInput(attrs={'placeholder': 'Apellido(s)'}),
            'telefono': forms.TextInput(attrs={'placeholder': '(XXX) XXX-XXXX'}),
            'email': forms.EmailInput(attrs={'placeholder': 'correo.electronico@ejemplo.com'}),
            'direccion': forms.TextInput(attrs={'placeholder': 'Dirección completa (Calle, Número, Ciudad, etc.)'}),
            # Para FileField o ImageField, el widget suele ser ClearableFileInput
            # No necesita placeholder, pero puedes personalizar el texto si quieres.
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
                 # Campo para documento
                 # La Row/Column asegura que use el espacio definido (col-md-6 en tu original)
                 # Si quieres que ocupe toda la fila, usa solo Field('documento_validacion', css_class='mb-3')
                Row(
                    Column(Field('documento_validacion'), css_class='col-md-8 mb-3'), # Ajustado a col-md-8 como ejemplo, o usa 12
                     # Podrías añadir texto de ayuda aquí si es necesario con HTML
                     # Column(HTML('<small class="form-text text-muted">Suba el certificado de confirmación o similar.</small>'), css_class='col-md-4 align-self-center')
                ),
            ), # Fin del tercer Fieldset

            Div(
                Submit('submit', 'Guardar', css_class='btn btn-primary'),
                HTML('<a class="btn btn-danger ms-2" href="{% url \'parroquia_list\' %}">Cancelar</a>'
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
        email = self.cleaned_data.get('email', '').strip()
        if not email:
            raise ValidationError("El correo electrónico es obligatorio.")
        try:
            validate_email(email)
        except ValidationError:
            raise ValidationError("Debe ingresar un correo electrónico válido.")
        return email