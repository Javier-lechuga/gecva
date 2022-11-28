# .\tipo_expediente\forms.py
from django import forms
from django.forms import ModelForm
from django.forms import TextInput
from tipo_expediente.models import TipoExpediente

class TipoExpForm(forms.ModelForm):
    class Meta:
        # activo = forms.BooleanField()
        model = TipoExpediente
        fields = ('nombre', 'siglas','unidad',)
        widgets = {
            'nombre': TextInput(attrs={'class': 'form-control'}),
            'siglas': TextInput(attrs={'class': 'form-control'}),
            'unidad' : forms.Select(attrs={'class': 'form-control'}),
        }