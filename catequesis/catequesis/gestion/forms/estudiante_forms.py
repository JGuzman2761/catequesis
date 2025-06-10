import re
import os
from django import forms
from django.core.exceptions import ValidationError
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Fieldset, Submit, Row, Column, HTML, Div
from django.utils.safestring import mark_safe
from ..models import Estudiante

class EstudianteForm(forms.ModelForm):
    """
    Formulario para crear y editar estudiantes/catequizandos.
    Incluye campos de documentos, relaciones y previsualización de foto.
    """
    class Meta:
        model = Estudiante
        exclude = [
            'creado_por',
            'actualizado_por',
            'fecha_creacion',
            'ultima_actualizacion'
        ]
        widgets = {
            'fecha_nacimiento': forms.DateInput(attrs={'type': 'date'}),
            'photo': forms.ClearableFileInput(attrs={'accept': 'image/*'}),
            'acta_bautismo': forms.ClearableFileInput(),
            'acta_nacimiento': forms.ClearableFileInput(),
            'acta_comunion': forms.ClearableFileInput(),
            'acta_catequesis': forms.ClearableFileInput(),
        }
        labels = {
            'photo': 'Foto del Estudiante',
            'padre': 'Padre/Madre/Tutor',
            'padrino': 'Padrino/Madrina',
            'acta_bautismo': 'Acta de Bautismo',
            'acta_nacimiento': 'Acta de Nacimiento',
            'acta_comunion': 'Acta de Comunión',
            'acta_catequesis': 'Acta de Catequesis',
        }
        help_texts = {
            'photo': 'Opcional. Seleccione una imagen.',
            'acta_bautismo': 'Opcional. Suba el acta de bautismo.',
            'acta_nacimiento': 'Opcional. Suba el acta de nacimiento.',
            'acta_comunion': 'Opcional. Suba el acta de comunión.',
            'acta_catequesis': 'Opcional. Suba el acta de catequesis.',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_method = 'post'
        self.helper.form_tag = True
        self.helper.form_enctype = 'multipart/form-data'

        # Previsualización si hay foto (verifica existencia física)
        photo_preview_html = ''
        if self.instance and self.instance.pk and self.instance.photo:
            try:
                if os.path.isfile(self.instance.photo.path):
                    photo_preview_html = mark_safe(f'''
                        <div class="mb-3">
                            <label class="form-label">Foto Actual:</label><br>
                            <img src="{self.instance.photo.url}" alt="Foto de {self.instance}" class="img-thumbnail" style="max-height: 150px; max-width: 150px;">
                        </div>
                    ''')
            except Exception:
                pass

        # Layout
        self.helper.layout = Layout(
            Fieldset(
                'Información Personal',
                Row(
                    HTML(photo_preview_html) if photo_preview_html else HTML(''),
                    Field('photo', css_class='mb-3'),
                ),
                Row(
                    Column(Field('nombres'), css_class='col-md-6 mb-3'),
                    Column(Field('apellidos'), css_class='col-md-6 mb-3'),
                ),
                Row(
                    Column(Field('fecha_nacimiento'), css_class='col-md-6 mb-3'),
                ),
            ),
            Fieldset(
                'Contacto',
                Row(
                    Column(Field('telefono'), css_class='col-md-6 mb-3'),
                    Column(Field('email'), css_class='col-md-6 mb-3'),
                ),
                Row(
                    Column(Field('direccion'), css_class='col-md-8 mb-3'),
                    Column(Field('codigo_postal'), css_class='col-md-4 mb-3'),
                ),
            ),
            Fieldset(
                'Relaciones Familiares',
                Row(
                    Column(Field('padre'), css_class='col-md-6 mb-3'),
                    Column(Field('padrino'), css_class='col-md-6 mb-3'),
                ),
            ),
            Fieldset(
                'Documentos',
                Row(
                    Column(Field('acta_bautismo'), css_class='col-md-3 mb-3'),
                    Column(Field('acta_nacimiento'), css_class='col-md-3 mb-3'),
                    Column(Field('acta_comunion'), css_class='col-md-3 mb-3'),
                    Column(Field('acta_catequesis'), css_class='col-md-3 mb-3'),
                ),
            ),
            Div(
                Submit('submit', 'Guardar', css_class='btn btn-primary'),
                HTML('<a class="btn btn-danger ms-2" href="{% url \'estudiante_list\' %}">Cancelar</a>')
            )
        )

    # Validaciones
    def clean_nombres(self):
        nombres = self.cleaned_data.get('nombres')
        if not nombres or not nombres.strip():
            raise ValidationError("El campo de nombres no puede estar en blanco.")
        if not re.match(r"^[a-zA-ZáéíóúÁÉÍÓÚñÑ\s'-]+$", nombres):
            raise ValidationError("El nombre solo puede contener letras, espacios, apóstrofes o guiones.")
        return nombres.strip().title()

    def clean_apellidos(self):
        apellidos = self.cleaned_data.get('apellidos')
        if not apellidos or not apellidos.strip():
            raise ValidationError("El campo de apellidos no puede estar en blanco.")
        if not re.match(r"^[a-zA-ZáéíóúÁÉÍÓÚñÑ\s'-]+$", apellidos):
            raise ValidationError("El apellido solo puede contener letras, espacios, apóstrofes o guiones.")
        return apellidos.strip().title()

    def clean_telefono(self):
        telefono = self.cleaned_data.get('telefono')
        if telefono and not re.match(r'^\+?1?\s?\(?\d{3}\)?[\s.-]?\d{3}[\s.-]?\d{4}$', telefono):
            raise ValidationError("Formato de teléfono inválido. Ejemplo: (514) 123-4567")
        return telefono

    def clean_codigo_postal(self):
        codigo_postal = self.cleaned_data.get('codigo_postal')
        if codigo_postal:
            cp_limpio = codigo_postal.replace(' ', '').upper()
            if not re.match(r'^[A-Z]\d[A-Z]\d[A-Z]\d$', cp_limpio):
                raise ValidationError("Formato de código postal inválido. Use A1A1A1.")
            return f"{cp_limpio[:3]} {cp_limpio[3:]}"
        return codigo_postal

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email:
            email = email.lower()
            query = Estudiante.objects.filter(email__iexact=email)
            if self.instance and self.instance.pk:
                query = query.exclude(pk=self.instance.pk)
            if query.exists():
                raise ValidationError("Ya existe un estudiante con este correo electrónico.")
        else:
            raise ValidationError("El correo electrónico es obligatorio.")
        return email
