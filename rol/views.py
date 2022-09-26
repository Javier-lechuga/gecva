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
from usuarios.models import PerfilUser
from expediente.views import registro_log_admin

# Create your views here.
# @login_required(redirect_field_name='login')
def ListarRoles(request):
    user_log = PerfilUser.objects.get(pk=request.user.pk)
    roles = Rol.objects.all()
    registro_log_admin(user_log,"Consulta",None,"Roles","Administrador")
    return render(request, 'roles.html', {'roles': roles, 'mensaje': 'Roles','user_log':user_log})

# @login_required(redirect_field_name='login')
def NuevoRol(request):
    user_log = PerfilUser.objects.get(pk=request.user.pk)
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
            registro_log_admin(user_log,"Crea",rol,"Rol","Administrador")
            return redirect('/roles/')
            #return render(request,'roles.html',{'roles/':rol})
    else:
        form = RolForm()
    return render(request, 'nuevo_rol.html', {'form': form, 'nuevo': 'Nuevo','user_log':user_log})

# @login_required(redirect_field_name='login')
def EditarRol(request, pk):
    user_log = PerfilUser.objects.get(pk=request.user.pk)
    try:
        rol = Rol.objects.get(pk=pk)
        if request.method == "POST":
            form = RolForm(request.POST, instance=rol)
            if form.is_valid():
                rol = form.save()
                rol.save()
                registro_log_admin(user_log,"Edita",rol,"Rol","Administrador")
                return redirect('/roles/')
                #return render(request, 'roles.html', {'roles/': unidad})
        else:
            form = RolForm(instance=rol)
        return render(request, 'edita_rol.html', {'form': form, 'mensaje': 'Modificar rol','user_log':user_log})
    except ObjectDoesNotExist:
        return redirect('/roles/')

# @login_required(redirect_field_name='login')
def EliminarRol(request, pk):
    try:
        user_log = PerfilUser.objects.get(pk=request.user.pk)
        rol = Rol.objects.get(pk=pk)
        rol.delete()
        registro_log_admin(user_log,"Elimina",rol,"Rol","Administrador")
        return redirect('/roles/')
    except ObjectDoesNotExist:
        return redirect('/roles/')

# @login_required(redirect_field_name='login')
def VerRol(request, pk):
    user_log = PerfilUser.objects.get(pk=request.user.pk)
    try:
        rol = Rol.objects.get(pk=pk)
        registro_log_admin(user_log,"Consulta",rol,"Rol","Administrador")
        return render(request, 'roles.html', {'rol': rol,'user_log':user_log})
    except ObjectDoesNotExist:
        return redirect('principal')