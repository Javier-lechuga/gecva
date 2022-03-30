# -*- coding: utf-8 -*-
from django.shortcuts import render
from estatus.models import Estatus
import expediente
from expediente.forms import ExpedienteForm
from django.contrib.auth.decorators import permission_required, login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import get_user
from django.http import HttpResponse
import datetime

import json
import time


from expediente.models import Expediente
from metadato.forms import MetadatoForm
from metadato.models import Metadato
from tipo_dato.models import TipoDato
import tipo_expediente
from tipo_expediente.models import TipoExpediente
from unidad.models import Unidad

#Para cargar expediente
from django.core.files.storage import default_storage

from usuarios.models import PerfilUser
#

# Create your views here.
# @login_required(redirect_field_name='login')
def ListarExpedientes(request):
    expedientes = Expediente.objects.all()
    return render(request, 'expedientes.html', {'expedientes': expedientes, 'mensaje': 'Expedientes'})

# @login_required(redirect_field_name='login')
def ListarExpUnidad(request, pk):
    # expedientes = Expediente.objects.all()
    expedientes = Expediente.objects.filter(unidad=pk)
    return render(request, 'expedientes.html', {'expedientes': expedientes, 'mensaje': 'Expedientes'})

# @login_required(redirect_field_name='login')
def NuevoExpediente(request):
    if request.method == "POST":
        form = ExpedienteForm(request.POST)
        expediente = None
        if form.is_valid():
             # Instanciando Estatus
            # @cambio
            # fecha : 28/03/2020
            # autor: lechuga
            # Explcación: cambie para que busque el estatus y no el pk    
            estatus_dos = Estatus.objects.get(nombre = 'Creado') 
            # @Anteriro 
            #estatus_dos = Estatus()
            #estatus_dos = Estatus.objects.get(pk=7) # Estableciendo el estatus como creado
            tipo_expediente_dos = TipoExpediente()
            tipo_expediente_dos = TipoExpediente.objects.get(pk=request.POST['tipo'])
            # Instanciando Unidad
            unidad_dos = Unidad()
            unidad_dos = Unidad.objects.get(pk=request.POST['unidad'])
            # Asignando el valor de activo
            if request.POST.get('activo','') == 'on':
                activo_dos = True
            else:
                activo_dos = False
            user = get_user(request)
            user = request.user
            expediente = Expediente.objects.create(
                identificador = request.POST.get('identificador',''),
                nombre = request.POST.get('nombre',''),
                descripcion = request.POST.get('descripcion',''),
                asunto = request.POST.get('asunto',''),
                ubicacion = request.POST.get('ubicacion',''),
                fecha_creacion = datetime.datetime.now(),
                estatus = estatus_dos,
                tipo_expediente = tipo_expediente_dos,
                unidad = unidad_dos,
                activo = activo_dos,
                usuario_crea = user
            )
            expediente.save()
            nuevo_expediente = Expediente.objects.filter(identificador=request.POST.get('identificador',''))
            # return redirect('/expedientes/lista_metadatos_exp')
            id = 0
            for exp in nuevo_expediente:
                id = exp.pk
            print(id)
            return redirect('/expedientes/lista_metadatos_exp?pk=%s&id=%s' % (expediente.tipo_expediente.pk, id))
            # return render(request, '/expedientes/lista_metadatos_exp', {'pk': expediente.tipo_expediente, 'id': nuevo_expediente.pk})
    else:
        form = ExpedienteForm()
    return render(request, 'nuevo_expediente.html', {'form': form, 'nuevo': 'Nuevo'})

# @login_required(redirect_field_name='login')
def BuscaMetadatosExp(request):
    metadatos = Metadato.objects.filter(tipo_expediente=request.POST['tipo'], base =1)
    expediente = ExpedienteForm()
    tipo = TipoExpediente()
    tipo = TipoExpediente.objects.get(pk=request.POST['tipo'])
    return render(request, 'nuevo_exp_completo.html', {'tipo': tipo, 'expediente': expediente, 'metadatos': metadatos, 'mensaje': 'Nuevo expediente'})

