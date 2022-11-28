# .\rol\forms.py
from django import forms
from django.forms import ModelForm
from django.forms import TextInput
from rol.models import Rol

class RolForm(forms.ModelForm):
    class Meta:
        model = Rol
        fields = ('nombre', 'descripcion')
        widgets = {
            'nombre': TextInput(attrs={'class': 'form-control'}),
            'descripcion': TextInput(attrs={'class': 'form-control'}),
        }