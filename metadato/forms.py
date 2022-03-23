from django import forms
from django.forms import ModelForm
from django.forms import TextInput
from metadato.models import Metadato

class MetadatoForm(forms.ModelForm):
    class Meta:
        # tipo_dato = forms.Select(attrs={'class': 'form-control'})
        # estatus_uno = forms.Select(attrs={'class': 'form-control'})
        obligatorio = forms.BooleanField()
        model = Metadato
        fields = ('nombre', 'descripcion', 'tipo_dato','obligatorio')
        widgets = {
            'nombre': TextInput(attrs={'class': 'form-control'}),
            'descripcion': TextInput(attrs={'class': 'form-control'}),
            # 'valor': TextInput(attrs={'class': 'form-control'}),
            # 'version': TextInput(attrs={'class': 'form-control'}),
            # 'motivo_rechazo': TextInput(attrs={'class': 'form-control'}),
            'tipo_dato' : forms.Select(attrs={'class': 'form-control'}),
            # 'estatus' : forms.Select(attrs={'class': 'form-control'}),
        }