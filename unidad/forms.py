from django import forms
from django.forms import ModelForm
from django.forms import TextInput
from unidad.models import Unidad

class UnidadForm(forms.ModelForm):
    class Meta:
        # activo = forms.BooleanField()
        model = Unidad
        fields = ('nombre', 'siglas', 'descripcion', 'jefe_unidad')
        widgets = {
            'nombre': TextInput(attrs={'class': 'form-control'}),
            'siglas': TextInput(attrs={'class': 'form-control'}),
            'descripcion': TextInput(attrs={'class': 'form-control'}),
            'jefe_unidad' : forms.Select(attrs={'class': 'form-control'}),
        }