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

# Create your views here.
# @login_required(redirect_field_name='login')
def ListarMetadatos(request):
    metadatos = Metadato.objects.all()
    return render(request, 'metadatos.html', {'metadatos': metadatos, 'mensaje': 'Metadatos'})

# @login_required(redirect_field_name='login')
def ListarMetadatosTipoEXp(request,pk):
    metadatos = Metadato.objects.filter(tipo_expediente=pk, vista=False)
    # Instanciando TipoExpediente
    tipo_expediente_dos = TipoExpediente()
    tipo_expediente_dos = TipoExpediente.objects.get(pk=pk)
    tipo = tipo_expediente_dos
    # metadatos = Metadato.objects.all()
    return render(request, 'metadatos.html', {'metadatos': metadatos,'tipo': tipo, 'mensaje': 'Metadatos'})

# @login_required(redirect_field_name='login')
def MetadatoTipoExp(request,pk):
    # return HttpResponse(request.POST.items())
    if request.method == "POST":
        form = MetadatoForm(request.POST)
        metadato = None
        if form.is_valid():
            user = request.user
            # Instanciando Estatus
            # @cambio
            # fecha : 28/03/2020
            # autor: lechuga
            # Explcación: cambie para que busque el estatus y no el pk
            estatus_dos = Estatus()  
            estatus_dos = Estatus.objects.get(nombre='Creado')
            # @Anteriro 
            #estatus_dos = Estatus()
            #estatus_dos = Estatus.objects.get(pk=7) # Estableciendo el estatus como creado
            # Instanciando TipoDato
            tipo_dato_dos = TipoDato()
            tipo_dato_dos = TipoDato.objects.get(pk=request.POST['tipo_dato'])
            # Instanciando TipoExpediente
            tipo_expediente_dos = TipoExpediente()
            tipo_expediente_dos = TipoExpediente.objects.get(pk=pk)
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
            )
            metadato.save()
            tipo = tipo_expediente_dos
            metadatos = Metadato.objects.filter(tipo_expediente=pk)
            # return render(request, 'metadatos.html', {'tipo': tipo,})
            return render(request, 'metadatos.html', {'metadatos': metadatos,'tipo': tipo, 'mensaje': 'Metadatos'})
            # return redirect('/metadatos/')
    else:
        form = MetadatoForm()
    return render(request, 'nuevo_metadato.html', {'form': form, 'nuevo': 'Nuevo'})

# @login_required(redirect_field_name='login')
def NuevoMetadato(request):
    if request.method == "POST":
        form = MetadatoForm(request.POST)
        metadato = None
        if form.is_valid():
            user = request.user
            # Instanciando Estatus
            # @cambio
            # fecha : 28/03/2020
            # autor: lechuga
            # Explcación: cambie para que busque el estatus y no el pk    
            estatus_dos = Estatus.objects.get(nombre = 'Creado') 
            # @Anteriro 
            #estatus_dos = Estatus()
            #estatus_dos = Estatus.objects.get(pk=7) # Estableciendo el estatus como creado
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
            )
            metadato.save()
            return redirect('/metadatos/')
    else:
        form = MetadatoForm()
    return render(request, 'nuevo_metadato.html', {'form': form, 'nuevo': 'Nuevo'})

# @login_required(redirect_field_name='login')
def EditarMetadato(request, pk):
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
                return render(request, 'metadatos.html', {'metadatos': metadatos,'tipo': tipo, 'mensaje': 'Metadatos'})
        else:
            form = MetadatoForm(instance=metadato)
        return render(request, 'edita_metadato.html', {'form': form, 'mensaje': 'Modificar metadato'})
    except ObjectDoesNotExist:
        return redirect('/metadatos/')

# @login_required(redirect_field_name='login')
def EliminaMetadato(request, pk):
    try:
        metadato = Metadato.objects.get(pk=pk)
        # return redirect('/metadatos/')
        tipo = metadato.tipo_expediente
        metadatos = Metadato.objects.filter(tipo_expediente=metadato.tipo_expediente.pk)
        metadato.delete()
        return render(request, 'metadatos.html', {'metadatos': metadatos,'tipo': tipo, 'mensaje': 'Metadatos'})
    except ObjectDoesNotExist:
        return redirect('/metadatos/')

# @login_required(redirect_field_name='login')
def VerMetadato(request, pk):
    try:
        metadato = Metadato.objects.get(pk=pk)
        return render(request, 'metadatos.html', {'metadatos': metadato})
    except ObjectDoesNotExist:
        return redirect('principal')