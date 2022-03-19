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

# Create your views here.
# @login_required(redirect_field_name='login')
def ListarTiposDatos(request):
    tipos = TipoDato.objects.all()
    return render(request, 'tipos_datos.html', {'tipos': tipos, 'mensaje': 'Tipos de datos'})

# @login_required(redirect_field_name='login')
def NuevoTipoDato(request):
    if request.method == "POST":
        form = TipoDatoForm(request.POST)
        tipo = None
        if form.is_valid():
            user = request.user
            tipo = TipoDato.objects.create(
                tipo = request.POST.get('tipo',''),
            )
            tipo.save()
            return redirect('/tipos_datos/')
    else:
        form = TipoDatoForm()
    return render(request, 'nuevo_tipo_dato.html', {'form': form, 'nuevo': 'Nuevo'})

# @login_required(redirect_field_name='login')
def EditarTipoDato(request, pk):
    try:
        tipo = TipoDato.objects.get(pk=pk)
        if request.method == "POST":
            form = TipoDatoForm(request.POST, instance=tipo)
            if form.is_valid():
                tipo = form.save()
                tipo.save()
                return redirect('/tipos_datos/')
        else:
            form = TipoDatoForm(instance=tipo)
        return render(request, 'edita_tipo_dato.html', {'form': form, 'mensaje': 'Modificar tipo de dato'})
    except ObjectDoesNotExist:
        return redirect('/tipos_datos/')

# @login_required(redirect_field_name='login')
def EliminarTipoDato(request, pk):
    try:
        tipo = TipoDato.objects.get(pk=pk)
        tipo.delete()
        return redirect('/tipos_datos/')
    except ObjectDoesNotExist:
        return redirect('/tipos_datos/')

# @login_required(redirect_field_name='login')
def VerTipoDato(request, pk):
    try:
        tipo = TipoDato.objects.get(pk=pk)
        return render(request, 'tipos_datos.html', {'tipos_datos': tipo})
    except ObjectDoesNotExist:
        return redirect('principal')