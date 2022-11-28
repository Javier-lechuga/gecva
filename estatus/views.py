# .\estatus\views.py

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
from usuarios.models import PerfilUser
from expediente.views import registro_log_admin

# No se puede acceder a las vistas a menos que se este logueado en el sistema
# Falta configurar el LOG en los perfiles
# Nota en lugar de esta funcionalida se implementaron las "Fixtures" se recomienda seguir utilizandolas

# Create your views here.
# @login_required(redirect_field_name='login')
def ListarEstatus(request):
    user_log = PerfilUser.objects.get(pk=request.user.pk)
    estatus = Estatus.objects.all()
    registro_log_admin(user_log,"Consulta",None,"Estatus","Administrador")
    return render(request, 'estatus.html', {'estatus': estatus, 'mensaje': 'Estatus','user_log':user_log})

# @login_required(redirect_field_name='login')
def NuevoEstatus(request):
    user_log = PerfilUser.objects.get(pk=request.user.pk)
    if request.method == "POST":
        form = EstatusForm(request.POST)
        estatus = None
        if form.is_valid():
            user = request.user
            estatus = Estatus.objects.create(
                nombre = request.POST.get('nombre',''),
            )
            estatus.save()
            registro_log_admin(user_log,"Crea",estatus,"Estatus","Administrador")
            return redirect('/estatus/')
            #return render(request,'estatus.html',{'estatus/':estatus})
    else:
        form = EstatusForm()
    return render(request, 'nuevo_estatus.html', {'form': form, 'nuevo': 'Nuevo','user_log':user_log})

# @login_required(redirect_field_name='login')
def EditarEstatus(request, pk):
    user_log = PerfilUser.objects.get(pk=request.user.pk)
    try:
        estatus = Estatus.objects.get(pk=pk)
        if request.method == "POST":
            form = EstatusForm(request.POST, instance=estatus)
            if form.is_valid():
                estatus = form.save()
                estatus.save()
                registro_log_admin(user_log,"Edita",estatus,"Estatus","Administrador")
                return redirect('/estatus/')
                #return render(request, 'estatus.html', {'estatus/': estatus})
        else:
            form = EstatusForm(instance=estatus)
        return render(request, 'edita_estatus.html', {'form': form, 'mensaje': 'Modificar estatus','user_log':user_log})
    except ObjectDoesNotExist:
        return redirect('/estatus/')

# @login_required(redirect_field_name='login')
def EliminarEstatus(request, pk):
    try:
        user_log = PerfilUser.objects.get(pk=request.user.pk)
        estatus = Estatus.objects.get(pk=pk)
        estatus.delete()
        registro_log_admin(user_log,"Elimina",estatus,"Estatus","Administrador")
        return redirect('/estatus/')
    except ObjectDoesNotExist:
        return redirect('/estatus/')

# @login_required(redirect_field_name='login')
def VerEstatus(request, pk): # No se usa
    user_log = PerfilUser.objects.get(pk=request.user.pk)
    try:
        estatus = Estatus.objects.get(pk=pk)
        registro_log_admin(user_log,"Consulta",estatus,"Estatus","Administrador")
        return render(request, 'estatus.html', {'estatus': estatus,'user_log':user_log})
    except ObjectDoesNotExist:
        return redirect('principal')