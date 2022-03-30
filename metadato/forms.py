from django import forms
from django.forms import ModelForm
from django.forms import TextInput
from metadato.models import Metadato

class MetadatoForm(forms.ModelForm):
    class Meta:
        obligatorio = forms.BooleanField()
        model = Metadato
        fields = ('nombre', 'descripcion', 'tipo_dato','obligatorio')
        widgets = {
            'nombre': TextInput(attrs={'class': 'form-control'}),
            'descripcion': TextInput(attrs={'class': 'form-control'}),
            'tipo_dato' : forms.Select(attrs={'class': 'form-control'}),
        }