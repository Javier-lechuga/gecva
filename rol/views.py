# -*- coding: utf-8 -*-
from django.shortcuts import render
from rol.forms import RolForm
from django.contrib.auth.decorators import permission_required, login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
import datetime

import json
import time


from rol.models import Rol

# Create your views here.
# @login_required(redirect_field_name='login')
def ListarRoles(request):
    roles = Rol.objects.all()
    return render(request, 'roles.html', {'roles': roles, 'mensaje': 'Roles'})

# @login_required(redirect_field_name='login')
def NuevoRol(request):
    if request.method == "POST":
        form = RolForm(request.POST)
        rol = None
        if form.is_valid():
            user = request.user
            rol = Rol.objects.create(
                nombre = request.POST.get('nombre',''),
                descripcion = request.POST.get('descripcion',''),
            )
            rol.save()
            return redirect('/roles/')
            #return render(request,'roles.html',{'roles/':rol})
    else:
        form = RolForm()
    return render(request, 'nuevo_rol.html', {'form': form, 'nuevo': 'Nuevo'})

# @login_required(redirect_field_name='login')
def EditarRol(request, pk):
    try:
        rol = Rol.objects.get(pk=pk)
        if request.method == "POST":
            form = RolForm(request.POST, instance=rol)
            if form.is_valid():
                rol = form.save()
                rol.save()
                return redirect('/roles/')
                #return render(request, 'roles.html', {'roles/': unidad})
        else:
            form = RolForm(instance=rol)
        return render(request, 'edita_rol.html', {'form': form, 'mensaje': 'Modificar rol'})
    except ObjectDoesNotExist:
        return redirect('/roles/')

# @login_required(redirect_field_name='login')
def EliminarRol(request, pk):
    try:
        rol = Rol.objects.get(pk=pk)
        rol.delete()
        return redirect('/roles/')
    except ObjectDoesNotExist:
        return redirect('/roles/')

# @login_required(redirect_field_name='login')
def VerRol(request, pk):
    try:
        rol = Rol.objects.get(pk=pk)
        return render(request, 'roles.html', {'rol': rol})
    except ObjectDoesNotExist:
        return redirect('principal')