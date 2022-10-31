# -*- coding: utf-8 -*-
from asyncio.windows_events import NULL
from turtle import update
from django.http import HttpResponse
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
from usuarios.models import PerfilUser
from expediente.views import registro_log_admin

# Create your views here.
# @login_required(redirect_field_name='login')
def ListarUnidades(request):
    user_log = PerfilUser.objects.get(pk=request.user.pk)
    registro_log_admin(user_log,"Consulta",None,"Unidades","Administrador")
    unidades = Unidad.objects.all()
    return render(request, 'unidades.html', {'unidades': unidades, 'mensaje': 'Unidades','user_log':user_log})

# @login_required(redirect_field_name='login')
def NuevaUnidad(request):
    user_log = PerfilUser.objects.get(pk=request.user.pk)
    usuarios = PerfilUser.objects.all().exclude(is_active=False).order_by('pk')
    if request.method == "POST":
        form = UnidadForm(request.POST)
        unidad = None
        # if form.is_valid():
        user = request.user
        # Instanciando Jefe_inmediato
        jefe_unidad_dos = PerfilUser()
        if request.POST['jefe_unidad']:
            jefe_unidad_dos = PerfilUser.objects.get(pk=request.POST['jefe_unidad'])
        else:
            # Si no cuenta con jefe de unidad se asigna automaticamente al superusuario del sistema
            jefe_unidad_dos = User.objects.get(pk=1)
        try:
            unidad = Unidad.objects.create(
                nombre = request.POST.get('nombre',''),
                siglas = request.POST.get('siglas',''),
                descripcion = request.POST.get('descripcion',''),
                jefe_unidad = jefe_unidad_dos,
            )
            unidad.save()
            registro_log_admin(user_log,"Crea",unidad,"Unidad","Administrador")
            # return redirect('/unidad/')
        except:
            return render(request, 'nueva_unidad.html', {'form': form, 'nuevo': 'Nuevo', 'usuarios': usuarios,'user_log':user_log})
    else:
        form = UnidadForm()
    return render(request, 'nueva_unidad.html', {'form': form, 'nuevo': 'Nuevo', 'usuarios': usuarios,'user_log':user_log, 'mensaje': 'Nueva unidad'})

# @login_required(redirect_field_name='login')
def UnidadNuevaDesdeUsuario(request):
    user_log = PerfilUser.objects.get(pk=request.user.pk)
    usuarios = PerfilUser.objects.all().exclude(is_active=False).order_by('pk')
    
    if request.method == "POST":
        form = UnidadForm(request.POST)
        unidad = None
        # Instanciando Jefe_inmediato
        jefe_unidad_dos = PerfilUser()
        if request.POST['jefe_unidad']:
            jefe_unidad_dos = PerfilUser.objects.get(pk=request.POST['jefe_unidad'])
        else:
            # Si no cuenta con jefe de unidad se asigna automaticamente al superusuario del sistema
            jefe_unidad_dos = User.objects.get(pk=1)
        try:
            unidad = Unidad.objects.create(
                nombre = request.POST.get('nombre',''),
                siglas = request.POST.get('siglas',''),
                descripcion = request.POST.get('descripcion',''),
                jefe_unidad = jefe_unidad_dos,
            )
            unidad.save()
            #registro_log_admin(user_log,"Crea",unidad,"Unidad","Administrador")
            #return redirect('/unidad/')
            return render(request, 'nuevo_usuario.html', {'form': form, 'nuevo': 'Nuevo', 'usuarios': usuarios,'user_log':user_log, 'unidades': unidades})
        except:
            # return HttpResponse(request.POST.items())
            unidades = Unidad.objects.all()
            return render(request, 'nuevo_usuario.html', {'form': form, 'nuevo': 'Nuevo', 'usuarios': usuarios,'user_log':user_log, 'unidades': unidades})
    else:
        form = UnidadForm()
    # return HttpResponse(request.POST.items())
    unidades = Unidad.objects.all()
    return render(request, 'nuevo_usuario.html', {'form': form, 'nuevo': 'Nuevo', 'usuarios': usuarios,'user_log':user_log, 'mensaje': 'Nuevo usuario', 'unidades': unidades})

# @login_required(redirect_field_name='login')
def EditarUnidad(request, pk):
    user_log = PerfilUser.objects.get(pk=request.user.pk)
    unidad = Unidad.objects.get(pk=pk)
    usuarios = PerfilUser.objects.filter(unidad_user=unidad.pk, rol=2).exclude(is_active=False).order_by('pk')
    if request.method == "POST":
        contador = 0
        if Unidad.objects.filter(nombre=request.POST.get('nombre','')).exclude(pk=unidad.pk).exists():
            contador = 1
        if Unidad.objects.filter(siglas=request.POST.get('siglas','')).exclude(pk=unidad.pk).exists():
            contador = 2
        if contador == 1:
            return render(request, 'edita_unidad.html', {'unidad': unidad,'mensaje': 'Modificar unidad','usuarios': usuarios,'user_log':user_log, 'error':'nombre'})
        if contador == 2:
            return render(request, 'edita_unidad.html', {'unidad': unidad,'mensaje': 'Modificar unidad','usuarios': usuarios,'user_log':user_log, 'error':'siglas'})
        if contador == 0:
            # return HttpResponse(request.POST.items())
            Unidad.objects.filter(pk=pk).update(nombre=request.POST['nombre'])
            Unidad.objects.filter(pk=pk).update(siglas=request.POST['siglas'])
            Unidad.objects.filter(pk=pk).update(descripcion=request.POST['descripcion'])
            # Instanciando el jefe de unidad
            jefe = PerfilUser()
            jefe = PerfilUser.objects.get(pk=request.POST['jefe_unidad'])
            Unidad.objects.filter(pk=pk).update(jefe_unidad=jefe)
            if request.POST['activo'] == 'on':
                Unidad.objects.filter(pk=pk).update(activo=True)
            else:
                Unidad.objects.filter(pk=pk).update(activo=False)
            registro_log_admin(user_log,"Modifica",unidad,"Unidad","Administrador")

        return redirect('/unidad/')
    else:
        return render(request, 'edita_unidad.html', {'unidad': unidad,'mensaje': 'Modificar unidad','usuarios': usuarios,'user_log':user_log})
        
def EliminarUnidad(request, pk):
    try:
        user_log = PerfilUser.objects.get(pk=request.user.pk)
        unidad = Unidad.objects.get(pk=pk)
        Unidad.objects.filter(pk=pk).update(activo=False)
        registro_log_admin(user_log,"Elimina",unidad,"Unidad","Administrador")
        return redirect('/unidad/')
    except ObjectDoesNotExist:
        return redirect('/unidad/')

# @login_required(redirect_field_name='login')
def VerUnidad(request, pk):
    user_log = PerfilUser.objects.get(pk=request.user.pk)
    try:
        unidad = Unidad.objects.get(pk=pk)
        registro_log_admin(user_log,"Consulta",unidad,"Unidad","Administrador")
        return render(request, 'unidad.html', {'unidad': unidad,'user_log':user_log})
    except ObjectDoesNotExist:
        return redirect('principal')