from django import forms
from usuarios.models import PerfilUser
from django.forms import BooleanField, TextInput

class PerfilUserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model=PerfilUser
        fields = ('username','first_name','last_name','amaterno','email','telefono', 'extension','jefe_inmediato','rol','unidad_user','password')
        widgets = {
            'username': TextInput(attrs={'class': 'form-control'}),
            'password': TextInput(attrs={'class': 'form-control'}),
            'first_name' : TextInput(attrs={'class':'form-control'}),
            'last_name': TextInput(attrs={'class': 'form-control'}),
            'amaterno': TextInput(attrs={'class': 'form-control'}),
            'email': TextInput(attrs={'class': 'form-control'}),
            'telefono': TextInput(attrs={'class': 'form-control'}),
            'extension': TextInput(attrs={'class': 'form-control'}),
            'rol' : forms.Select(attrs={'class': 'form-control'}),
            'jefe_inmediato' : forms.Select(attrs={'class': 'form-control'}),
            'unidad_user' : forms.Select(attrs={'class': 'form-control'}),
        }