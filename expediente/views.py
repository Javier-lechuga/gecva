#
#
#
#
# hay que limpear los imprts
#
#
#
#
#
#

# -*- coding: utf-8 -*-
from ensurepip import version
from django.shortcuts import render
from estatus.models import Estatus
import expediente
from expediente.models import Expediente_deputy
from expediente.forms import ExpedienteForm
from django.contrib.auth.decorators import permission_required, login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import get_user
from django.http import HttpResponse
from django.contrib.auth.models import User
import datetime

import json
import time

from expediente.models import Expediente, Expediente_aprobador, Registra_actividad
from metadato.forms import MetadatoForm
from metadato.models import Metadato
from tipo_dato.models import TipoDato
import tipo_expediente
from tipo_expediente.models import TipoExpediente
from unidad.models import Unidad

#Para cargar archivos
from django.core.files.storage import default_storage
from usuarios.models import PerfilUser
#para crer directorios
from os import path
from os import makedirs
from genericpath import exists

# Create your views here.
# @login_required(redirect_field_name='login')
def ListarExpedientes(request):
    user_log = PerfilUser.objects.get(pk=request.user.pk)
    registro_log_user(user_log,"Consulta",None,"Expedientes","Usuario")
    expedientes = Expediente.objects.all()
    return render(request, 'expedientes.html', {'expedientes': expedientes, 'mensaje': 'Expedientes','user_log':user_log})

# @login_required(redirect_field_name='login')
def ListarExpUnidad(request, pk):
    user_log = PerfilUser.objects.get(pk=request.user.pk)
    registro_log_user(user_log,"Lista",None,"Expedientes","Usuario")
    expedientes = Expediente.objects.filter(unidad=pk)
    return render(request, 'expedientes.html', {'expedientes': expedientes, 'mensaje': 'Expedientes','user_log':user_log})


# @login_required(redirect_field_name='login')
def BuscaMetadatosExp(request):
    user_log = PerfilUser.objects.get(pk=request.user.pk)
    metadatos = Metadato.objects.filter(tipo_expediente=request.POST['tipo'], base =1)
    expediente = ExpedienteForm()
    tipo = TipoExpediente()
    tipo = TipoExpediente.objects.get(pk=request.POST['tipo'])
    contiene_arhivos = expediente_tine_archivos(metadatos)

    # valores retornados:
    #   tipo : tipo                     // El tipo de expediente
    #   expediente : definir            // definir el tipo
    #   metadatos : metadatos           // tupla con los metadatos que componen el expediente
    #   mensaje : 'metadatos'           // Mensaje a mostrar en la pagina
    #   contiene_archivos : bool        // variable auxiliar que representa si el expediente
    #                                      tiene un metadato del tipo Archivo.
    return render(request,
                  'nuevo_exp_completo.html',
                  {'tipo': tipo,
                   'expediente': expediente,
                   'metadatos': metadatos,
                   'mensaje': 'Nuevo expediente',
                   'contiene_archivos' : contiene_arhivos,
                   'user_log': user_log
                  })

# @login_required(redirect_field_name='login')
def VerExpediente(request, pk): # para mostrar el expediente
    user_log = PerfilUser.objects.get(pk=request.user.pk)
    usuarios = PerfilUser()
    usuarios = PerfilUser.objects.all().exclude(is_active=False, rol=3).order_by('pk')
    expediente = Expediente.objects.get(pk=pk)
    registro_log_user(user_log,"Consulta",expediente,"Expediente","Usuario")
    # now = datetime.datetime.now()
    # nom_arch = "Logs/" + now.strftime("%Y-%m-%d") + "log_user.txt"
    # with open(nom_arch,'a') as archivo:
    #     archivo.write(now.strftime("%Y-%m-%d %H:%M:%S") + " El usuario " + user_log.first_name + " " + user_log.last_name + " " + user_log.amaterno + " consulta el expediente " + expediente.identificador + "\n")
    metadatos = Metadato.objects.filter(expediente=pk).order_by('pk')
    seleccionados = []
    va = Expediente_aprobador()
    va = Expediente_aprobador.objects.filter(id_expediente=pk)
    for v in va:
        seleccionados.append(v)


    contiene_arhivos = expediente_tine_archivos(metadatos)

    #full_url = ''.join(['http://', get_current_site(request).domain, obj.get_absolute_url()])
    #url_archivo = get_current_site(request) 
    #return HttpResponse(url_archivo)

    # vaores returnados:
    #   expediente : Expediente         // Expediente a mostrar
    #   metadatos  : tupla              // tupla con todos los metadatos
    #   usuarios   : tupla              // tupla con todos los usuarios
    #   seleccionados : string          // Mensaje a mostrar en la pagina
    #   contiene_arhivos : boolean      // variable auxiliar que representa si el expediente
    #                                      tiene un metadato del tipo Archivo.

    return render(request,
                 'ver_expediente.html',
                 {'expediente': expediente,
                  'metadatos': metadatos,
                  'usuarios': usuarios,
                  'etiqueta': 'Detalle expediente',
                  'seleccionados': seleccionados,
                  'contiene_arhivos' : contiene_arhivos,
                  'user_log' : user_log
                  })

# @login_required(redirect_field_name='login')
def ConsultaExpediente(request, pk): # para mostrar el expediente
    user_log = PerfilUser.objects.get(pk=request.user.pk)
    usuarios = PerfilUser()
    usuarios = PerfilUser.objects.all().exclude(is_active=False).order_by('pk')
    expediente = Expediente.objects.get(pk=pk)
    registro_log_user(user_log,"Consulta",expediente,"Expediente","Usuario")
    metadatos = Metadato.objects.filter(expediente=pk).order_by('pk')
    seleccionados = []
    va = Expediente_aprobador()
    va = Expediente_aprobador.objects.filter(id_expediente=pk)
    for v in va:
        seleccionados.append(v)
    contiene_arhivos = expediente_tine_archivos(metadatos)
    return render(request,
                 'consulta_expediente.html',
                 {'expediente': expediente,
                  'metadatos': metadatos,
                  'usuarios': usuarios,
                  'etiqueta': 'Detalle expediente',
                  'seleccionados': seleccionados,
                  'contiene_arhivos' : contiene_arhivos,
                  'user_log' : user_log
                  })

# @login_required(redirect_field_name='login')
def AprobarExp(request, pk):
    user_log = PerfilUser.objects.get(pk=request.user.pk)
    expediente = Expediente.objects.get(pk=pk)
    registro_log_user(user_log,"Consulta",expediente,"Expediente","Usuario")
    metadatos = Metadato.objects.filter(expediente=pk).order_by('pk')
    return render(request, 'aprobar_expediente.html', {'expediente': expediente, 'metadatos': metadatos, 'etiqueta': 'Expediente recibido','user_log':user_log})