# @login_required(redirect_field_name='login')
def NuevoExpCompleto(request):
    if request.method == "POST":
        # return HttpResponse(request.POST.items())
        form = ExpedienteForm(request.POST)
        expediente = None
        # CREANDO EL EXPEDIENTE
        user = get_user(request)
        user = request.user
        # Instanciando Estatus
        estatus_expediente = Estatus()
        estatus_expediente = Estatus.objects.get(nombre = 'Creado')
        #Instanciando Tipo_expediente
        tipo_expediente_exp = TipoExpediente()
        tipo_expediente_exp = TipoExpediente.objects.get(pk=request.POST['tipo'])
        #Instanciando el PerfilUser
        perfil = PerfilUser()
        perfil = PerfilUser.objects.get(pk=user)
        # Instanciando Unidad Modificar con lo del login
        unidad_expediente = Unidad()
        unidad_expediente = Unidad.objects.get(pk=perfil.unidad_user.pk)
        expediente = Expediente.objects.create(
            identificador = request.POST.get('identificador',''),
            nombre = request.POST.get('nombre',''),
            descripcion = request.POST.get('descripcion',''),
            asunto = request.POST.get('asunto',''),
            ubicacion = request.POST.get('ubicacion',''),
            fecha_creacion = datetime.datetime.now(),
            estatus = estatus_expediente,
            tipo_expediente = tipo_expediente_exp,
            unidad = unidad_expediente,
            activo = True,
            usuario_crea = user
        )
        expediente.save()
        nuevo_expediente = Expediente.objects.get(identificador=request.POST.get('identificador',''))
        # CREANDO LOS METADATOS
        metadato = None
        vars = []
        tipo = 0
        metas = []
        for variable in request.POST.items():
            vars.append(variable)
        # print(vars)
        for otro in vars[8:]:
            metas.append(otro)
            tipo = otro[0]
        # print(vars)
        # print("Este es el valor de tipo: %s" % tipo)
        # print(metas)
        for valor in metas:
            #Instanciando Metadato
            meta = Metadato()
            meta = Metadato.objects.get(pk=valor[0])
            # print(valor)
            # print(meta)
            metadato = Metadato.objects.create(
                nombre = meta.nombre,
                descripcion = meta.descripcion,
                obligatorio = meta.obligatorio,
                valor = valor[1],
                version = 1,
                tipo_dato = meta.tipo_dato,
                tipo_expediente = nuevo_expediente.tipo_expediente,
                estatus = meta.estatus,
                expediente = nuevo_expediente,
            )
            metadato.save()
        # return HttpResponse(request.POST.items())
        return redirect('/expedientes/mis_expedientes')
    else:
        form = ExpedienteForm()
    return render(request, 'nuevo_expediente.html', {'form': form, 'nuevo': 'Nuevo'})

# @login_required(redirect_field_name='login')
def ModificaExpCompleto(request):
    # return HttpResponse(request.POST.items())
    try:
        if request.method == "POST":
            expediente = Expediente.objects.get(pk=request.POST.get('expediente',''))
            exp = request.POST.get('expediente','')
            Expediente.objects.filter(pk=exp).update(nombre=request.POST.get('nombre',''))
            Expediente.objects.filter(pk=exp).update(descripcion=request.POST.get('descripcion',''))
            Expediente.objects.filter(pk=exp).update(asunto=request.POST.get('asunto',''))
            Expediente.objects.filter(pk=exp).update(ubicacion=request.POST.get('ubicacion',''))
            vars = []
            for variable in request.POST.items():
                vars.append(variable)
            print(vars)
            for otro in vars[13:]:
                Metadato.objects.filter(pk=otro[0], expediente=exp).update(valor=otro[1])
                Metadato.objects.filter(pk=otro[0], expediente=exp).update(version=2)
            # return redirect('/expedientes/mis_expedientes')
            expediente = Expediente.objects.get(pk=request.POST.get('expediente',''))
            metadatos = Metadato.objects.filter(expediente=expediente.pk)
            return render(request, 'detalle_expediente.html', {'expediente': expediente,'metadatos': metadatos, 'mensaje': 'Detalle expediente'})
        else:
            form = ExpedienteForm(instance=expediente)
        return render(request, 'edita_expediente.html', {'form': form, 'mensaje': 'Modificar expediente'})
    except ObjectDoesNotExist:
        return redirect('/expedientes/mis_expedientes')

# @login_required(redirect_field_name='login')
def DetalleExpediente(request, pk):
    try:
        expediente = Expediente.objects.get(pk=pk)
        metadatos = Metadato.objects.filter(expediente=pk)
        if request.method == "POST":
            form = ExpedienteForm(request.POST, instance=expediente)
            if form.is_valid():
                expediente = form.save()
                expediente.save()
                return redirect('/expedientes/mis_expedientes')
        # else:
            # form = ExpedienteForm(instance=expediente)
        return render(request, 'detalle_expediente.html', {'expediente': expediente, 'metadatos': metadatos, 'mensaje': 'Detalle expediente'})
    except ObjectDoesNotExist:
        return redirect('/expedientes/mis_expedientes')

