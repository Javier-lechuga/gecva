# -*- coding: utf-8 -*-
from django.shortcuts import render
from estatus.models import Estatus
from expediente.forms import ExpedienteForm
from django.contrib.auth.decorators import permission_required, login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import get_user
from django.http import HttpResponse
import datetime

import json
import time


from expediente.models import Expediente
from metadato.models import Metadato
import tipo_expediente
from tipo_expediente.models import TipoExpediente
from unidad.models import Unidad

# Create your views here.
# @login_required(redirect_field_name='login')
def ListarExpedientes(request):
    expedientes = Expediente.objects.all()
    return render(request, 'expedientes.html', {'expedientes': expedientes, 'mensaje': 'Expedientes'})

# @login_required(redirect_field_name='login')
def ListarExpUnidad(request, pk):
    # expedientes = Expediente.objects.all()
    expedientes = Expediente.objects.filter(unidad=pk)
    return render(request, 'expedientes.html', {'expedientes': expedientes, 'mensaje': 'Expedientes'})

# @login_required(redirect_field_name='login')
def NuevoExpediente(request):
    if request.method == "POST":
        form = ExpedienteForm(request.POST)
        expediente = None
        if form.is_valid():
            # Instanciando Estatus
            estatus_dos = Estatus()
            estatus_dos = Estatus.objects.get(pk=7) # Estableciendo el estatus como creado
            # Instanciando TipoExpediente
            tipo_expediente_dos = TipoExpediente()
            tipo_expediente_dos = TipoExpediente.objects.get(pk=request.POST['tipo'])
            # Instanciando Unidad
            unidad_dos = Unidad()
            unidad_dos = Unidad.objects.get(pk=request.POST['unidad'])
            # Asignando el valor de activo
            if request.POST.get('activo','') == 'on':
                activo_dos = True
            else:
                activo_dos = False
            user = get_user(request)
            user = request.user
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
                usuario_crea = user
            )
            expediente.save()
            # return redirect('/expedientes/lista_metadatos_exp')
            return redirect('/expedientes/lista_metadatos_exp?pk=%s' % expediente.tipo_expediente.pk )
            # return render(request, '/expedientes/lista_metadatos_exp', {'pk': expediente.tipo_expediente,'mensaje': 'Metadatos'})
    else:
        form = ExpedienteForm()
    return render(request, 'nuevo_expediente.html', {'form': form, 'nuevo': 'Nuevo'})

# @login_required(redirect_field_name='login')
def GuardaMetadatosExp(request):
    vars = []
    for variable in request.POST.items():
        vars.append(variable)
    for otro in vars[2:]:
        Metadato.objects.filter(pk=otro[0]).update(valor=otro[1])
        Metadato.objects.filter(pk=otro[0]).update(version=1)
    # return HttpResponse(vars)
    return redirect('/expedientes/mis_expedientes')

# @login_required(redirect_field_name='login')
def ListarMisExpedientes(request):
    user = get_user(request)
    user = request.user
    expedientes = Expediente.objects.filter(usuario_crea=user)
    return render(request, 'mis_expedientes.html', {'expedientes': expedientes, 'mensaje': 'Expedientes'})

# @login_required(redirect_field_name='login')
def ListaMetadatosExp(request):
    if request.method == "GET":
        tipo = TipoExpediente()
        tipo = TipoExpediente.objects.get(pk=request.GET['pk'])
        metadatos = Metadato.objects.filter(tipo_expediente=tipo.pk)
        return render(request, 'lista_metadatos_exp.html', {'metadatos': metadatos, 'tipo': tipo,'mensaje': 'Metadatos'})

# @login_required(redirect_field_name='login')
def MuestraCamposExp(request):
    tipo = TipoExpediente()
    tipo = TipoExpediente.objects.get(pk=request.POST['tipo'])
    form = ExpedienteForm()
    return render(request, 'nuevo_expediente.html', {'form': form,'tipo': tipo, 'nuevo': 'Nuevo'})

# @login_required(redirect_field_name='login')
def SeleccionaTipoExp(request):
    tipos_expedientes = TipoExpediente.objects.all()
    # return redirect('/expedientes/')
    return render(request, 'selecciona_tipo_exp.html', {'tipos_expedientes': tipos_expedientes, 'mensaje': 'Expedientes'})
    

# @login_required(redirect_field_name='login')
def EditarExpediente(request, pk):
    try:
        expediente = Expediente.objects.get(pk=pk)
        if request.method == "POST":
            form = ExpedienteForm(request.POST, instance=expediente)
            if form.is_valid():
                expediente = form.save()
                expediente.save()
                return redirect('/expedientes/mis_expedientes')
        else:
            form = ExpedienteForm(instance=expediente)
        return render(request, 'edita_expediente.html', {'form': form, 'mensaje': 'Modificar expediente'})
    except ObjectDoesNotExist:
        return redirect('/expedientes/mis_expedientes')

# @login_required(redirect_field_name='login')
def EliminarExpediente(request, pk):
    try:
        expediente = Expediente.objects.get(pk=pk)
        expediente.delete()
        return redirect('/expedientes/mis_expedientes')
    except ObjectDoesNotExist:
        return redirect('/expedientes/mis_expedientes')

# @login_required(redirect_field_name='login')
def VerExpediente(request, pk):
    try:
        expediente = Expediente.objects.get(pk=pk)
        return render(request, 'expedientes.html', {'expediente': expediente})
    except ObjectDoesNotExist:
        return redirect('principal')