# @login_required(redirect_field_name='login')
def ExpAprobado(request):
    user_log = PerfilUser.objects.get(pk=request.user.pk)
    estatus = Estatus()
    estatus = Estatus.objects.get(nombre="Aprobado")
    expediente = Expediente.objects.get(pk=request.POST['expediente'])
    metadatos = Metadato.objects.filter(expediente=expediente.pk).order_by('pk')
    valor = Expediente_aprobador.objects.filter(id_expediente=expediente.pk, id_usuario=user_log.pk)
    Expediente_aprobador.objects.filter(pk=valor.pk).update(id_estatus=estatus.pk)
    #Expediente.objects.filter(pk=expediente.pk).update(estatus=estatus)
    #Expediente_aprobador.objects.filter(pk=expediente.pk, id_usuario=user_log.pk).update(id_estatus=estatus)
    for metadato in metadatos:
        Metadato.objects.filter(pk=metadato.pk).update(estatus=estatus)
    metas = Metadato.objects.filter(expediente=expediente.pk)
    contador = 0
    for meta in metas:
        if meta.estatus.nombre != "Aprobado":
            break
        else:
            contador += 1
    if contador == len(metas):
        print("El archivo ya se aprobó por todos ya puede pasar al jefe de unidad")
        #Agregar aqui la funcionalidad para enviar el expediente aprobado al jefe de unidad

    registro_log_user(user_log,"Aprueba",expediente,"Expediente","Usuario")
    return render(request, 'aprobar_expediente.html', {'expediente': expediente, 'metadatos': metadatos, 'etiqueta': 'Expediente recibido','user_log':user_log})

# @login_required(redirect_field_name='login')
def RechazarExp(request):
    user_log = PerfilUser.objects.get(pk=request.user.pk)
    expediente = Expediente.objects.get(pk=request.POST['expediente'])
    metadatos = Metadato.objects.filter(expediente=expediente.pk).order_by('pk')
    estatus = Estatus()
    estatus = Estatus.objects.get(nombre="Rechazado")
    valor = Expediente_aprobador.objects.get(id_expediente=expediente.pk, id_usuario=user_log.pk)
    Expediente_aprobador.objects.filter(pk=valor.pk).update(id_estatus=estatus.pk)
    Expediente_aprobador.objects.filter(pk=valor.pk).update(motivo_rechazo=request.POST['motivo_rechazo'])
    registro_log_user(user_log,"Rechaza",expediente,"Expediente","Usuario")
    return render(request, 'aprobar_expediente.html', {'expediente': expediente, 'metadatos': metadatos, 'etiqueta': 'Expediente recibido','user_log':user_log})

# @login_required(redirect_field_name='login')
def ExpRecibidos(request):
    user_log = PerfilUser.objects.get(pk=request.user.pk)
    registro_log_user(user_log,"Consulta Recibidos",None,"Expedientes","Usuario")
    ids_users = Expediente_aprobador.objects.filter(id_usuario=user_log.pk)
    recibidos = []
    for id_usr in ids_users:
        recibidos.append(id_usr)
    return render(request, 'exp_recibidos.html', {'recibidos': recibidos, 'etiqueta': 'Expedientes recibidos','user_log':user_log})

# @login_required(redirect_field_name='login')
def AsignaExpediente(request):
    user_log = PerfilUser.objects.get(pk=request.user.pk)
    if request.method == "POST":
        usuarios = User.objects.all().order_by('pk')
        expediente = Expediente()
        expediente = Expediente.objects.get(pk=request.POST['expediente'])
        registro_log_user(user_log,"Asigna",expediente,"Expediente","Usuario")
        Expediente.objects.filter(pk=expediente.pk).update(estatus=3)
        metadatos = Metadato.objects.filter(expediente=expediente.pk).order_by('pk')
        ids_usuarios_sel = request.POST['users'].split(",")
        estatus = Estatus()
        estatus = Estatus.objects.get(pk=3)
        seleccionados = []
        for usuario in ids_usuarios_sel:
            # print(usuario)
            usr = PerfilUser()
            usr = PerfilUser.objects.get(pk=usuario)
            # seleccionados.append(usr)
            exp_aprobador = Expediente_aprobador.objects.create(
                id_expediente = expediente,
                id_usuario = usr,
                id_estatus = estatus,
            )
            exp_aprobador.save()
        va = Expediente_aprobador()
        va = Expediente_aprobador.objects.filter(id_expediente=expediente.pk)
        for v in va:
            seleccionados.append(v)
        # return HttpResponse(request.POST.items())
        return render(request, 'ver_expediente.html', {'expediente': expediente, 'metadatos': metadatos, 'usuarios': usuarios, 'etiqueta': 'Detalle expediente', 'seleccionados': seleccionados, 'user_log': user_log})

# @login_required(redirect_field_name='login')
def NuevoExpCompleto(request):
    user_log = PerfilUser.objects.get(pk=request.user.pk)
    if request.method == "POST":
        #return HttpResponse(request.POST.items())
        form = ExpedienteForm(request.POST)
        expediente = None
        # CREANDO EL EXPEDIENTE
        # Instanciando Estatus
        estatus_expediente = Estatus()
        estatus_expediente = Estatus.objects.get(nombre = 'Creado')
        #Instanciando Tipo_expediente
        tipo_expediente_exp = TipoExpediente()
        tipo_expediente_exp = TipoExpediente.objects.get(pk=request.POST['tipo'])
        #Instanciando el PerfilUser
        perfil = PerfilUser()
        perfil = PerfilUser.objects.get(pk=user_log.pk)
        # Instanciando Unidad Modificar con lo del login
        unidad_expediente = Unidad()
        unidad_expediente = Unidad.objects.get(pk=perfil.unidad_user.pk)
        # Buscando el último expediente creado en base al tipo de expediente
        try:
            exps = Expediente.objects.filter(identificador__contains=user_log.unidad_user.siglas + tipo_expediente_exp.siglas)
            mayor = 0
            for exp in exps:
                # print(int(exp.identificador[6:]))
                if mayor < int(exp.identificador[6:]):
                    mayor = int(exp.identificador[6:])
            print(mayor)
            str_ultimo = str(mayor)
            id_nuevo = mayor + 1
        except:
            str_ultimo = str(mayor)
            id_nuevo = mayor + 1
        #return HttpResponse(request.POST.items())
        # Generando el identificador
        # try:
        #     ultimo = Expediente.objects.latest('id')
        #     str_ultimo = str(ultimo.pk)
        #     id_nuevo = ultimo.pk + 1
        # except:
        #     ultimo = 0
        #     str_ultimo = str(ultimo)
        #     id_nuevo = ultimo + 1
        if len(str_ultimo) == 1:
            identif = user_log.unidad_user.siglas + tipo_expediente_exp.siglas + "000000" + str(id_nuevo)
        elif len(str_ultimo) == 2:
            identif = user_log.unidad_user.siglas + tipo_expediente_exp.siglas + "00000" + str(id_nuevo)
        elif len(str_ultimo) == 3:
            identif = user_log.unidad_user.siglas + tipo_expediente_exp.siglas + "0000" + str(id_nuevo)
        elif len(str_ultimo) == 4:
            identif = user_log.unidad_user.siglas + tipo_expediente_exp.siglas + "000" + str(id_nuevo)
        elif len(str_ultimo) == 5:
            identif = user_log.unidad_user.siglas + tipo_expediente_exp.siglas + "00" + str(id_nuevo)
        elif len(str_ultimo) == 6:
            identif = user_log.unidad_user.siglas + tipo_expediente_exp.siglas + "0" + str(id_nuevo)
        else:
            identif = user_log.unidad_user.siglas + tipo_expediente_exp.siglas + str(id_nuevo)
        print(identif)
        expediente = Expediente.objects.create(
            identificador = identif,
            nombre = request.POST.get('nombre',''),
            descripcion = request.POST.get('descripcion',''),
            asunto = request.POST.get('asunto',''),
            ubicacion = request.POST.get('ubicacion',''),
            fecha_creacion = datetime.datetime.now(),
            estatus = estatus_expediente,
            tipo_expediente = tipo_expediente_exp,
            unidad = unidad_expediente,
            activo = True,
            usuario_crea = perfil
        )
        expediente.save()
        nuevo_expediente = Expediente.objects.get(identificador=identif)
        registro_log_user(user_log,"Crea",expediente,"Expediente","Usuario")
        # CREANDO LOS METADATOS
        metadato = None
        vars = []
        tipo = 0
        metas = []
        for variable in request.POST.items():
            vars.append(variable)
        for otro in vars[8:]:
            metas.append(otro)
            tipo = otro[0]
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
        # Guardando metadatos con archivos, 
        if not request.FILES:
            pass
        else:
            for metadato_archivo in request.FILES.items():
                # crear el directorio con el id del expediente, nombre del metadato y version,
                # la version simpre sera 1 cuando se crea un metadato nuevo
                #   ejemplo : ./media/nombre_metadato/pk_expediente/v1/
                nombre_metadato = Metadato.objects.get(pk=metadato_archivo[0]).nombre    
                pk_expediente = str(nuevo_expediente.pk)
                ruta_archivo = crea_carpeta('./media/'+pk_expediente+'/'+nombre_metadato+'/v1/')
                url_archivo = guardar_archivo(ruta_archivo,metadato_archivo[1])
                # se elimina el primer caracter de lacadena '.' para poder guardar la url 
                url_archivo = url_archivo[1:]
                #crear el metadato
                metadato = Metadato()
                metadato = Metadato.objects.get(pk=metadato_archivo[0])
                nuevo_metadato = Metadato.objects.create(
                    nombre = metadato.nombre,
                    descripcion = metadato.descripcion,
                    obligatorio = metadato.obligatorio,
                    valor = url_archivo,
                    version = 1,
                    tipo_dato = metadato.tipo_dato,
                    tipo_expediente = metadato.tipo_expediente,
                    estatus = metadato.estatus,
                    expediente = nuevo_expediente,    
                )
                nuevo_metadato.save()
        return redirect('/expedientes/mis_expedientes')
    else:
        form = ExpedienteForm()
    #return render(request, 'nuevo_expediente.html', {'form': form, 'nuevo': 'Nuevo','user_log':user_log, 'ultimo':ultimo})
    return render(request, 'nuevo_expediente.html', {'form': form, 'nuevo': 'Nuevo','user_log':user_log})

