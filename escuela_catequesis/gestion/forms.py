from django import forms
from .models import Parroquia,Catequista,Padrino,Padre

class ParroquiaForm(forms.ModelForm):
    class Meta:
        model = Parroquia
        fields = '__all__'
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'direccion': forms.Textarea(attrs={'rows': 2}),
            'codigo_postal': forms.TextInput(attrs={'class': 'form-control'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.TextInput(attrs={'class': 'form-control'}),
            'parroco': forms.TextInput(attrs={'class': 'form-control'}),
        }

class CatequistaForm(forms.ModelForm):
    class Meta:
        model = Catequista
        fields = '__all__'
        widgets = {
            'nombres': forms.TextInput(attrs={'class': 'form-control'}),
            'apellidos': forms.TextInput(attrs={'class': 'form-control'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'parroquia': forms.Select(attrs={'class': 'form-select'}),
            'representante': forms.Select(attrs={'class': 'form-select'}),
        }

class PadreForm(forms.ModelForm):
    class Meta:
        model = Padre
        exclude = ['creado_por', 'actualizado_por', 'fecha_creacion', 'ultima_actualizacion']
        widgets = {
            'nombres': forms.TextInput(attrs={'class': 'form-control'}),
            'apellidos': forms.TextInput(attrs={'class': 'form-control'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'direccion': forms.TextInput(attrs={'class': 'form-control'}),
        }

class PadrinoForm(forms.ModelForm):
    class Meta:
        model = Padrino
        exclude = ('creado_por', 'actualizado_por', 'fecha_creacion', 'ultima_actualizacion')
