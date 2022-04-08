# -*- coding: utf-8 -*-
from ensurepip import version
from django.shortcuts import render
from estatus.models import Estatus
import expediente
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

from expediente.models import Expediente, Expediente_aprobador
from metadato.forms import MetadatoForm
from metadato.models import Metadato
from tipo_dato.models import TipoDato
import tipo_expediente
from tipo_expediente.models import TipoExpediente
from unidad.models import Unidad

#Para cargar expediente
from django.core.files.storage import default_storage
from usuarios.models import PerfilUser
#para crer directorios
from os import path
from os import makedirs
from genericpath import exists

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
    
    # @cambio
    # fecha : 31/03/2020
    # autor: lechuga
    # Explcación: se revisa si el expediente tiene algun archivo como metadato,
    #             de ser asi se le asigna true a la variable bandera, 
    #             caso contrario sele asigna false  
    cantiene_arhivos = False
    for metadato in metadatos:
        if metadato.tipo_dato.tipo == "Archivo":
            cantiene_arhivos = True
            break

    # @cambio
    # fecha : 31/03/2020
    # autor: lechuga
    # Explcación: se agrego un parametro en el return para especificar si uno de los metadotas
    #             es de tipo "Archivo"
    # Contenido del return:
    #   metadatos : metadatos           // Los metadatos que componen el expediente
    #   tipo : tipo                     // El tipo de expediente
    #   id : id                         // El id del expediente que se esta trabajando
    #   mensaje : 'metadatos'           // Mensaje a mostrar en la pagina
    #   bandera : cantiene_arhivos      // variable auxiliar que representa si el expediente
    #                                      tiene un metadato del tipo Archivo.
    return render(request,
                  'nuevo_exp_completo.html',
                  {'tipo': tipo,
                   'expediente': expediente,
                   'metadatos': metadatos,
                   'mensaje': 'Nuevo expediente',
                   'contiene_archivos' : cantiene_arhivos
                  })
    # @Anteriro 
    #return render(request, 'nuevo_exp_completo.html', {'tipo': tipo, 'expediente': expediente, 'metadatos': metadatos, 'mensaje': 'Nuevo expediente'})

# @login_required(redirect_field_name='login')
def VerExpediente(request, pk): # para mostrar el expediente
    usuarios = PerfilUser()
    usuarios = PerfilUser.objects.all().exclude(is_active=False).order_by('pk')
    expediente = Expediente.objects.get(pk=pk)
    metadatos = Metadato.objects.filter(expediente=pk).order_by('pk')
    ids_users = Expediente_aprobador.objects.filter(id_expediente=pk)
    # print(ids_users.query)
    seleccionados = []
    va = Expediente_aprobador()
    va = Expediente_aprobador.objects.filter(id_expediente=pk)
    for v in va:
        seleccionados.append(v)

   
    contiene_arhivos = expediente_tine_archivos(metadatos)

    #full_url = ''.join(['http://', get_current_site(request).domain, obj.get_absolute_url()])
    #url_archivo = get_current_site(request) 
    #return HttpResponse(url_archivo)

    # @cambio
    # fecha : 04/04/2020
    # autor: lechuga
    # Explcación: se agrego un parametro en el return para especificar si uno de los metadotas
    #             es de tipo "Archivo"
    # Contenido del return:
    #   expediente : int                // pk del expediente
    #   metadatos  : tupla              // tupla con todos los metadatos
    #   usuarios   : tupla              // tupla con todos los usuarios
    #   etiqueta   : string             // Mensaje a mostrar en la pagina
    #   contiene_arhivos : boolean      // variable auxiliar que representa si el expediente
    #                                      tiene un metadato del tipo Archivo.

    return render(request,
                 'ver_expediente.html',
                 {'expediente': expediente,
                  'metadatos': metadatos,
                  'usuarios': usuarios,
                  'etiqueta': 'Detalle expediente',
                  'seleccionados': seleccionados,
                  'contiene_arhivos' : contiene_arhivos
                  })

    # @Anteriro 
    #return render(request, 'ver_expediente.html', {'expediente': expediente, 'metadatos': metadatos, 'usuarios': usuarios, 'etiqueta': 'Detalle expediente', 'seleccionados': seleccionados})