# @login_required(redirect_field_name='login')
def ModificaExpCompleto(request):
    user_log = PerfilUser.objects.get(pk=request.user.pk)
    try:
        if request.method == "POST":
            expediente = Expediente.objects.get(pk=request.POST.get('expediente',''))
            exp = request.POST.get('expediente','')
            estatus_expediente = Estatus()
            estatus_expediente = Estatus.objects.get(nombre = 'Creado')
            Expediente.objects.filter(pk=exp).update(nombre=request.POST.get('nombre',''))
            Expediente.objects.filter(pk=exp).update(descripcion=request.POST.get('descripcion',''))
            Expediente.objects.filter(pk=exp).update(asunto=request.POST.get('asunto',''))
            Expediente.objects.filter(pk=exp).update(ubicacion=request.POST.get('ubicacion',''))
            Expediente.objects.filter(pk=exp).update(estatus=estatus_expediente)
            # guardando metadatos con archivo en caso de tenerlos
            if not request.FILES:
                # no se encontraron archivos en el POST
                pass
            else:
                for archivo in request.FILES.items():
                    nombre_metadato = Metadato.objects.get(pk=archivo[0]).nombre
                    pk_expediente = str(expediente.pk)
                    version = Metadato.objects.get(pk=archivo[0]).version
                    version = int(version) + 1
                    ruta_archivo = crea_carpeta('./media/'+
                                                pk_expediente+
                                                '/'+
                                                nombre_metadato+
                                                '/v'+
                                                str(version)+
                                                '/'
                                                )
                    url_archivo = guardar_archivo(ruta_archivo,archivo[1])
                    #le quitamos el "." a la ruta del archivo guardado
                    url_archivo = url_archivo[1:]
                    # actualizando cambios
                    Metadato.objects.filter(pk=archivo[0], expediente=exp).update(valor=url_archivo)
                    Metadato.objects.filter(pk=archivo[0], expediente=exp).update(version=version)
                    Metadato.objects.filter(pk=archivo[0], expediente=exp).update(estatus=estatus_expediente)
                     
            #actializando metadatos            
            vars = []
            for variable in request.POST.items():
                vars.append(variable)
            print(vars)
            for otro in vars[13:]:       
                #solo realizar actualizacion si no se trata de metadatos de tipo archivo 
                if Metadato.objects.get(pk=otro[0]).tipo_dato.tipo == "Archivo":
                    pass
                else:
                    Metadato.objects.filter(pk=otro[0], expediente=exp).update(valor=otro[1])
                    Metadato.objects.filter(pk=otro[0], expediente=exp).update(version=2)
                    Metadato.objects.filter(pk=otro[0], expediente=exp).update(estatus=estatus_expediente)

            expediente = Expediente.objects.get(pk=request.POST.get('expediente',''))
            registro_log_user(user_log,"Modifica",expediente,"Expediente","Usuario")
            metadatos  = Metadato.objects.filter(expediente=expediente.pk).order_by('pk')
            return render(request, 'detalle_expediente.html', {'expediente': expediente,'metadatos': metadatos, 'mensaje': 'Detalle expediente','user_log':user_log})
        else:
            form = ExpedienteForm(instance=expediente)
        return render(request, 'edita_expediente.html', {'form': form, 'mensaje': 'Modificar expediente','user_log':user_log})
    except ObjectDoesNotExist:
        return redirect('/expedientes/mis_expedientes')

# @login_required(redirect_field_name='login')
def DetalleExpediente(request, pk): #muestra expediente para ser modificado
    user_log = PerfilUser.objects.get(pk=request.user.pk)
    try:
        expediente = Expediente.objects.get(pk=pk)
        registro_log_user(user_log,"Consulta",expediente,"Expediente","Usuario")
        metadatos  = Metadato.objects.filter(expediente=pk).order_by('pk')
        if request.method == "POST":
            form = ExpedienteForm(request.POST, instance=expediente)
            if form.is_valid():
                expediente = form.save()
                expediente.save()
                return redirect('/expedientes/mis_expedientes')
        # else:
            # form = ExpedienteForm(instance=expediente)



    #   Valores regresados
    #   expediente : Expedinte        // Expediente seleccionado
    #   metadatos  : Metadaros[]      // Tupla con los metadatos del expediente
    #   mensaje    : String           // Mensaje a mostrar en la pagina
        return render(request, 
                      'detalle_expediente.html', 
                       {'expediente': expediente, 
                        'metadatos': metadatos, 
                        'mensaje': 'Detalle expediente',
                        'user_log': user_log,
                       }
                      )
    except ObjectDoesNotExist:
        return redirect('/expedientes/mis_expedientes')
        # Gansito marinela
        # 
        # recuerdame
        #
        #
        # hay que escribir en el log del sistema el error ocurrido
        #

# @login_required(redirect_field_name='login')
def GuardaMetadatosExp(request):
    
    vars = []
    for variable in request.POST.items():
        vars.append(variable)
    for otro in vars[3:]:
        Metadato.objects.filter(pk=otro[0]).update(valor=otro[1])
        Metadato.objects.filter(pk=otro[0]).update(version=1)
        Metadato.objects.filter(pk=otro[0]).update(expediente=request.POST['id_exp'])
    return redirect('/expedientes/mis_expedientes')

