# gestion/forms/profile_forms.py
from django import forms
from gestion.models import Profile

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['photo'] # Puedes agregar más campos del modelo Profile aquí si los añades en el futuro