# @login_required(redirect_field_name='login')
def AprobarExp(request, pk):
    expediente = Expediente.objects.get(pk=pk)
    metadatos = Metadato.objects.filter(expediente=pk).order_by('pk')
    ids_users = Expediente_aprobador.objects.filter(id_expediente=pk)
        
    return render(request, 'aprobar_expediente.html', {'expediente': expediente, 'metadatos': metadatos, 'etiqueta': 'Expediente recibido'})

# @login_required(redirect_field_name='login')
def ExpAprobado(request):
    user = get_user(request)
    user = request.user
    expediente = Expediente.objects.get(pk=request.POST['expediente'])
    metadatos = Metadato.objects.filter(expediente=expediente.pk).order_by('pk')
    ids_users = Expediente_aprobador.objects.filter(id_expediente=expediente.pk)
    Expediente.objects.filter(pk=expediente.pk).update(estatus=5)
    # Expediente.objects.filter(pk=expediente.pk).update(motivo_rechazo=request.POST['motivo_rechazo'])
    Expediente_aprobador.objects.filter(pk=expediente.pk).update(id_estatus=5)
    # Expediente_aprobador.objects.filter(pk=expediente.pk).update(motivo_rechazo=request.POST['motivo_rechazo'])
    # Expediente_aprobador.objects.filter(pk=expediente.pk, id_usuario=user.pk).delete()
    print(expediente)
    for metadato in metadatos:
        Metadato.objects.filter(pk=metadato.pk).update(id_estatus=5)
    # return HttpResponse(request.POST.items())
    user = get_user(request)
    user = request.user
    ids_users = Expediente_aprobador.objects.filter(id_usuario=user.pk)
    # print(ids_users.query)
    recibidos = []
    for id_usr in ids_users:
        recibidos.append(id_usr)
    # return render(request, 'exp_recibidos.html', {'recibidos': recibidos, 'etiqueta': 'Expedientes recibidos'})
    return render(request, 'aprobar_expediente.html', {'expediente': expediente, 'metadatos': metadatos, 'etiqueta': 'Expediente recibido'})

# @login_required(redirect_field_name='login')
def RechazarExp(request):
    user = get_user(request)
    user = request.user
    expediente = Expediente.objects.get(pk=request.POST['expediente'])
    metadatos = Metadato.objects.filter(expediente=expediente.pk).order_by('pk')
    ids_users = Expediente_aprobador.objects.filter(id_expediente=expediente.pk)
    Expediente.objects.filter(pk=expediente.pk).update(estatus=6)
    Expediente.objects.filter(pk=expediente.pk).update(motivo_rechazo=request.POST['motivo_rechazo'])
    Expediente_aprobador.objects.filter(pk=expediente.pk).update(id_estatus=6)
    Expediente_aprobador.objects.filter(pk=expediente.pk).update(motivo_rechazo=request.POST['motivo_rechazo'])
    # Expediente_aprobador.objects.filter(pk=expediente.pk, id_usuario=user.pk).delete()
    print(expediente)
    # return HttpResponse(request.POST.items())
    user = get_user(request)
    user = request.user
    ids_users = Expediente_aprobador.objects.filter(id_usuario=user.pk)
    # print(ids_users.query)
    recibidos = []
    for id_usr in ids_users:
        recibidos.append(id_usr)
    # return render(request, 'exp_recibidos.html', {'recibidos': recibidos, 'etiqueta': 'Expedientes recibidos'})
    return render(request, 'aprobar_expediente.html', {'expediente': expediente, 'metadatos': metadatos, 'etiqueta': 'Expediente recibido'})

# @login_required(redirect_field_name='login')
def ExpRecibidos(request):
    user = get_user(request)
    user = request.user
    ids_users = Expediente_aprobador.objects.filter(id_usuario=user.pk)
    # print(ids_users.query)
    recibidos = []
    for id_usr in ids_users:
        recibidos.append(id_usr)
       
    return render(request, 'exp_recibidos.html', {'recibidos': recibidos, 'etiqueta': 'Expedientes recibidos'})