# @login_required(redirect_field_name='login')
def ListarMisExpedientes(request):
    user_log = PerfilUser.objects.get(pk=request.user.pk)
    registro_log_user(user_log,"Consulta",None,"Expedientes","Usuario")
    user = get_user(request)
    user = request.user
    usuarios = PerfilUser.objects.all().exclude(pk=user_log.pk)
    expedientes = Expediente.objects.filter(usuario_crea=user).exclude(activo=False).order_by('-fecha_creacion')
    return render(request, 'mis_expedientes.html', {'expedientes': expedientes, 'usuarios': usuarios ,'mensaje': 'Mis expedientes','user_log':user_log})

# @login_required(redirect_field_name='login')
def ListaMetadatosExp(request):
    user_log = PerfilUser.objects.get(pk=request.user.pk)
    if request.method == "GET":
        tipo = TipoExpediente()
        tipo = TipoExpediente.objects.get(pk=request.GET['pk'])

        id = Expediente()
        id = Expediente.objects.get(pk=request.GET['id'])

        metadatos = Metadato.objects.filter(tipo_expediente=tipo.pk).order_by('pk')
        bandera = expediente_tine_archivos(metadatos)

        #   Valores regresados 
        #   metadatos : metadatos // Los metadatos que componen el expediente
        #   tipo : tipo           // El tipo de expediente
        #   id : id               // El id del expediente que se esta trabajando
        #   mensaje : 'metadatos' // Mensaje a mostrar en la pagina
        #   bandera : bandera     // variable auxiliar que representa si el expediente
        #                            tiene un metadato del tipo Archivo.
        return render(request,
                     'lista_metadatos_exp.html',
                     {'metadatos': metadatos, 
                      'tipo': tipo, 
                      'id': id,
                      'mensaje': 'Metadatos',
                      'bandera': bandera,
                      'user_log': user_log,
                     })

# @login_required(redirect_field_name='login')
def MuestraCamposExp(request):
    user_log = PerfilUser.objects.get(pk=request.user.pk)
    tipo = TipoExpediente()
    tipo = TipoExpediente.objects.get(pk=request.POST['tipo'])
    form = ExpedienteForm()
    return render(request, 'nuevo_expediente.html', {'form': form,'tipo': tipo, 'nuevo': 'Nuevo', 'user_log':user_log})


# @login_required(redirect_field_name='login')
def SeleccionaTipoExp(request):
    user_log = PerfilUser.objects.get(pk=request.user.pk)
    # tipos_expedientes = TipoExpediente.objects.all()
    tipos_expedientes = TipoExpediente.objects.filter(activo=True, unidad=user_log.unidad_user)
    # return redirect('/expedientes/')
    registro_log_user(user_log,"Lista",None,"Tipos de Expedientes","Usuario")
    return render(request, 'selecciona_tipo_exp.html', {'tipos_expedientes': tipos_expedientes, 'mensaje': 'Expedientes','user_log':user_log})
    

# @login_required(redirect_field_name='login')
def EditarExpediente(request, pk):
    user_log = PerfilUser.objects.get(pk=request.user.pk)
    try:
        expediente = Expediente.objects.get(pk=pk)
        if request.method == "POST":
            form = ExpedienteForm(request.POST, instance=expediente)
            if form.is_valid():
                expediente = form.save()
                expediente.save()
                registro_log_user(user_log,"Elimina",expediente,"Estatus","Usuario")
                return redirect('/expedientes/mis_expedientes')
        else:
            form = ExpedienteForm(instance=expediente)
        return render(request, 'edita_expediente.html', {'form': form, 'mensaje': 'Modificar expediente','user_log':user_log})
    except ObjectDoesNotExist:
        return redirect('/expedientes/mis_expedientes')


# @login_required(redirect_field_name='login')
def EliminarExpediente(request, pk):
    #return redirect(borrar_expediente(request, pk))
    return redirect(marcar_expediente_como_inactivo(request, pk))
    

# @creacióm de función
# fecha : 08/04/2020
# autor: Rada
# explicacion : borra expediente de la base de datos, el borrado se realiza en cascada
def borrar_expediente(request, pk):
     try:
         user_log = PerfilUser.objects.get(pk=request.user.pk)
         expediente = Expediente.objects.get(pk=pk)
         expediente.delete()
         registro_log_user(user_log,"Elimina",expediente,"Expediente","Usuario")
         return '/expedientes/mis_expedientes'
     except ObjectDoesNotExist:
         return '/expedientes/mis_expedientes'


# @creacióm de función
# fecha : 08/04/2020
# autor: Rada
def marcar_expediente_como_inactivo(request, pk):
    user_log = PerfilUser.objects.get(pk=request.user.pk)
    try:
        expediente = Expediente.objects.get(pk=pk)
        registro_log_user(user_log,"Elimina",expediente,"Expediente","Usuario")
        Expediente.objects.filter(pk=pk).update(activo=False)
        return '/expedientes/mis_expedientes'
    except ObjectDoesNotExist:
        return '/expedientes/mis_expedientes'

     
def crea_carpeta(ruta ): # parametros 
                         #    ruta : string. Cadena que contenga la ruta
                         # retorno
                         #    string : ruta de la carpeta creada
    if not exists(ruta):
        makedirs(ruta)
    print(ruta)
    return ruta          # rwtorno : string. Cadena con la ruta creada
    

def guardar_archivo(ruta,archivo): # parametros 
                                   #    ruta : string. Cadena que contenga la ruta
                                   #    archivo : File. Archivo que sera guardado
                                   # retorno
                                   #    string : Cadena con la url del archivo guardado
    url = ruta+archivo.name
    with open(url, 'wb+') as destination:
        for chunk in archivo.chunks():
                        destination.write(chunk)
    return url                     


def expediente_tine_archivos(metadatos): # parametros 
                                         #    metadatos : Metadato. Tupla con los metadatos
                                         #    del expediente                              
                                         # retorno
                                         #    boolean : True si el expediente tine archivvos, 
                                         #              False en caso contrario
    for metadato in metadatos:
        if metadato.tipo_dato.tipo == "Archivo":
            bandera = True
            return True
        return False

# @Funciones decrepitas
# poner acontinuación las funciones que ya no tienen utilidad y especificar porque es decrepita 
#
#
#
#

# @ Decrepita ya no se utiliza dado que solo crea los datos principales 
#   del expediente y no crea las demas relaciones que conforman el expediente,
#   en sulugar se usa la funcion NuevoExpCompleto 
#    
# @login_required(redirect_field_name='login')
def NuevoExpediente(request): 
    user_log = PerfilUser.objects.get(pk=request.user.pk)
    if request.method == "POST":
        form = ExpedienteForm(request.POST)
        expediente = None
        if form.is_valid():
            # Instanciando Estatus
            estatus_dos = Estatus.objects.get(nombre = 'Creado') 
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
            # Obteniendo usuario
            user = get_user(request)
            user = request.user
            # Creando expediente
            expediente = Expediente.objects.create(
                identificador   = request.POST.get('identificador',''),
                nombre          = request.POST.get('nombre',''),
                descripcion     = request.POST.get('descripcion',''),
                asunto          = request.POST.get('asunto',''),
                ubicacion       = request.POST.get('ubicacion',''),
                fecha_creacion  = datetime.datetime.now(),
                estatus         = estatus_dos,
                tipo_expediente = tipo_expediente_dos,
                unidad          = unidad_dos,
                activo          = activo_dos,
                usuario_crea    = user
            )
            # Guardando expediente en la base
            expediente.save()
            # Regresando expediente completo
            nuevo_expediente = Expediente.objects.filter(identificador=request.POST.get('identificador',''))
            registro_log_user(user_log,"Crea",nuevo_expediente,"Expediente","Usuario")
            id = 0
            for exp in nuevo_expediente:
                id = exp.pk
            print(id)
            return redirect('/expedientes/lista_metadatos_exp?pk=%s&id=%s' % (expediente.tipo_expediente.pk, id))            
    else:
        form = ExpedienteForm()
    return render(request, 'nuevo_expediente.html', {'form': form, 'nuevo': 'Nuevo','user_log':user_log})

