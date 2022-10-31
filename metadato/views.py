# -*- coding: utf-8 -*-
from django.http import HttpResponse
from django.shortcuts import render
from estatus.models import Estatus
import expediente
from expediente.models import Expediente
from metadato.forms import MetadatoForm
from django.contrib.auth.decorators import permission_required, login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
import datetime

import json
import time


from metadato.models import Metadato
from tipo_dato.models import TipoDato
from tipo_expediente.models import TipoExpediente
from usuarios.models import PerfilUser
from expediente.views import registro_log_admin

# Create your views here.
# @login_required(redirect_field_name='login')
def ListarMetadatos(request):
    user_log = PerfilUser.objects.get(pk=request.user.pk)
    metadatos = Metadato.objects.all()
    registro_log_admin(user_log,"Consulta",None,"Metadatos","Administrador")
    return render(request, 'metadatos.html', {'metadatos': metadatos, 'mensaje': 'Metadatos','user_log':user_log})

# @login_required(redirect_field_name='login')
def ListarMetadatosTipoEXp(request,pk):
    user_log = PerfilUser.objects.get(pk=request.user.pk)
    metadatos = Metadato.objects.filter(tipo_expediente=pk)
    # Instanciando TipoExpediente
    tipo_expediente_dos = TipoExpediente()
    tipo_expediente_dos = TipoExpediente.objects.get(pk=pk)
    tipo = tipo_expediente_dos
    # metadatos = Metadato.objects.all()
    registro_log_admin(user_log,"Consulta",None,"Metadato","Administrador")
    return render(request, 'metadatos.html', {'metadatos': metadatos,'tipo': tipo, 'mensaje': 'Agregar metadatos','user_log':user_log})

# @login_required(redirect_field_name='login')
def MetadatoTipoExp(request,pk):
    user_log = PerfilUser.objects.get(pk=request.user.pk)
    # return HttpResponse(request.POST.items())
    # Instanciando TipoExpediente
    tipo_expediente_dos = TipoExpediente()
    tipo_expediente_dos = TipoExpediente.objects.get(pk=pk)
    if request.method == "POST":
        form = MetadatoForm(request.POST)
        metadato = None
        if form.is_valid():
            # Instanciando Estatus
            estatus_dos = Estatus()  
            estatus_dos = Estatus.objects.get(nombre='Creado')
            # Instanciando TipoDato
            tipo_dato_dos = TipoDato()
            tipo_dato_dos = TipoDato.objects.get(pk=request.POST['tipo_dato'])
            # Instanciando TipoExpediente
            # tipo_expediente_dos = TipoExpediente()
            # tipo_expediente_dos = TipoExpediente.objects.get(pk=pk)
            # Asignando el valor de obligatorio
            if request.POST.get('obligatorio','') == 'on':
                obligatorio_dos = True
            else:
                obligatorio_dos = False
            metadato = Metadato.objects.create(
                nombre = request.POST.get('nombre',''),
                descripcion = request.POST.get('descripcion',''),
                obligatorio = obligatorio_dos,
                valor = request.POST.get('valor',''),
                version = request.POST.get('version',''),
                motivo_rechazo = request.POST.get('motivo_rechazo',''),
                tipo_dato = tipo_dato_dos,
                tipo_expediente = tipo_expediente_dos,
                estatus = estatus_dos,
                base = 1,
            )
            metadato.save()
            tipo = tipo_expediente_dos
            metadatos = Metadato.objects.filter(tipo_expediente=pk)
            # return render(request, 'metadatos.html', {'tipo': tipo,})
            registro_log_admin(user_log,"Crea",metadato,"Metadato","Administrador")
            return render(request, 'metadatos.html', {'metadatos': metadatos,'tipo': tipo, 'mensaje': 'Agregar metadatos','user_log':user_log})
            # return redirect('/metadatos/')
    else:
        form = MetadatoForm()
    return render(request, 'nuevo_metadato.html', {'form': form,'tipo':tipo_expediente_dos , 'nuevo': 'Nuevo','user_log':user_log, 'mensaje': 'Nuevo metadato'})