# @login_required(redirect_field_name='login')
def AsignaExpediente(request):
    if request.method == "POST":
        usuarios = User.objects.all().order_by('pk')
        expediente = Expediente()
        expediente = Expediente.objects.get(pk=request.POST['expediente'])
        Expediente.objects.filter(pk=expediente.pk).update(estatus=3)
        metadatos = Metadato.objects.filter(expediente=expediente.pk).order_by('pk')
        ids_usuarios_sel = request.POST['users'].split(",")
        estatus = Estatus()
        estatus = Estatus.objects.get(pk=3)
        seleccionados = []
        for usuario in ids_usuarios_sel:
            # print(usuario)
            usr = User()
            usr = User.objects.get(pk=usuario)
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
        return render(request, 'ver_expediente.html', {'expediente': expediente, 'metadatos': metadatos, 'usuarios': usuarios, 'etiqueta': 'Detalle expediente', 'seleccionados': seleccionados})

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

        # return HttpResponse(request.POST.items())

        # @cambio
        # fecha : 04/04/2020
        # autor: lechuga
        # Explcación: Funcionalidad para guardar metadatos con archivos, 
        #

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
                #guardar el archivo
                url_archivo = guardar_archivo(ruta_archivo,metadato_archivo[1])
                # @cambio
                # fecha : 04/04/2020
                # autor: lechuga
                # Explcación: se elimina el primer caracter de lacadena '.' para poder guardar 
                #             la url 
                #
                url_archivo = url_archivo[1:]
                print(url_archivo)
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
            metadato.save()
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


            #
            #return(HttpResponse(request.FILES.items()))
            #return(HttpResponse(request.POST.items()))
            

            #

            #actializando metadatos con archivo 
            #obteniendo_archivos si existen
            if not request.FILES:
                #return HttpResponse("no se encontraron archivos en el POST primera linea")
                pass
            else :
                for archivo in request.FILES.items():
                    #return HttpResponse(archivo)
                    #metadato = Metadato.objects.get(pk=archivo[0])
                    nombre_metadato = Metadato.objects.get(pk=archivo[0]).nombre
                    pk_expediente = str(expediente.pk)
                    version = Metadato.objects.get(pk=archivo[0]).version
                    version = int(version) + 1
                    ruta_archivo = crea_carpeta('./media/'+
                                                pk_expediente+
                                                '/'+nombre_metadato+
                                                '/v'+
                                                str(version)+
                                                '/'
                                                )
                    #guardar el archivo
                    url_archivo = guardar_archivo(ruta_archivo,archivo[1])
                    print("guardando")
                    print(url_archivo)
                    url_archivo = url_archivo[1:]
                    #return HttpResponse(url_archivo)
                    Metadato.objects.filter(pk=archivo[0], expediente=exp).update(valor=url_archivo)
                    Metadato.objects.filter(pk=archivo[0], expediente=exp).update(version=version)
                     
            #actializando metadatos            
            vars = []
            for variable in request.POST.items():
                vars.append(variable)
            print(vars)
            for otro in vars[13:]:       
                         
            # @cambio
            # fecha : 06/04/2020
            # autor: lechuga
            # Explcación: se valida que e tipo del metadato no sea archivo dado que el POST
            #             cuando no se seleccionan archivos envia los camopos de tipo file
            #             en el POST.items() y no en el post.FILE.items(),por lo que hay que
            #             filttrarlos
                #return HttpResponse(Metadato.objects.get(pk=otro[0]).tipo_dato)
                if Metadato.objects.get(pk=otro[0]).tipo_dato.tipo == "Archivo":
                    #return HttpResponse(Metadato.objects.get(pk=otro[0]).tipo_dato)
                    pass
                else:
                    #return HttpResponse("modificando mal")
                    Metadato.objects.filter(pk=otro[0], expediente=exp).update(valor=otro[1])
                    Metadato.objects.filter(pk=otro[0], expediente=exp).update(version=2)

            # @anterios
                Metadato.objects.filter(pk=otro[0], expediente=exp).update(valor=otro[1])
                Metadato.objects.filter(pk=otro[0], expediente=exp).update(version=2)

            # return redirect('/expedientes/mis_expedientes')
            expediente = Expediente.objects.get(pk=request.POST.get('expediente',''))
            metadatos = Metadato.objects.filter(expediente=expediente.pk).order_by('pk')
            return render(request, 'detalle_expediente.html', {'expediente': expediente,'metadatos': metadatos, 'mensaje': 'Detalle expediente'})
        else:
            form = ExpedienteForm(instance=expediente)
        return render(request, 'edita_expediente.html', {'form': form, 'mensaje': 'Modificar expediente'})
    except ObjectDoesNotExist:
        return redirect('/expedientes/mis_expedientes')