# @login_required(redirect_field_name='login')
def BuscaExpedientes(request):
    user_log = PerfilUser.objects.get(pk=request.user.pk)
    registro_log_user(user_log,"Buscador",None,"Expedientes","Usuario")
    expedientes = Expediente.objects.all().order_by("-fecha_creacion")
    #expedientes = Expediente.objects.all().exclude(estatus = 1)
    return render(request, 'busca_expedientes.html', {'expedientes': expedientes, 'mensaje': 'Búsqueda de expedientes','user_log':user_log})

# @login_required(redirect_field_name='login')
def RecibidosDeputy(request):
    user_log = PerfilUser.objects.get(pk=request.user.pk)
    # recibidos = Expediente_deputy.objects.all()
    recibidos = Expediente_deputy.objects.filter(deputy=user_log)
    registro_log_user(user_log,"Consulta",None,"Expedientes deputy","Usuario")
    # registros = Registra_actividad.objects.all().exclude(rol="Usuario").order_by("-pk")
    return render(request, 'exp_deputy.html', {'recibidos': recibidos, 'mensaje': 'Expedientes deputy','user_log':user_log, 'bandera' : True})

# @login_required(redirect_field_name='login')
def LogUsuario(request):
    user_log = PerfilUser.objects.get(pk=request.user.pk)
    registro_log_user(user_log,"Consulta",None,"Log usuarios","Administrador")
    registros = Registra_actividad.objects.all().exclude(rol="Administrador").order_by("-pk")
    return render(request, 'logs.html', {'registros': registros, 'mensaje': 'Log usuarios','user_log':user_log})

# @login_required(redirect_field_name='login')
def LogAdministrador(request):
    user_log = PerfilUser.objects.get(pk=request.user.pk)
    registro_log_user(user_log,"Consulta",None,"Log administrador","Administrador")
    registros = Registra_actividad.objects.all().exclude(rol="Usuario").order_by("-pk")
    return render(request, 'logs.html', {'registros': registros, 'mensaje': 'Log usuarios','user_log':user_log})

def registro_log_user(usuario,actividad,objeto,detalle_objeto,rol):
    
    now = datetime.datetime.now()
    nom_arch = "Logs/" + now.strftime("%Y-%m-%d") + "log_user.txt"
    with open(nom_arch,'a') as archivo:
        if objeto != None:
            if hasattr(objeto,"identificador"):
                archivo.write(now.strftime("%Y-%m-%d %H:%M:%S") + " " + rol + " " + usuario.first_name + " " + usuario.last_name + " " + usuario.amaterno + " " + actividad + " " + detalle_objeto+": " + objeto.identificador + "\n")
                objeto_utilizado = objeto.identificador
            elif hasattr(objeto,"tipo"):
                archivo.write(now.strftime("%Y-%m-%d %H:%M:%S") + " " + rol + " " + usuario.first_name + " " + usuario.last_name + " " + usuario.amaterno + " " + actividad + " " + detalle_objeto+": " + objeto.tipo + " " + "\n")
                objeto_utilizado = objeto.tipo
            else:  
                archivo.write(now.strftime("%Y-%m-%d %H:%M:%S") + " " + rol + " "+ usuario.first_name + " " + usuario.last_name + " " + usuario.amaterno + " " + actividad + " " + detalle_objeto+": " + objeto.nombre + " " "\n")     
                objeto_utilizado = objeto.nombre
        else:
            archivo.write(now.strftime("%Y-%m-%d %H:%M:%S") + " " + rol + " "+ usuario.first_name + " " + usuario.last_name + " " + usuario.amaterno + " " + actividad + " " + detalle_objeto + "\n")
            objeto_utilizado = ""
        archivo.close()
    fecha = now.strftime("%Y-%m-%d")
    hora = now.strftime("%H:%M:%S")
    registro_actividad = Registra_actividad.objects.create(
        fecha = fecha,
        hora = hora,
        rol = rol,
        usuario = usuario,
        actividad = actividad,
        detalle_objeto = detalle_objeto,
        objeto = objeto_utilizado,
    )
    registro_actividad.save()

def registro_log_admin(usuario,actividad,objeto,detalle_objeto,rol):
    now = datetime.datetime.now()
    nom_arch = "Logs/" + now.strftime("%Y-%m-%d") + "log_admin.txt"
    with open(nom_arch,'a') as archivo:
        if objeto != None:
            if hasattr(objeto,"username"):
                archivo.write(now.strftime("%Y-%m-%d %H:%M:%S") + " " + rol + " "+ usuario.first_name + " " + usuario.last_name + " " + usuario.amaterno + " " + actividad + " " + detalle_objeto +": " + objeto.username + "\n")
                objeto_utilizado = objeto.username
            elif hasattr(objeto,"tipo"):
                archivo.write(now.strftime("%Y-%m-%d %H:%M:%S") + " " + rol + " "+ usuario.first_name + " " + usuario.last_name + " " + usuario.amaterno + " " + actividad + " " + detalle_objeto +": " + objeto.tipo + "\n")
                objeto_utilizado = objeto.tipo
            else:  
                archivo.write(now.strftime("%Y-%m-%d %H:%M:%S") + " " + rol + " "+ usuario.first_name + " " + usuario.last_name + " " + usuario.amaterno + " " + actividad + ": " + detalle_objeto +": " + objeto.nombre + "\n")
                objeto_utilizado = objeto.nombre    
        else:
            archivo.write(now.strftime("%Y-%m-%d %H:%M:%S") + " " + rol + " "+ usuario.first_name + " " + usuario.last_name + " " + usuario.amaterno + " " + actividad + " " + detalle_objeto + "\n")
            objeto_utilizado = ""
        archivo.close()
    fecha = now.strftime("%Y-%m-%d")
    hora = now.strftime("%H:%M:%S")
    registro_actividad = Registra_actividad.objects.create(
        fecha = fecha,
        hora = hora,
        rol = rol,
        usuario = usuario,
        actividad = actividad,
        detalle_objeto = detalle_objeto,
        objeto = objeto_utilizado
    )
    registro_actividad.save()

# @login_required(redirect_field_name='login')
def Deputy(request):
    user_log = PerfilUser.objects.get(pk=request.user.pk)
    try:
        usuarios = PerfilUser.objects.all().exclude(pk=request.POST['usuario_origen'])
        usuario = PerfilUser.objects.get(pk=request.POST['usuario_origen'])
        usuario_origen = PerfilUser.objects.get(pk=request.POST['usuario_origen'])
        usuario_destino = PerfilUser.objects.get(pk=request.POST['usuario_destino'])
        expedientes_origen = Expediente.objects.filter(usuario_crea=usuario_origen)
        expedientes_asignados = Expediente_aprobador.objects.all()
        #expedientes_asignados = Expediente_aprobador.objects.filter(id_usuario=usuario_origen)
        expedientes = Expediente.objects.filter(usuario_crea=usuario.pk)
        #return HttpResponse(request.POST.items())
        for expediente in expedientes_origen:
            print(expediente)
            deputy = Expediente_deputy.objects.create(
                expediente = expediente,
                usuario_crea = usuario_origen,
                deputy = usuario_destino,
            )
            deputy.save()
        
        # for expediente in expedientes_asignados:
        #     print(expediente)
        #     if expediente.id_expediente.usuario_crea == usuario_origen:
        #         deputy = Expediente_deputy.objects.create(
        #             expediente = expediente,
        #             usuario_crea = usuario_origen,
        #             deputy = usuario_destino,
        #         )
        #         deputy.save()

        PerfilUser.objects.filter(pk=usuario_origen.pk).update(transferido=True)
        PerfilUser.objects.filter(pk=usuario_destino.pk).update(deputy=True)
        registro_log_admin(user_log,"Transfiere expedientes",usuario," Al usuario",usuario_destino.first_name + " " + usuario_destino.last_name + " " + usuario_destino.amaterno)
        # return HttpResponse(request.POST.items())
        return render(request, 'mis_expedientes.html', {'expedientes': expedientes, 'usuarios': usuarios ,'mensaje': 'Mis expedientes','user_log':user_log})
    except ObjectDoesNotExist:
        return redirect('principal')

