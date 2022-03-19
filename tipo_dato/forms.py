from django import forms
from django.forms import ModelForm
from django.forms import TextInput
from tipo_dato.models import TipoDato

class TipoDatoForm(forms.ModelForm):
    class Meta:
        model = TipoDato
        fields = ('tipo',)
        widgets = {
            'tipo': TextInput(attrs={'class': 'form-control'}),
        }