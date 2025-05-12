import re
from django import forms
from django.core.exceptions import ValidationError
from django.utils.safestring import mark_safe # Para mostrar HTML de forma segura
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Fieldset, Submit, Row, Column, HTML, Div
from ..models import Catequista, Parroquia

class CatequistaForm(forms.ModelForm):
    class Meta:
        model = Catequista
        # Añadir 'photo' a la lista de campos
        fields = ['nombres', 'apellidos', 'direccion', 'codigo_postal', 'telefono', 'email', 'parroquia', 'photo']
        widgets = {
            'nombres': forms.TextInput(attrs={'maxlength': '100', 'placeholder': 'Nombre(s)'}),
            'apellidos': forms.TextInput(attrs={'maxlength': '100', 'placeholder': 'Apellido(s)'}),
            'direccion': forms.TextInput(attrs={'placeholder': 'Calle, número, etc.'}),
            'codigo_postal': forms.TextInput(attrs={'placeholder': 'A1A 1A1'}),
            'telefono': forms.TextInput(attrs={'maxlength': '15', 'placeholder': '(XXX) XXX-XXXX'}),
            'email': forms.EmailInput(attrs={'placeholder': 'correo@ejemplo.com'}),
            # El widget por defecto para ImageField es ClearableFileInput, que está bien
            'photo': forms.ClearableFileInput(attrs={'accept': 'image/*'}), # Limitar a imágenes
        }
        labels = {
            'photo': 'Foto del Catequista',
            # ... otras labels ...
        }
        help_texts = {
            'photo': 'Opcional. Seleccione una imagen.',
            # ... otros help_texts ...
        }


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_method = 'post'
        self.helper.form_tag = True

        # --- MUY IMPORTANTE para subida de archivos ---
        self.helper.form_enctype = 'multipart/form-data'

        # --- Preparamos el HTML para la previsualización de la foto ---
        photo_preview_html = ''
        # Verificamos si estamos editando (instance existe y tiene pk) y si hay una foto guardada
        if self.instance and self.instance.pk and self.instance.photo:
            photo_preview_html = mark_safe(f'''
                <div class="mb-3">
                    <label class="form-label">Foto Actual:</label><br>
                    <img src="{self.instance.photo.url}" alt="Foto de {self.instance}" class="img-thumbnail" style="max-height: 150px; max-width: 150px;">
                </div>
            ''')

        # --- Definimos el Layout ---
        self.helper.layout = Layout(
            Fieldset(
                'Información Principal',
                Row(
                    # Mostramos la previsualización (si existe)
                    HTML(photo_preview_html) if photo_preview_html else HTML(''),
                    # Mostramos el campo para subir/cambiar la foto
                    Field('photo', css_class='mb-3'),
                ),
                Row(
                    Column(Field('nombres'), css_class='col-md-6 mb-3'),
                    Column(Field('apellidos'), css_class='col-md-6 mb-3'),
                ),
                Row(
                    Column(Field('direccion'), css_class='col-md-8 mb-3'),
                    Column(Field('codigo_postal'), css_class='col-md-4 mb-3'),
                ),
            ),
            Fieldset(
                'Contacto y Asignación',
                Row(
                    Column(Field('telefono'), css_class='col-md-6 mb-3'),
                    Column(Field('email'), css_class='col-md-6 mb-3'),
                ),
                Row(
                    Column(Field('parroquia'), css_class='col-md-12 mb-3'),
                ),
            ),
            
            Div(
                Submit('submit', 'Guardar', css_class='btn btn-primary'),
                HTML('<a class="btn btn-danger ms-2" href="{% url \'catequista_list\' %}">Cancelar</a>'
                ),
            ),
        )
        

    # --- Tus validaciones existentes ---
    def clean_nombres(self):
        nombres = self.cleaned_data.get('nombres')
        if not nombres or not nombres.strip():
            raise ValidationError("El campo de nombres no puede estar en blanco.")
        if nombres and not re.match(r"^[a-zA-ZáéíóúÁÉÍÓÚñÑ\s'-]+$", nombres):
            raise ValidationError("El nombre solo puede contener letras, espacios, apóstrofes o guiones.")
        return nombres.strip().title()

    def clean_apellidos(self):
        apellidos = self.cleaned_data.get('apellidos')
        if not apellidos or not apellidos.strip():
            raise ValidationError("El campo de apellidos no puede estar en blanco.")
        if apellidos and not re.match(r"^[a-zA-ZáéíóúÁÉÍÓÚñÑ\s'-]+$", apellidos):
             raise ValidationError("El apellido solo puede contener letras, espacios, apóstrofes o guiones.")
        return apellidos.strip().title()

    def clean_telefono(self):
        telefono = self.cleaned_data.get('telefono')
        if telefono and not re.match(r'^\+?1?\s?\(?\d{3}\)?[\s.-]?\d{3}[\s.-]?\d{4}$', telefono):
            raise ValidationError("Formato de teléfono inválido.")
        return telefono

    def clean_codigo_postal(self):
        codigo_postal = self.cleaned_data.get('codigo_postal')
        if codigo_postal:
            cp_limpio = codigo_postal.replace(' ', '').upper()
            if not re.match(r'^[A-Z]\d[A-Z]\d[A-Z]\d$', cp_limpio):
                raise ValidationError("Formato de código postal inválido. Use A1A1A1.")
            # Formatear a A1A 1A1
            return f"{cp_limpio[:3]} {cp_limpio[3:]}"
        return codigo_postal

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email:
            email = email.lower()
            query = Catequista.objects.filter(email__iexact=email)
            if self.instance and self.instance.pk:
                query = query.exclude(pk=self.instance.pk)
            if query.exists():
                raise ValidationError("Ya existe un catequista con este correo electrónico.")
        else:
            # Asegurar que el email sea obligatorio si no lo define el modelo
            raise ValidationError("El correo electrónico es obligatorio.")
        return email