from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4, inch
from reportlab.lib.enums import TA_CENTER
from reportlab.lib import colors
from reportlab.platypus import Paragraph, Table, TableStyle, Image
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.utils import ImageReader

# @login_required(redirect_field_name='login')
def ReporteUsuario(request,pk):

    user_log = PerfilUser.objects.get(pk=request.user.pk)
    # registro_log_user(user_log,"Genera",expediente,"Reporte","Usuario")

    # Instanciando caja
    usuario = PerfilUser()
    usuario = PerfilUser.objects.get(pk=pk)

    registro_log_admin(user_log,"Genera",usuario,"Reporte usuario","Administrador")

    myDate = datetime.datetime.now()
    fecha_formateada = myDate.strftime("%d-%m-%Y")
    
    # Create the HttpResponse headers with PDF
    response = HttpResponse(content_type='applicacion/pdf')
    response['Content-Disposition'] = 'attachment; filename=REPORTE-' + usuario.first_name + '-' + usuario.last_name + '-' + usuario.amaterno + '-' + fecha_formateada + '.pdf'
    
    # Create the PDF object. using the BytesIO object as its "file"
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)
    
    # Header
    logo = ImageReader('static\imagenes\solusoft.png')
    c.drawImage(logo,200,750,width=200,height=66.62,mask='auto')

    c.setLineWidth(.3)
    c.setFont('Helvetica', 16)
    c.drawString(150,725,'REPORTE DE ACTIVIDAD DEL USUARIO:')

    c.setFont('Helvetica-Bold', 12)
    c.drawString(30,700,usuario.first_name + " " + usuario.last_name + " " + usuario.amaterno)

    c.setFont('Helvetica', 9)
    c.drawString(470,800,'Fecha: ' + fecha_formateada)
    #c.line(460,725,560,725)

    # Table header
    styles = getSampleStyleSheet()
    styleBH = styles["Normal"]
    styleBH.alignment = TA_CENTER
    styleBH.fontSize = 10

    id = Paragraph('''#''', styleBH)
    fecha_creacion = Paragraph('''FECHA CREACIÓN''', styleBH)
    identificador = Paragraph('''IDENTIFICADOR''', styleBH)
    nombre = Paragraph('''NOMBRE''', styleBH)
    estatus = Paragraph('''ESTATUS''', styleBH)
    

    styles = getSampleStyleSheet()
    styleN = styles["BodyText"]
    styleN.alignment = TA_CENTER
    styleN.fontSize = 7

    width, height = A4
    high = 675


    expedientes = Expediente()
    expedientes = Expediente.objects.filter(usuario_crea=usuario.pk)
    total_expedientes = len(expedientes)

    index = 0
    otro = []
    otro.append([id, fecha_creacion, identificador, estatus, nombre])
    for expediente in expedientes:
        index += 1
        fecha = expediente.fecha_creacion
        fecha_crea = fecha.strftime("%d-%m-%Y a %H:%m hrs.")
        otro.append([index, fecha_crea, expediente.identificador, expediente.estatus.nombre, expediente.nombre])
        high = high - 18

    c.setFont('Helvetica-Bold', 12)
    c.drawString(400,700,"Total de expedientes: " + str(total_expedientes))

    # Table size
    table = Table(otro, colWidths=[0.9 * inch, 1.6 * inch, 1.5 * inch, 0.9 * inch, 2.5 * inch])
    table.setStyle(TableStyle([ # Estilos de la tabla
        ('INNERGRID', (0,0), (-1,-1), 0.25, colors.black),
        ('BOX', (0,0), (-1,-1), 0.25, colors.black),
    ]))
    
    # PDF size
    table.wrapOn(c, width, height)
    table.drawOn(c, 30, high)
    #c.showPage()
    # c.showPage() # save page

    # save PDF
    c.save()
    
    # get the value of BytesIO buffer and write response
    pdf = buffer.getvalue()
    buffer.close()
    response.write(pdf)
    return response


# @login_required(redirect_field_name='login')
def ReporteUnidad(request,pk):

    user_log = PerfilUser.objects.get(pk=request.user.pk)
    # registro_log_user(user_log,"Genera",expediente,"Reporte","Usuario")

    unidad = Unidad()
    unidad = Unidad.objects.get(pk=pk)

    registro_log_admin(user_log,"Genera",unidad,"Reporte unidad","Administrador")

    myDate = datetime.datetime.now()
    fecha_formateada = myDate.strftime("%d-%m-%Y")
    
    # Create the HttpResponse headers with PDF
    response = HttpResponse(content_type='applicacion/pdf')
    response['Content-Disposition'] = 'attachment; filename=REPORTE-' + unidad.nombre + "-" + fecha_formateada + '.pdf'
    
    # Create the PDF object. using the BytesIO object as its "file"
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)
    
    # Header
    logo = ImageReader('static\imagenes\solusoft.png')
    c.drawImage(logo,200,750,width=200,height=66.62,mask='auto')

    c.setLineWidth(.3)
    c.setFont('Helvetica', 16)
    c.drawString(200,725,'REPORTE DE UNIDAD: ' + unidad.siglas)

    c.setFont('Helvetica-Bold', 12)
    c.drawString(30,700,unidad.nombre)

    c.setFont('Helvetica', 9)
    c.drawString(470,800,'Fecha: ' + fecha_formateada)
    #c.line(460,725,560,725)

    # Table header
    styles = getSampleStyleSheet()
    styleBH = styles["Normal"]
    styleBH.alignment = TA_CENTER
    styleBH.fontSize = 10

    id = Paragraph('''#''', styleBH)
    fecha_creacion = Paragraph('''FECHA CREACIÓN''', styleBH)
    identificador = Paragraph('''IDENTIFICADOR''', styleBH)
    nombre = Paragraph('''CREADO''', styleBH)
    estatus = Paragraph('''ESTATUS''', styleBH)
    

    styles = getSampleStyleSheet()
    styleN = styles["BodyText"]
    styleN.alignment = TA_CENTER
    styleN.fontSize = 7

    width, height = A4
    high = 675


    expedientes = Expediente()
    expedientes = Expediente.objects.filter(unidad=unidad.pk)
    total_expedientes = len(expedientes)

    index = 0
    otro = []
    otro.append([id, fecha_creacion, identificador, estatus, nombre])
    for expediente in expedientes:
        index += 1
        fecha = expediente.fecha_creacion
        fecha_crea = fecha.strftime("%d-%m-%Y a %H:%m hrs.")
        nombre_crea = expediente.usuario_crea.first_name + " " + expediente.usuario_crea.last_name + " " + expediente.usuario_crea.amaterno 
        otro.append([index, fecha_crea, expediente.identificador, expediente.estatus.nombre, nombre_crea])
        high = high - 18

    c.setFont('Helvetica-Bold', 12)
    c.drawString(400,700,"Total de expedientes: " + str(total_expedientes))

    # Table size
    table = Table(otro, colWidths=[0.9 * inch, 1.6 * inch, 1.5 * inch, 0.9 * inch, 2.5 * inch])
    table.setStyle(TableStyle([ # Estilos de la tabla
        ('INNERGRID', (0,0), (-1,-1), 0.25, colors.black),
        ('BOX', (0,0), (-1,-1), 0.25, colors.black),
    ]))
    
    # PDF size
    table.wrapOn(c, width, height)
    table.drawOn(c, 30, high)
    #c.showPage()
    # c.showPage() # save page

    # save PDF
    c.save()
    
    # get the value of BytesIO buffer and write response
    pdf = buffer.getvalue()
    buffer.close()
    response.write(pdf)
    return response

