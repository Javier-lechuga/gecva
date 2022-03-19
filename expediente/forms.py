from django import forms
from django.forms import ModelForm
from django.forms import TextInput
from expediente.models import Expediente

class ExpedienteForm(forms.ModelForm):
    class Meta:
        
        fecha_creacion = forms.DateTimeField()
        fecha_cierre = forms.DateTimeField()
        activo = forms.BooleanField()
        # descripcion = forms.CharField( widget=forms.Textarea(attrs={'rows': 5, 'cols': 100}) )
        model = Expediente
        fields = ('identificador','nombre', 'descripcion','asunto',
            'ubicacion', 'motivo_rechazo','activo', 'tipo_expediente', 'estatus', 'unidad')
        widgets = {
            'identificador': TextInput(attrs={'class': 'form-control'}),
            'nombre': TextInput(attrs={'class': 'form-control'}),
            'descripcion': TextInput(attrs={'class': 'form-control'}),
            'asunto': TextInput(attrs={'class': 'form-control'}),
            'ubicacion': TextInput(attrs={'class': 'form-control'}),
            'motivo_rechazo': TextInput(attrs={'class': 'form-control'}),
            'estatus' : forms.Select(attrs={'class': 'form-control'}),
            'unidad' : forms.Select(attrs={'class': 'form-control'}),
            'tipo_expediente' : forms.Select(attrs={'class': 'form-control'}),
            # 'usuario_crea' : forms.Select(attrs={'class': 'form-control'}),
        }