# @login_required(redirect_field_name='login')
def DetalleExpediente(request, pk): #muestra expediente para ser modificado
    try:
        expediente = Expediente.objects.get(pk=pk)
        metadatos = Metadato.objects.filter(expediente=pk).order_by('pk')
        if request.method == "POST":
            form = ExpedienteForm(request.POST, instance=expediente)
            if form.is_valid():
                expediente = form.save()
                expediente.save()
                return redirect('/expedientes/mis_expedientes')
        # else:
            # form = ExpedienteForm(instance=expediente)


    # @cambio
    # fecha : 04/04/2020
    # autor: lechuga
    # Explcación: se agrego un parametro en el return para especificar sitio actual,
    #             al final no se utilizo y solo se acomodo el formato
    # Contenido del return:
    #   metadatos : metadatos           // Los metadatos que componen el expediente
    #   tipo : tipo                     // El tipo de expediente
    #   id : id                         // El id del expediente que se esta trabajando
    #   mensaje : 'metadatos'           // Mensaje a mostrar en la pagina
    #   bandera : cantiene_arhivos      // variable auxiliar que representa si el expediente
    #                                      tiene un metadato del tipo Archivo.        
        return render(request, 
                      'detalle_expediente.html', 
                       {'expediente': expediente, 
                        'metadatos': metadatos, 
                        'mensaje': 'Detalle expediente',
                       }
                      )
    except ObjectDoesNotExist:
        return redirect('/expedientes/mis_expedientes')
        #return HttpResponse(str(url_archivo) + str(metadatos[0]))

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
    expedientes = Expediente.objects.filter(usuario_crea=user).exclude(activo=False).order_by('pk')
    return render(request, 'mis_expedientes.html', {'expedientes': expedientes, 'mensaje': 'Expedientes'})

# @login_required(redirect_field_name='login')
def ListaMetadatosExp(request):
    if request.method == "GET":
        tipo = TipoExpediente()
        tipo = TipoExpediente.objects.get(pk=request.GET['pk'])

        id = Expediente()
        id = Expediente.objects.get(pk=request.GET['id'])

        metadatos = Metadato.objects.filter(tipo_expediente=tipo.pk).order_by('pk')

        #se revisa si el expediente tiene algun archivo como metadato,
        #de ser asi se le asigna true a la variable bandera, 
        #caso contrario sele asigna false  
        bandera = False
        for metadato in metadatos:
            if metadato.tipo_dato.tipo == "Archivo":
                bandera = True
                break

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
        return render(request,
                     'lista_metadatos_exp.html',
                     {'metadatos': metadatos, 
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
# def EliminarExpediente(request, pk):
#     try:
#         expediente = Expediente.objects.get(pk=pk)
#         expediente.delete()
#         return redirect('/expedientes/mis_expedientes')
#     except ObjectDoesNotExist:
#         return redirect('/expedientes/mis_expedientes')

# @login_required(redirect_field_name='login')
def EliminarExpediente(request, pk):
    try:
        expediente = Expediente.objects.get(pk=pk)
        Expediente.objects.filter(pk=pk).update(activo=False)
        return redirect('/expedientes/mis_expedientes')
    except ObjectDoesNotExist:
        return redirect('/expedientes/mis_expedientes')

# @creacióm de función
# fecha : 01/03/2020
# autor: lechuga        
def crea_carpeta(ruta ): # parametros 
                         #    ruta : string. Cadena que contenga la ruta
                         # retorno
                         #    string : ruta de la carpeta creada
    if not exists(ruta):
        makedirs(ruta)
    print(ruta)
    return ruta          # rwtorno : string. Cadena con la ruta creada
    


# @creacióm de función
# fecha : 01/03/2020
# autor: lechuga       
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


# @creacióm de función
# fecha : 01/03/2020
# autor: lechuga
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