# @login_required(redirect_field_name='login')
def ReporteGeneral(request):

    user_log = PerfilUser.objects.get(pk=request.user.pk)
    # registro_log_user(user_log,"Genera",expediente,"Reporte","Usuario")

    registro_log_admin(user_log,"Genera",None,"Reporte general","Administrador")

    myDate = datetime.datetime.now()
    fecha_formateada = myDate.strftime("%d-%m-%Y")
    
    # Create the HttpResponse headers with PDF
    response = HttpResponse(content_type='applicacion/pdf')
    response['Content-Disposition'] = 'attachment; filename=REPORTE-GENERAL' + fecha_formateada + '.pdf'
    
    # Create the PDF object. using the BytesIO object as its "file"
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)
    
    # Header
    logo = ImageReader('static\imagenes\solusoft.png')
    c.drawImage(logo,200,750,width=200,height=66.62,mask='auto')

    c.setLineWidth(.3)
    c.setFont('Helvetica', 16)
    c.drawString(150,725,'REPORTE GENERAL DE EXPEDIENTES:')

    c.setFont('Helvetica-Bold', 12)
    c.drawString(30,700,'Reporte general')

    c.setFont('Helvetica', 9)
    c.drawString(470,800,'Fecha: ' + fecha_formateada)
    #c.line(460,725,560,725)

    # Table header
    styles = getSampleStyleSheet()
    styleBH = styles["Normal"]
    styleBH.alignment = TA_CENTER
    styleBH.fontSize = 10

    id = Paragraph('''#''', styleBH)
    fecha_creacion = Paragraph('''FECHA CREACIÓN''', styleBH)
    identificador = Paragraph('''IDENTIFICADOR''', styleBH)
    nombre = Paragraph('''CREADO''', styleBH)
    estatus = Paragraph('''ESTATUS''', styleBH)
    unidad = Paragraph('''UNIDAD''', styleBH)
    

    styles = getSampleStyleSheet()
    styleN = styles["BodyText"]
    styleN.alignment = TA_CENTER
    styleN.fontSize = 7

    width, height = A4
    high = 675


    expedientes = Expediente()
    expedientes = Expediente.objects.all()
    total_expedientes = len(expedientes)

    index = 0
    otro = []
    otro.append([id, fecha_creacion, identificador, estatus, unidad, nombre])
    for expediente in expedientes:
        index += 1
        fecha = expediente.fecha_creacion
        fecha_crea = fecha.strftime("%d-%m-%Y a %H:%m hrs.")
        nombre_crea = expediente.usuario_crea.first_name + " " + expediente.usuario_crea.last_name + " " + expediente.usuario_crea.amaterno 
        otro.append([index, fecha_crea, expediente.identificador, expediente.estatus.nombre, expediente.unidad.siglas , nombre_crea])
        high = high - 18

    c.setFont('Helvetica-Bold', 12)
    c.drawString(400,700,"Total de expedientes: " + str(total_expedientes))

    # Table size
    table = Table(otro, colWidths=[0.9 * inch, 1.6 * inch, 1.5 * inch, 0.9 * inch, 0.7 * inch, 1.7 * inch])
    table.setStyle(TableStyle([ # Estilos de la tabla
        ('INNERGRID', (0,0), (-1,-1), 0.25, colors.black),
        ('BOX', (0,0), (-1,-1), 0.25, colors.black),
    ]))
    
    # PDF size
    table.wrapOn(c, width, height)
    table.drawOn(c, 30, high)
    #c.showPage()
    # c.showPage() # save page

    # save PDF
    c.save()
    
    # get the value of BytesIO buffer and write response
    pdf = buffer.getvalue()
    buffer.close()
    response.write(pdf)
    return response

# @login_required(redirect_field_name='login')
def ReporteUsuarios(request):

    user_log = PerfilUser.objects.get(pk=request.user.pk)
    # registro_log_user(user_log,"Genera",expediente,"Reporte","Usuario")

    registro_log_admin(user_log,"Genera",None,"Reporte usuarios","Administrador")

    myDate = datetime.datetime.now()
    fecha_formateada = myDate.strftime("%d-%m-%Y")
    
    # Create the HttpResponse headers with PDF
    response = HttpResponse(content_type='applicacion/pdf')
    response['Content-Disposition'] = 'attachment; filename=REPORTE-USUARIOS' + fecha_formateada + '.pdf'
    
    # Create the PDF object. using the BytesIO object as its "file"
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)
    
    # Header
    logo = ImageReader('static\imagenes\solusoft.png')
    c.drawImage(logo,200,750,width=200,height=66.62,mask='auto')

    c.setLineWidth(.3)
    c.setFont('Helvetica', 16)
    c.drawString(150,725,'REPORTE DE USUARIOS:')

    c.setFont('Helvetica-Bold', 12)
    c.drawString(30,700,'Reporte de usuarios')

    c.setFont('Helvetica', 9)
    c.drawString(470,800,'Fecha: ' + fecha_formateada)
    #c.line(460,725,560,725)

    # Table header
    styles = getSampleStyleSheet()
    styleBH = styles["Normal"]
    styleBH.alignment = TA_CENTER
    styleBH.fontSize = 10

    id = Paragraph('''#''', styleBH)
    nombre = Paragraph('''NOMBRE''', styleBH)
    correo = Paragraph('''CORREO''', styleBH)
    creado = Paragraph('''CREADO''', styleBH)
    estatus = Paragraph('''STS''', styleBH)
    ultimo_log = Paragraph('''ÚLTIMO LOGIN''', styleBH)
    

    styles = getSampleStyleSheet()
    styleN = styles["BodyText"]
    styleN.alignment = TA_CENTER
    styleN.fontSize = 7

    width, height = A4
    high = 675

    usuarios = PerfilUser()
    usuarios = PerfilUser.objects.all()
    total_usuarios = len(usuarios)

    index = 0
    otro = []
    otro.append([id, nombre, correo, estatus, creado, ultimo_log])
    for usuario in usuarios:
        index += 1
        fecha = usuario.date_joined
        fecha_crea = fecha.strftime("%d-%m-%Y")
        fecha_log = usuario.last_login
        #print(fecha_log)
        if fecha_log == None:
            fecha_last_log = "--"
        else:
            fecha_last_log = fecha_log.strftime("%d-%m-%Y %H:%m")
        # fecha_last_log = datetime.datetime.strptime(fecha_log, '%Y-%m-%d %H:%m:%S.%f')

        if usuario.is_active:
            activo = "Activo"
        else:
            activo = "Inactivo"

        nombre_crea = usuario.first_name + " " + usuario.last_name + " " + usuario.amaterno 
        otro.append([index, nombre_crea, usuario.email, activo, fecha_crea, fecha_last_log])
        high = high - 18

    c.setFont('Helvetica-Bold', 12)
    c.drawString(400,700,"Total de usuarios: " + str(total_usuarios))

    # Table size
    table = Table(otro, colWidths=[0.5 * inch, 2.5 * inch, 1.8 * inch, 0.6 * inch, 0.9 * inch, 1.25 * inch])
    table.setStyle(TableStyle([ # Estilos de la tabla
        ('INNERGRID', (0,0), (-1,-1), 0.25, colors.black),
        ('BOX', (0,0), (-1,-1), 0.25, colors.black),
    ]))
    
    # PDF size
    table.wrapOn(c, width, height)
    table.drawOn(c, 30, high)
    #c.showPage()
    # c.showPage() # save page

    # save PDF
    c.save()
    
    # get the value of BytesIO buffer and write response
    pdf = buffer.getvalue()
    buffer.close()
    response.write(pdf)
    return response

