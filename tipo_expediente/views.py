# -*- coding: utf-8 -*-
from django.shortcuts import render
from metadato.forms import MetadatoForm
from metadato.models import Metadato
from tipo_expediente.forms import TipoExpForm
from django.contrib.auth.decorators import permission_required, login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
import datetime

import json
import time


from tipo_expediente.models import TipoExpediente

# Create your views here.
# @login_required(redirect_field_name='login')
def ListarTiposExpedientes(request):
    tipos = TipoExpediente.objects.all()
    return render(request, 'tipos_expedientes.html', {'tipos': tipos, 'mensaje': 'Tipos de expedientes'})

# @login_required(redirect_field_name='login')
def NuevoTipoExp(request):
    if request.method == "POST":
        form = TipoExpForm(request.POST)
        tipo = None
        if form.is_valid():
            # Asignando el valor de activo
            if request.POST.get('activo','') == 'on':
                activo_dos = True
            else:
                activo_dos = False
            user = request.user
            tipo = TipoExpediente.objects.create(
                nombre = request.POST.get('nombre',''),
                activo = activo_dos,
            )
            tipo.save()
            # return redirect('/tipos_expedientes/')
            # return redirect('/metadatos/nuevo_metadato')
            #form = MetadatoForm()
            return render(request, 'metadatos.html', {'tipo': tipo,})
            # return render(request, 'nuevo_metadato.html', {'tipo': tipo,})
    else:
        form = TipoExpForm()
    return render(request, 'nuevo_tipo_exp.html', {'form': form, 'nuevo': 'Nuevo'})


# @login_required(redirect_field_name='login')
def EditarTipoExp(request, pk):
    try:
        tipo = TipoExpediente.objects.get(pk=pk)
        if request.method == "POST":
            form = TipoExpForm(request.POST, instance=tipo)
            if form.is_valid():
                tipo = form.save()
                tipo.save()
                metadatos = Metadato.objects.filter(tipo_expediente=pk)
                return render(request, 'metadatos.html', {'metadatos': metadatos,'tipo': tipo, 'mensaje': 'Metadatos'})
        else:
            form = TipoExpForm(instance=tipo)
        return render(request, 'edita_tipo_exp.html', {'form': form,'tipo': tipo, 'mensaje': 'Modificar tipo de expediente'})
    except ObjectDoesNotExist:
        return redirect('/tipos_expedientes/')

# @login_required(redirect_field_name='login')
def EliminarTipoExp(request, pk):
    try:
        tipo = TipoExpediente.objects.get(pk=pk)
        tipo.delete()
        return redirect('/tipos_expedientes/')
    except ObjectDoesNotExist:
        return redirect('/tipos_expedientes/')

# @login_required(redirect_field_name='login')
def VerTipoExp(request, pk):
    try:
        tipo = TipoExpediente.objects.get(pk=pk)
        return render(request, 'tipo_expedientes.html', {'tipo_expedientes': tipo})
    except ObjectDoesNotExist:
        return redirect('principal')