# -*- coding: utf-8 -*-
from asyncio.windows_events import NULL
from django.shortcuts import render
from unidad.forms import UnidadForm
from django.contrib.auth.decorators import permission_required, login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User
import datetime

import json
import time


from unidad.models import Unidad

# Create your views here.
# @login_required(redirect_field_name='login')
def ListarUnidades(request):
    unidades = Unidad.objects.all()
    return render(request, 'unidades.html', {'unidades': unidades, 'mensaje': 'Unidades'})

# @login_required(redirect_field_name='login')
def NuevaUnidad(request):
    if request.method == "POST":
        form = UnidadForm(request.POST)
        unidad = None
        if form.is_valid():
            user = request.user
            # Instanciando Jefe_inmediato
            jefe_unidad_dos = User()
            if request.POST['jefe_unidad']:
                jefe_unidad_dos = User.objects.get(pk=request.POST['jefe_unidad'])
            else:
                # Si no cuenta con jefe de unidad se asigna automaticamente al superusuario del sistema
                jefe_unidad_dos = User.objects.get(pk=1)
            unidad = Unidad.objects.create(
                nombre = request.POST.get('nombre',''),
                descripcion = request.POST.get('descripcion',''),
                jefe_unidad = jefe_unidad_dos,
            )
            unidad.save()
            return redirect('/unidad/')
            #return render(request,'unidades.html',{'unidad/':unidad})
    else:
        form = UnidadForm()
    return render(request, 'nueva_unidad.html', {'form': form, 'nuevo': 'Nuevo'})

# @login_required(redirect_field_name='login')
def EditarUnidad(request, pk):
    try:
        unidad = Unidad.objects.get(pk=pk)
        if request.method == "POST":
            form = UnidadForm(request.POST, instance=unidad)
            if form.is_valid():
                unidad = form.save()
                unidad.save()
                return redirect('/unidad/')
                #return render(request, 'unidades.html', {'unidad/': unidad})
        else:
            form = UnidadForm(instance=unidad)
        return render(request, 'edita_unidad.html', {'form': form, 'mensaje': 'Modificar unidad'})
    except ObjectDoesNotExist:
        return redirect('/unidad/')

# @login_required(redirect_field_name='login')
# def EliminarUnidad(request, pk):
#     try:
#         unidad = Unidad.objects.get(pk=pk)
#         unidad.delete()
#         return redirect('/unidad/')
#     except ObjectDoesNotExist:
#         return redirect('/unidad/')

# @login_required(redirect_field_name='login')
def EliminarUnidad(request, pk):
    try:
        unidad = Unidad.objects.get(pk=pk)
        Unidad.objects.filter(pk=pk).update(activo=False)
        return redirect('/unidad/')
    except ObjectDoesNotExist:
        return redirect('/unidad/')

# @login_required(redirect_field_name='login')
def VerUnidad(request, pk):
    try:
        unidad = Unidad.objects.get(pk=pk)
        return render(request, 'unidad.html', {'unidad': unidad})
    except ObjectDoesNotExist:
        return redirect('principal')