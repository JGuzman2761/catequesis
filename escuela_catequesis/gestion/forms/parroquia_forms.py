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
        # Opcional: Añadir widgets para placeholders, etc.
        widgets = {
            'nombre': forms.TextInput(attrs={'placeholder': 'Ej: Parroquia San Juan Bautista'}),
            'direccion': forms.TextInput(attrs={'placeholder': 'Ej: rue Ontario'}),
            'codigo_postal': forms.TextInput(attrs={'placeholder': 'Ej: J5G 1R9'}),
            'telefono': forms.TextInput(attrs={'placeholder': '(819)555-5555)'}),
            'email': forms.EmailInput(attrs={'placeholder': 'ejemplo@email.com'}),
            'parroco': forms.TextInput(attrs={'placeholder': 'Ej: Juan de los palotes'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_tag = True
        self.helper.label_class = 'form-label'
        self.helper.field_class = 'form-control'
    
        # Construcción del Layout mejorado
        self.helper.layout = Layout(
            # Agrupando campos principales con Fieldset
            Fieldset(
                # Leyenda del grupo
                'Información Principal',
                # Fila para Nombre y Párroco
                Row(
                    Column(Field('nombre', maxlength='100'), css_class='col-md-6'),
                    Column(Field('parroco', maxlength='100', placeholder='Nombre del párroco actual'), css_class='col-md-6'), # Placeholder añadido aquí
                ),
                # Fila para Dirección y Código Postal
                Row(
                    Column(Field('direccion', maxlength='150'), css_class='col-md-8'),
                    Column(Field('codigo_postal'), css_class='col-md-4'), # Incluyendo código postal
                ),
                # Usar HTML para un separador visual
                HTML('<hr>'),
                # Leyenda implícita para la siguiente sección o solo campos
                HTML('<h4>Contacto</h4>'),
                # Fila para Teléfono y Email
                Row(
                    Column(Field('telefono', maxlength='15'), css_class='col-md-3'),
                    Column(Field('email'), css_class='col-md-7'),
                ),
                
            ), # Fin del Fieldset

            # --- Opciones para Botones ---
            # Botones alineados en una fila
            Div(
                Submit('submit', 'Guardar', css_class='btn btn-primary'),
                HTML('<a class="btn btn-danger ms-2" href="{% url \'parroquia_list\' %}">Cancelar</a>'
                ),
            ),
        )
    # Validación para que el campo parroco no esté vacío
    def clean_parroco(self):
        parroco = self.cleaned_data.get('parroco')
        if not parroco or not parroco.strip():
            raise ValidationError("El campo 'Párroco' es obligatorio.")
        return parroco

    # Validación para email válido
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email:
            try:
                validate_email(email)
            except ValidationError:
                raise ValidationError("Por favor, introduce un correo electrónico válido.")
        return email