# @login_required(redirect_field_name='login')
def ReporteUnidades(request):

    user_log = PerfilUser.objects.get(pk=request.user.pk)
    # registro_log_user(user_log,"Genera",expediente,"Reporte","Usuario")

    registro_log_admin(user_log,"Genera",None,"Reporte unidades","Administrador")

    myDate = datetime.datetime.now()
    fecha_formateada = myDate.strftime("%d-%m-%Y")
    
    # Create the HttpResponse headers with PDF
    response = HttpResponse(content_type='applicacion/pdf')
    response['Content-Disposition'] = 'attachment; filename=REPORTE-UNIDADES' + fecha_formateada + '.pdf'
    
    # Create the PDF object. using the BytesIO object as its "file"
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)
    
    # Header
    logo = ImageReader('static\imagenes\solusoft.png')
    c.drawImage(logo,200,750,width=200,height=66.62,mask='auto')

    c.setLineWidth(.3)
    c.setFont('Helvetica', 16)
    c.drawString(200,725,'REPORTE DE UNIDADES:')

    c.setFont('Helvetica-Bold', 12)
    c.drawString(30,700,'Reporte de unidades')

    c.setFont('Helvetica', 9)
    c.drawString(470,800,'Fecha: ' + fecha_formateada)
    #c.line(460,725,560,725)

    # Table header
    styles = getSampleStyleSheet()
    styleBH = styles["Normal"]
    styleBH.alignment = TA_CENTER
    styleBH.fontSize = 10

    id = Paragraph('''#''', styleBH)
    unidad = Paragraph('''UNIDAD''', styleBH)
    siglas = Paragraph('''SIGLAS''', styleBH)
    estatus = Paragraph('''ESTATUS''', styleBH)
    

    styles = getSampleStyleSheet()
    styleN = styles["BodyText"]
    styleN.alignment = TA_CENTER
    styleN.fontSize = 7

    width, height = A4
    high = 675

    unidades = Unidad()
    unidades = Unidad.objects.all()
    total_unidades = len(unidades)

    index = 0
    otro = []
    otro.append([id, unidad, siglas, estatus])
    for unidad in unidades:
        index += 1
        if unidad.activo:
            activo = "Activo"
        else:
            activo = "Inactivo"
        otro.append([index, unidad.nombre, unidad.siglas, activo])
        high = high - 18

    c.setFont('Helvetica-Bold', 12)
    c.drawString(430,700,"Total de unidades: " + str(total_unidades))

    # Table size
    table = Table(otro, colWidths=[0.5 * inch, 5 * inch, 0.9 * inch, 1 * inch])
    table.setStyle(TableStyle([ # Estilos de la tabla
        ('INNERGRID', (0,0), (-1,-1), 0.25, colors.black),
        ('BOX', (0,0), (-1,-1), 0.25, colors.black),
    ]))
    
    # PDF size
    table.wrapOn(c, width, height)
    table.drawOn(c, 30, high)
    #c.showPage()
    # c.showPage() # save page

    # save PDF
    c.save()
    
    # get the value of BytesIO buffer and write response
    pdf = buffer.getvalue()
    buffer.close()
    response.write(pdf)
    return response

# @login_required(redirect_field_name='login')
def ReporteTiposExpedientes(request):

    user_log = PerfilUser.objects.get(pk=request.user.pk)
    # registro_log_user(user_log,"Genera",expediente,"Reporte","Usuario")

    registro_log_admin(user_log,"Genera",None,"Reporte tipos expedientes","Administrador")

    myDate = datetime.datetime.now()
    fecha_formateada = myDate.strftime("%d-%m-%Y")
    
    # Create the HttpResponse headers with PDF
    response = HttpResponse(content_type='applicacion/pdf')
    response['Content-Disposition'] = 'attachment; filename=REPORTE-TIPOS-EXPEDIENTES' + fecha_formateada + '.pdf'
    
    # Create the PDF object. using the BytesIO object as its "file"
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)
    
    # Header
    logo = ImageReader('static\imagenes\solusoft.png')
    c.drawImage(logo,200,750,width=200,height=66.62,mask='auto')

    c.setLineWidth(.3)
    c.setFont('Helvetica', 16)
    c.drawString(170,725,'REPORTE TIPOS DE EXPEDIENTES:')

    c.setFont('Helvetica-Bold', 12)
    c.drawString(30,700,'Reporte tipos de expedientes')

    c.setFont('Helvetica', 9)
    c.drawString(470,800,'Fecha: ' + fecha_formateada)
    #c.line(460,725,560,725)

    # Table header
    styles = getSampleStyleSheet()
    styleBH = styles["Normal"]
    styleBH.alignment = TA_CENTER
    styleBH.fontSize = 10

    id = Paragraph('''#''', styleBH)
    tipo_e = Paragraph('''TIPO DE EXPEDIENTE''', styleBH)
    siglas = Paragraph('''SIGLAS''', styleBH)
    estatus = Paragraph('''ESTATUS''', styleBH)
    

    styles = getSampleStyleSheet()
    styleN = styles["BodyText"]
    styleN.alignment = TA_CENTER
    styleN.fontSize = 7

    width, height = A4
    high = 675

    tipos_exp = TipoExpediente()
    tipos_exp = TipoExpediente.objects.all()
    total_tipos = len(tipos_exp)

    index = 0
    otro = []
    otro.append([id, tipo_e, siglas, estatus])
    for tipo in tipos_exp:
        index += 1
        if tipo.activo:
            activo = "Activo"
        else:
            activo = "Inactivo"
        otro.append([index, tipo.nombre, tipo.siglas, activo])
        high = high - 18

    c.setFont('Helvetica-Bold', 12)
    c.drawString(380,700,"Total tipos de expedientes: " + str(total_tipos))

    # Table size
    table = Table(otro, colWidths=[0.5 * inch, 5 * inch, 0.9 * inch, 1 * inch])
    table.setStyle(TableStyle([ # Estilos de la tabla
        ('INNERGRID', (0,0), (-1,-1), 0.25, colors.black),
        ('BOX', (0,0), (-1,-1), 0.25, colors.black),
    ]))
    
    # PDF size
    table.wrapOn(c, width, height)
    table.drawOn(c, 30, high)
    #c.showPage()
    # c.showPage() # save page

    # save PDF
    c.save()
    
    # get the value of BytesIO buffer and write response
    pdf = buffer.getvalue()
    buffer.close()
    response.write(pdf)
    return response