from django import forms
from django.forms import ModelForm
from django.forms import TextInput
from tipo_expediente.models import TipoExpediente

class TipoExpForm(forms.ModelForm):
    class Meta:
        activo = forms.BooleanField()
        model = TipoExpediente
        fields = ('nombre', 'activo')
        widgets = {
            'nombre': TextInput(attrs={'class': 'form-control'}),
        }