# .\estatus\forms.py

from django import forms
from django.forms import ModelForm
from django.forms import TextInput
from estatus.models import Estatus

class EstatusForm(forms.ModelForm):
    class Meta:
        es_doc = forms.BooleanField()
        model = Estatus
        fields = ('nombre','es_doc')
        widgets = {
            'nombre': TextInput(attrs={'class': 'form-control'}),
        }