# @login_required(redirect_field_name='login')
def NuevoMetadato(request):
    user_log = PerfilUser.objects.get(pk=request.user.pk)
    if request.method == "POST":
        form = MetadatoForm(request.POST)
        metadato = None
        if form.is_valid():
            user = request.user
            # Instanciando Estatus
            estatus_dos = Estatus()  
            estatus_dos = Estatus.objects.get(nombre='Creado')
            # Instanciando TipoDato
            tipo_dato_dos = TipoDato()
            tipo_dato_dos = TipoDato.objects.get(pk=request.POST['tipo_dato'])
            # Instanciando TipoExpediente
            tipo_expediente_dos = TipoExpediente()
            tipo_expediente_dos = TipoExpediente.objects.get(pk=request.POST['tipo'])
            # Asignando el valor de obligatorio
            if request.POST.get('obligatorio','') == 'on':
                obligatorio_dos = True
            else:
                obligatorio_dos = False
            metadato = Metadato.objects.create(
                nombre = request.POST.get('nombre',''),
                descripcion = request.POST.get('descripcion',''),
                obligatorio = obligatorio_dos,
                valor = request.POST.get('valor',''),
                version = request.POST.get('version',''),
                motivo_rechazo = request.POST.get('motivo_rechazo',''),
                tipo_dato = tipo_dato_dos,
                tipo_expediente = tipo_expediente_dos,
                estatus = estatus_dos,
                expediente = request.POST.get('expediente',''),
                base = 1,
            )
            metadato.save()
            registro_log_admin(user_log,"Crea",metadato,"Metadato","Administrador")
            return redirect('/metadatos/')
    else:
        form = MetadatoForm()
    return render(request, 'nuevo_metadato.html', {'form': form, 'nuevo': 'Nuevo','user_log':user_log, 'mensaje':'Nuevo metadato'})

# @login_required(redirect_field_name='login')
def EditarMetadato(request, pk):
    user_log = PerfilUser.objects.get(pk=request.user.pk)
    try:
        metadato = Metadato.objects.get(pk=pk)
        if request.method == "POST":
            form = MetadatoForm(request.POST, instance=metadato)
            if form.is_valid():
                metadato = form.save()
                metadato.save()
                # return redirect('/metadatos/')
                tipo = metadato.tipo_expediente
                metadatos = Metadato.objects.filter(tipo_expediente=metadato.tipo_expediente.pk)
                registro_log_admin(user_log,"Modifica",metadato,"Metadato","Administrador")
                return render(request, 'metadatos.html', {'metadatos': metadatos,'tipo': tipo, 'mensaje': 'Agregar metadatos','user_log':user_log})
        else:
            form = MetadatoForm(instance=metadato)
        return render(request, 'edita_metadato.html', {'form': form, 'mensaje': 'Modificar metadato','user_log':user_log, 'metadato':metadato})
    except ObjectDoesNotExist:
        return redirect('/metadatos/')

# @login_required(redirect_field_name='login')
def EliminaMetadato(request, pk):
    user_log = PerfilUser.objects.get(pk=request.user.pk)
    try:
        metadato = Metadato.objects.get(pk=pk)
        # return redirect('/metadatos/')
        tipo = metadato.tipo_expediente
        metadatos = Metadato.objects.filter(tipo_expediente=metadato.tipo_expediente.pk)
        metadato.delete()
        registro_log_admin(user_log,"Elimina",metadato,"Metadato","Administrador")
        return render(request, 'metadatos.html', {'metadatos': metadatos,'tipo': tipo, 'mensaje': 'Agregar metadatos','user_log':user_log})
    except ObjectDoesNotExist:
        return redirect('/metadatos/')

# @login_required(redirect_field_name='login')
def VerMetadato(request, pk):
    user_log = PerfilUser.objects.get(pk=request.user.pk)
    try:
        metadato = Metadato.objects.get(pk=pk)
        registro_log_admin(user_log,"Consulta",metadato,"Metadato","Administrador")
        return render(request, 'metadatos.html', {'metadatos': metadato,'user_log':user_log})
    except ObjectDoesNotExist:
        return redirect('principal')