# -*- coding: utf-8 -*-
from django.shortcuts import render
from metadato.forms import MetadatoForm
from metadato.models import Metadato
from tipo_expediente.forms import TipoExpForm
from unidad.models import Unidad
from django.contrib.auth.decorators import permission_required, login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
import datetime

import json
import time


from tipo_expediente.models import TipoExpediente
from usuarios.models import PerfilUser
from expediente.views import registro_log_admin

# Create your views here.
# @login_required(redirect_field_name='login')
def ListarTiposExpedientes(request):
    user_log = PerfilUser.objects.get(pk=request.user.pk)
    tipos = TipoExpediente.objects.all()
    registro_log_admin(user_log,"Consulta",None,"Tipos de Expedientes","Administrador")
    return render(request, 'tipos_expedientes.html', {'tipos': tipos, 'mensaje': 'Tipos de expedientes','user_log':user_log})

# @login_required(redirect_field_name='login')
def NuevoTipoExp(request):
    user_log = PerfilUser.objects.get(pk=request.user.pk)
    if request.method == "POST":
        form = TipoExpForm(request.POST)
        tipo = None
        if form.is_valid():
            # Instanciando unidad
            unidad = Unidad.objects.get(pk=request.POST.get('unidad',''))
            # Asignando el valor de activo
            tipo = TipoExpediente.objects.create(
                nombre = request.POST.get('nombre',''),
                siglas = request.POST.get('siglas',''),
                unidad = unidad,
                activo = True,
            )
            tipo.save()
            # return redirect('/tipos_expedientes/')
            # return redirect('/metadatos/nuevo_metadato')
            #form = MetadatoForm()
            registro_log_admin(user_log,"Crea",tipo,"Tipo de Expediente","Administrador")
            return render(request, 'metadatos.html', {'tipo': tipo,})
            # return render(request, 'nuevo_metadato.html', {'tipo': tipo,})
    else:
        form = TipoExpForm()
    unidades = Unidad.objects.all()
    return render(request, 'nuevo_tipo_exp.html', {'form': form, 'nuevo': 'Nuevo','user_log':user_log, 'unidades': unidades, 'mensaje':'Nuevo tipo de expediente'})


# @login_required(redirect_field_name='login')
def EditarTipoExp(request, pk):
    user_log = PerfilUser.objects.get(pk=request.user.pk)
    try:
        tipo = TipoExpediente.objects.get(pk=pk)
        form = TipoExpForm(instance=tipo)
        if request.method == "POST":
            # form = TipoExpForm(request.POST, instance=tipo)
            # Asignando el valor de activo
            if request.POST.get('activo','') == 'on':
                activo_dos = True
            else:
                activo_dos = False
            contador = 0
            if TipoExpediente.objects.filter(nombre=request.POST.get('nombre','')).exclude(pk=tipo.pk).exists():
                contador = 1
            if TipoExpediente.objects.filter(siglas=request.POST.get('siglas','')).exclude(pk=tipo.pk).exists():
                contador = 2
            if contador == 1:
                return render(request, 'edita_tipo_exp.html', {'form': form,'tipo': tipo, 'mensaje': 'Modificar tipo de expediente','user_log':user_log, 'error': 'nombre'})  
            if contador == 2:
                return render(request, 'edita_tipo_exp.html', {'form': form,'tipo': tipo, 'mensaje': 'Modificar tipo de expediente','user_log':user_log, 'error': 'siglas'})
            if contador == 0:
                TipoExpediente.objects.filter(pk=pk).update(nombre=request.POST.get('nombre',''))
                TipoExpediente.objects.filter(pk=pk).update(siglas=request.POST.get('siglas',''))
                TipoExpediente.objects.filter(pk=pk).update(activo=activo_dos)
                metadatos = Metadato.objects.filter(tipo_expediente=pk, base=1)
                registro_log_admin(user_log,"Edita",tipo,"Tipo de Expediente","Administrador")
            return render(request, 'metadatos.html', {'metadatos': metadatos,'tipo': tipo, 'mensaje': 'Metadatos del expediente','user_log':user_log})
        unidades = Unidad.objects.all()    
        return render(request, 'edita_tipo_exp.html', {'form': form,'tipo': tipo, 'mensaje': 'Modificar tipo de expediente','user_log':user_log, 'unidades': unidades})
    except ObjectDoesNotExist:
        return redirect('/tipos_expedientes/')

# @login_required(redirect_field_name='login')
def EliminarTipoExp(request, pk):
    try:
        user_log = PerfilUser.objects.get(pk=request.user.pk)
        tipo = TipoExpediente.objects.get(pk=pk)
        TipoExpediente.objects.filter(pk=pk).update(activo=False)
        registro_log_admin(user_log,"Elimina",tipo,"Tipo de Expediente","Administrador")
        return redirect('/tipos_expedientes/')
    except ObjectDoesNotExist:
        return redirect('/tipos_expedientes/')

# @login_required(redirect_field_name='login')
def VerTipoExp(request, pk): # No se usa
    user_log = PerfilUser.objects.get(pk=request.user.pk)
    try:
        tipo = TipoExpediente.objects.get(pk=pk)
        registro_log_admin(user_log,"Consulta",tipo,"Tipo de Expediente","Administrador")
        return render(request, 'tipo_expedientes.html', {'tipo_expedientes': tipo,'user_log':user_log})
    except ObjectDoesNotExist:
        return redirect('principal')