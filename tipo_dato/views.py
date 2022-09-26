# -*- coding: utf-8 -*-
from django.shortcuts import render
from tipo_dato.forms import TipoDatoForm
from django.contrib.auth.decorators import permission_required, login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
import datetime

import json
import time


from tipo_dato.models import TipoDato
from usuarios.models import PerfilUser
from expediente.views import registro_log_admin

# Create your views here.
# @login_required(redirect_field_name='login')
def ListarTiposDatos(request):
    user_log = PerfilUser.objects.get(pk=request.user.pk)
    tipos = TipoDato.objects.all()
    registro_log_admin(user_log,"Consulta",None,"Tipo de Dato","Administrador")
    return render(request, 'tipos_datos.html', {'tipos': tipos, 'mensaje': 'Tipos de datos','user_log':user_log})

# @login_required(redirect_field_name='login')
def NuevoTipoDato(request):
    user_log = PerfilUser.objects.get(pk=request.user.pk)
    if request.method == "POST":
        form = TipoDatoForm(request.POST)
        tipo = None
        if form.is_valid():
            user = request.user
            tipo = TipoDato.objects.create(
                tipo = request.POST.get('tipo',''),
            )
            tipo.save()
            registro_log_admin(user_log,"Crea",tipo,"Tipo de Dato","Administrador")
            return redirect('/tipos_datos/')
    else:
        form = TipoDatoForm()
    return render(request, 'nuevo_tipo_dato.html', {'form': form, 'nuevo': 'Nuevo','user_log':user_log})

# @login_required(redirect_field_name='login')
def EditarTipoDato(request, pk):
    user_log = PerfilUser.objects.get(pk=request.user.pk)
    try:
        tipo = TipoDato.objects.get(pk=pk)
        if request.method == "POST":
            form = TipoDatoForm(request.POST, instance=tipo)
            if form.is_valid():
                tipo = form.save()
                tipo.save()
                registro_log_admin(user_log,"Edita",tipo,"Tipo de Dato","Administrador")
                return redirect('/tipos_datos/')
        else:
            form = TipoDatoForm(instance=tipo)
        return render(request, 'edita_tipo_dato.html', {'form': form, 'mensaje': 'Modificar tipo de dato','user_log':user_log})
    except ObjectDoesNotExist:
        return redirect('/tipos_datos/')

# @login_required(redirect_field_name='login')
def EliminarTipoDato(request, pk):
    try:
        user_log = PerfilUser.objects.get(pk=request.user.pk)
        tipo = TipoDato.objects.get(pk=pk)
        tipo.delete()
        registro_log_admin(user_log,"Elimina",tipo,"Tipo de Dato","Administrador")
        return redirect('/tipos_datos/')
    except ObjectDoesNotExist:
        return redirect('/tipos_datos/')

# @login_required(redirect_field_name='login')
def VerTipoDato(request, pk):
    user_log = PerfilUser.objects.get(pk=request.user.pk)
    try:
        tipo = TipoDato.objects.get(pk=pk)
        registro_log_admin(user_log,"Consulta",tipo,"Tipo de Dato","Administrador")
        return render(request, 'tipos_datos.html', {'tipos_datos': tipo,'user_log':user_log})
    except ObjectDoesNotExist:
        return redirect('principal')