# @login_required(redirect_field_name='login')
def GuardaMetadatosExp(request):
    # request.FILES
    
    # print("hola putito")
    # print(request.FILES)

    # file = request.FILES['51']
    # file_name = default_storage.save(file.name, file)

    vars = []
    for variable in request.POST.items():
        vars.append(variable)
    for otro in vars[3:]:
        Metadato.objects.filter(pk=otro[0]).update(valor=otro[1])
        Metadato.objects.filter(pk=otro[0]).update(version=1)
        Metadato.objects.filter(pk=otro[0]).update(expediente=request.POST['id_exp'])
    # return HttpResponse(vars)
    return redirect('/expedientes/mis_expedientes')

# @login_required(redirect_field_name='login')
def ListarMisExpedientes(request):
    user = get_user(request)
    user = request.user
    expedientes = Expediente.objects.filter(usuario_crea=user)
    return render(request, 'mis_expedientes.html', {'expedientes': expedientes, 'mensaje': 'Expedientes'})

# @login_required(redirect_field_name='login')
def ListaMetadatosExp(request):
    if request.method == "GET":
        tipo = TipoExpediente()
        tipo = TipoExpediente.objects.get(pk=request.GET['pk'])

        id = Expediente()
        id = Expediente.objects.get(pk=request.GET['id'])

        metadatos = Metadato.objects.filter(tipo_expediente=tipo.pk)

        #se revisa si el expediente tiene algun archivo como metadato,
        #de ser asi se le asigna true a la variable bandera, 
        #caso contrario sele asigna false  
        bandera = False
        for metadato in metadatos:
            if metadato.tipo_dato.tipo == "Archivo":
                bandera = True
                break

        #lechuga        
        #return render(request, 'lista_metadatos_exp.html', {'metadatos': metadatos, 'tipo': tipo,'mensaje': 'Metadatos','bandera':bandera})
        #rada
        #return render(request, 'lista_metadatos_exp.html', {'metadatos': metadatos, 'tipo': tipo, 'id': id,'mensaje': 'Metadatos'})
        #se cambio para regresar 
        #   metadatos : metadatos // Los metadatos que componen el expediente
        #   tipo : tipo           // El tipo de expediente
        #   id : id               // El id del expediente que se esta trabajando
        #   mensaje : 'metadatos' // Mensaje a mostrar en la pagina
        #   bandera : bandera     // variable auxiliar que representa si el expediente
        #                            tiene un metadato del tipo Archivo.
        return render(request, 'lista_metadatos_exp.html', {'metadatos': metadatos, 
                                                            'tipo': tipo, 
                                                            'id': id,
                                                            'mensaje': 'Metadatos',
                                                            'bandera': bandera
                                                            })

# @login_required(redirect_field_name='login')
def MuestraCamposExp(request):
    tipo = TipoExpediente()
    tipo = TipoExpediente.objects.get(pk=request.POST['tipo'])
    form = ExpedienteForm()
    return render(request, 'nuevo_expediente.html', {'form': form,'tipo': tipo, 'nuevo': 'Nuevo'})

# @login_required(redirect_field_name='login')
def SeleccionaTipoExp(request):
    tipos_expedientes = TipoExpediente.objects.all()
    # return redirect('/expedientes/')
    return render(request, 'selecciona_tipo_exp.html', {'tipos_expedientes': tipos_expedientes, 'mensaje': 'Expedientes'})
    

# @login_required(redirect_field_name='login')
def EditarExpediente(request, pk):
    try:
        expediente = Expediente.objects.get(pk=pk)
        if request.method == "POST":
            form = ExpedienteForm(request.POST, instance=expediente)
            if form.is_valid():
                expediente = form.save()
                expediente.save()
                return redirect('/expedientes/mis_expedientes')
        else:
            form = ExpedienteForm(instance=expediente)
        return render(request, 'edita_expediente.html', {'form': form, 'mensaje': 'Modificar expediente'})
    except ObjectDoesNotExist:
        return redirect('/expedientes/mis_expedientes')

# @login_required(redirect_field_name='login')
def EliminarExpediente(request, pk):
    try:
        expediente = Expediente.objects.get(pk=pk)
        expediente.delete()
        return redirect('/expedientes/mis_expedientes')
    except ObjectDoesNotExist:
        return redirect('/expedientes/mis_expedientes')

# @login_required(redirect_field_name='login')
def VerExpediente(request, pk):
    try:
        expediente = Expediente.objects.get(pk=pk)
        return render(request, 'expedientes.html', {'expediente': expediente})
    except ObjectDoesNotExist:
        return redirect('principal')