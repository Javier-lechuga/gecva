# .\expediente\forms.py
from dataclasses import fields
from django import forms
from django.forms import ModelForm
from django.forms import TextInput
from expediente.models import Expediente, Expediente_aprobador, Expediente_transferido, Registra_actividad, Expediente_deputy

class ExpedienteForm(forms.ModelForm):
    class Meta:
        
        fecha_creacion = forms.DateTimeField()
        fecha_cierre = forms.DateTimeField()
        activo = forms.BooleanField()
        # descripcion = forms.CharField( widget=forms.Textarea(attrs={'rows': 5, 'cols': 100}) )
        model = Expediente
        fields = ('identificador','nombre', 'descripcion','asunto',
            'ubicacion','activo', 'unidad')
        widgets = {
            'identificador': TextInput(attrs={'class': 'form-control'}),
            'nombre': TextInput(attrs={'class': 'form-control'}),
            'descripcion': TextInput(attrs={'class': 'form-control'}),
            'asunto': TextInput(attrs={'class': 'form-control'}),
            'ubicacion': TextInput(attrs={'class': 'form-control'}),
            # 'estatus' : forms.Select(attrs={'class': 'form-control'}),
            'unidad' : forms.Select(attrs={'class': 'form-control'}),
            # 'tipo_expediente' : forms.Select(attrs={'class': 'form-control'}),
        }

class ExpeAprobadorForm(forms.ModelForm):
    class Meta:
        model = Expediente_aprobador
        fields = '__all__'


class RegistraActividadForm():
    class Meta:
        models = Registra_actividad
        fields = '__all__'

class Expediente_deputyForm():
    class Meta:
        models = Expediente_deputy
        fields = '__all__'

class Expediente_transferidoForm():
    class Meta:
        models = Expediente_transferido
        fields = '__all__'