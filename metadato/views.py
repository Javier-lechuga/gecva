# -*- coding: utf-8 -*-
from django.shortcuts import render
from estatus.models import Estatus
from metadato.forms import MetadatoForm
from django.contrib.auth.decorators import permission_required, login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
import datetime

import json
import time


from metadato.models import Metadato
from tipo_dato.models import TipoDato

# Create your views here.
# @login_required(redirect_field_name='login')
def ListarMetadatos(request):
    metadatos = Metadato.objects.all()
    return render(request, 'metadatos.html', {'metadatos': metadatos, 'mensaje': 'Metadatos'})

# @login_required(redirect_field_name='login')
def NuevoMetadato(request):
    if request.method == "POST":
        form = MetadatoForm(request.POST)
        metadato = None
        if form.is_valid():
            user = request.user
            # Instanciando Estatus
            estatus_dos = Estatus()
            estatus_dos = Estatus.objects.get(pk=request.POST['estatus'])
            # Instanciando TipoDato
            tipo_dato_dos = TipoDato()
            tipo_dato_dos = TipoDato.objects.get(pk=request.POST['tipo_dato'])
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
                estatus = estatus_dos,
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
                return redirect('/metadatos/')
        else:
            form = MetadatoForm(instance=metadato)
        return render(request, 'edita_metadato.html', {'form': form, 'mensaje': 'Modificar metadato'})
    except ObjectDoesNotExist:
        return redirect('/metadatos/')

# @login_required(redirect_field_name='login')
def EliminaMetadato(request, pk):
    try:
        metadato = Metadato.objects.get(pk=pk)
        metadato.delete()
        return redirect('/metadatos/')
    except ObjectDoesNotExist:
        return redirect('/metadatos/')

# @login_required(redirect_field_name='login')
def VerMetadato(request, pk):
    try:
        metadato = Metadato.objects.get(pk=pk)
        return render(request, 'metadatos.html', {'metadatos': metadato})
    except ObjectDoesNotExist:
        return redirect('principal')