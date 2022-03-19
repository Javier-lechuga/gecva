# -*- coding: utf-8 -*-
from django.shortcuts import render
from estatus.models import Estatus
from expediente.forms import ExpedienteForm
from django.contrib.auth.decorators import permission_required, login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import get_user
import datetime

import json
import time


from expediente.models import Expediente
import tipo_expediente
from tipo_expediente.models import TipoExpediente
from unidad.models import Unidad

# Create your views here.
# @login_required(redirect_field_name='login')
def ListarExpedientes(request):
    expedientes = Expediente.objects.all()
    return render(request, 'expedientes.html', {'expedientes': expedientes, 'mensaje': 'Expedientes'})

# @login_required(redirect_field_name='login')
def NuevoExpediente(request):
    if request.method == "POST":
        form = ExpedienteForm(request.POST)
        expediente = None
        if form.is_valid():
            # Instanciando Estatus
            estatus_dos = Estatus()
            estatus_dos = Estatus.objects.get(pk=request.POST['estatus'])
            # Instanciando TipoExpediente
            tipo_expediente_dos = TipoExpediente()
            tipo_expediente_dos = TipoExpediente.objects.get(pk=request.POST['tipo_expediente'])
            # Instanciando Unidad
            unidad_dos = Unidad()
            unidad_dos = Unidad.objects.get(pk=request.POST['unidad'])
            # Asignando el valor de activo
            if request.POST.get('activo','') == 'on':
                activo_dos = True
            else:
                activo_dos = False
            user = get_user(request)
            # user = request.user
            expediente = Expediente.objects.create(
                identificador = request.POST.get('identificador',''),
                nombre = request.POST.get('nombre',''),
                descripcion = request.POST.get('descripcion',''),
                asunto = request.POST.get('asunto',''),
                ubicacion = request.POST.get('ubicacion',''),
                motivo_rechazo = request.POST.get('motivo_rechazo',''),
                fecha_creacion = datetime.datetime.now(),
                estatus = estatus_dos,
                tipo_expediente = tipo_expediente_dos,
                unidad = unidad_dos,
                activo = activo_dos,
                # usuario_crea = user
            )
            expediente.save()
            return redirect('/expedientes/')
    else:
        form = ExpedienteForm()
    return render(request, 'nuevo_expediente.html', {'form': form, 'nuevo': 'Nuevo'})

# @login_required(redirect_field_name='login')
def EditarExpediente(request, pk):
    try:
        expediente = Expediente.objects.get(pk=pk)
        if request.method == "POST":
            form = ExpedienteForm(request.POST, instance=expediente)
            if form.is_valid():
                expediente = form.save()
                expediente.save()
                return redirect('/expedientes/')
        else:
            form = ExpedienteForm(instance=expediente)
        return render(request, 'edita_expediente.html', {'form': form, 'mensaje': 'Modificar expediente'})
    except ObjectDoesNotExist:
        return redirect('/expedientes/')

# @login_required(redirect_field_name='login')
def EliminarExpediente(request, pk):
    try:
        expediente = Expediente.objects.get(pk=pk)
        expediente.delete()
        return redirect('/expedientes/')
    except ObjectDoesNotExist:
        return redirect('/expedientes/')

# @login_required(redirect_field_name='login')
def VerExpediente(request, pk):
    try:
        expediente = Expediente.objects.get(pk=pk)
        return render(request, 'expedientes.html', {'expediente': expediente})
    except ObjectDoesNotExist:
        return redirect('principal')