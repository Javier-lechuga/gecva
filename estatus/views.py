# -*- coding: utf-8 -*-
from django.shortcuts import render
from estatus.forms import EstatusForm
from django.contrib.auth.decorators import permission_required, login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
import datetime

import json
import time


from estatus.models import Estatus

# Create your views here.
# @login_required(redirect_field_name='login')
def ListarEstatus(request):
    estatus = Estatus.objects.all()
    return render(request, 'estatus.html', {'estatus': estatus, 'mensaje': 'Estatus'})

# @login_required(redirect_field_name='login')
def NuevoEstatus(request):
    if request.method == "POST":
        form = EstatusForm(request.POST)
        estatus = None
        if form.is_valid():
            user = request.user
            estatus = Estatus.objects.create(
                nombre = request.POST.get('nombre',''),
            )
            estatus.save()
            return redirect('/estatus/')
            #return render(request,'estatus.html',{'estatus/':estatus})
    else:
        form = EstatusForm()
    return render(request, 'nuevo_estatus.html', {'form': form, 'nuevo': 'Nuevo'})

# @login_required(redirect_field_name='login')
def EditarEstatus(request, pk):
    try:
        estatus = Estatus.objects.get(pk=pk)
        if request.method == "POST":
            form = EstatusForm(request.POST, instance=estatus)
            if form.is_valid():
                estatus = form.save()
                estatus.save()
                return redirect('/estatus/')
                #return render(request, 'estatus.html', {'estatus/': estatus})
        else:
            form = EstatusForm(instance=estatus)
        return render(request, 'edita_estatus.html', {'form': form, 'mensaje': 'Modificar estatus'})
    except ObjectDoesNotExist:
        return redirect('/estatus/')

# @login_required(redirect_field_name='login')
def EliminarEstatus(request, pk):
    try:
        estatus = Estatus.objects.get(pk=pk)
        estatus.delete()
        return redirect('/estatus/')
    except ObjectDoesNotExist:
        return redirect('/estatus/')

# @login_required(redirect_field_name='login')
def VerEstatus(request, pk):
    try:
        estatus = Estatus.objects.get(pk=pk)
        return render(request, 'estatus.html', {'estatus': estatus})
    except ObjectDoesNotExist:
        return redirect('principal')