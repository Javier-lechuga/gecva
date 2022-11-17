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
from pydoc import apropos
from django.shortcuts import render
from estatus.models import Estatus
import expediente
from expediente.models import Expediente_deputy, Expediente_transferido
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
from metadato.models import Metadato, Xml_metadato
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
def CargaDatosXml(request):
    #raise Exception("Error")
    #return HttpResponse(request.FILES.items())
    #return HttpResponse(request.POST.items())
    user_log = PerfilUser.objects.get(pk=request.user.pk)
    metadatos = Metadato.objects.filter(tipo_expediente=request.POST['tipo'], base =1)
    expediente = ExpedienteForm()
    tipo = TipoExpediente()
    tipo = TipoExpediente.objects.get(pk=request.POST['tipo'])
    contiene_arhivos = expediente_tine_archivos(metadatos)
    archivo_xml = ""
    # valores retornados:
    #   tipo : tipo                     // El tipo de expediente
    #   expediente : definir            // definir el tipo
    #   metadatos : metadatos           // tupla con los metadatos que componen el expediente
    #   mensaje : 'metadatos'           // Mensaje a mostrar en la pagina
    #   contiene_archivos : bool        // variable auxiliar que representa si el expediente
    #                                      tiene un metadato del tipo Archivo.

    if not request.FILES:
        pass
    else:
        for metadato_archivo in request.FILES.items():
            # crear el directorio con el id del expediente, nombre del metadato y version,
            # la version simpre sera 1 cuando se crea un metadato nuevo
            #   ejemplo : ./media/nombre_metadato/pk_expediente/v1/
            #print(metadato_archivo)
            #
            archivo_xml = metadato_archivo[1]
            nombre_metadato = "factura"
            pk_expediente = "temporal"
            ruta_archivo = crea_carpeta('./media/'+pk_expediente+'/'+nombre_metadato+'/v1/')
            url_archivo = guardar_archivo(ruta_archivo,metadato_archivo[1])
            # se elimina el primer caracter de lacadena '.' para poder guardar la url 
            url_archivo = url_archivo[1:]
            url_final = "." + str(url_archivo)
            xml= open(url_final,"r")

            #return HttpResponse(request.FILES.items())

    #xml= open("facturas/18043.xml","r")
    #with open("C:/Users/Solusoft/OneDrive/Escritorio/gecva/static/facturas/8021215300.xml","rb") as f:
        #xml= open(str(f))
        #xml= open("C:/Users/Solusoft/OneDrive/Escritorio/gecva/static/facturas/8021215300.xml","r")

    #return HttpResponse(request.POST.items())
    
    mytree=minidom.parse(xml)

    comprobante = []

    # Comprobante
    tagname=mytree.getElementsByTagName('cfdi:Comprobante')[0]
    fecha= tagname.attributes['Fecha'].value
    folio= tagname.attributes['Folio'].value
    condicionesDePago= tagname.attributes['CondicionesDePago'].value
    subTotal= tagname.attributes['SubTotal'].value
    moneda= tagname.attributes['Moneda'].value
    total1= tagname.attributes['Total'].value
    tipoDeComprobante= tagname.attributes['TipoDeComprobante'].value
    metodoPago= tagname.attributes['MetodoPago'].value
    lugarExpedicion= tagname.attributes['LugarExpedicion'].value
    try:
        descuento = tagname.attributes['Descuento'].value
        print(descuento)
    except:
        descuento = False
        #print(descuento)

    comprobante.append({
                        "Comprobante":1,
                        "Fecha":fecha, 
                        "Folio":folio,
                        "CondicionesDePago":condicionesDePago,
                        "SubTotal":subTotal,
                        "Moneda":moneda,
                        "Total":total1,
                        "TipoDeComprobante":tipoDeComprobante,
                        "MetodoPago":metodoPago,
                        "LugarExpedicion":lugarExpedicion,
                        "Descuento":descuento,
                        })

    # Emisor
    emisor = []
    tagname=mytree.getElementsByTagName('cfdi:Emisor')[0]
    rfc= tagname.attributes['Rfc'].value
    nombre= tagname.attributes['Nombre'].value
    regimenFiscal= tagname.attributes['RegimenFiscal'].value

    emisor.append({
                        "Emisor":1,
                        "Rfc":rfc, 
                        "Nombre":nombre,
                        "RegimenFiscal":regimenFiscal,
                        })

    # Receptor
    receptor = []
    tagname=mytree.getElementsByTagName('cfdi:Receptor')[0]
    rfc= tagname.attributes['Rfc'].value
    nombre= tagname.attributes['Nombre'].value
    usoCFDI= tagname.attributes['UsoCFDI'].value

    receptor.append({
                        "Receptor":1,
                        "Rfc":rfc, 
                        "Nombre":nombre,
                        "UsoCFDI":usoCFDI,
                        })

    no_conceptos=mytree.getElementsByTagName('cfdi:Concepto')

    conceptos = []

    for i in range(len(no_conceptos)):

        # Concepto
        concepto=mytree.getElementsByTagName('cfdi:Concepto')[i]
        claveProdServ= concepto.attributes['ClaveProdServ'].value
        noIdentificacion= concepto.attributes['NoIdentificacion'].value
        cantidad= concepto.attributes['Cantidad'].value
        claveUnidad= concepto.attributes['ClaveUnidad'].value
        unidad= concepto.attributes['Unidad'].value
        descripcion= concepto.attributes['Descripcion'].value
        valorUnitario= concepto.attributes['ValorUnitario'].value
        importe= concepto.attributes['Importe'].value

        conceptos.append({
                        "concepto":i,
                        "ClaveProdServ":claveProdServ, 
                        "NoIdentificacion":noIdentificacion,
                        "Cantidad":cantidad,
                        "ClaveUnidad":claveUnidad,
                        "Unidad":unidad,
                        "Descripcion":descripcion,
                        "ValorUnitario":valorUnitario,
                        "Importe":importe,
                        })

    no_traslados=mytree.getElementsByTagName('cfdi:Traslados')

    traslados = []

    for i in range(len(no_traslados)):

        # Concepto
        traslado=mytree.getElementsByTagName('cfdi:Traslado')[i]
        impuesto= traslado.attributes['Impuesto'].value
        tipoFactor= traslado.attributes['TipoFactor'].value
        tasaOCuota= traslado.attributes['TasaOCuota'].value
        importe= traslado.attributes['Importe'].value

        traslados.append({
                        "traslado":i,
                        "Impuesto":impuesto, 
                        "TipoFactor":tipoFactor,
                        "TasaOCuota":tasaOCuota,
                        "Importe":importe,
                        })

    # print(comprobante)

    return render(request,
                  'nuevo_exp_completo.html',
                  {
                    'comprobante': comprobante,
                    'emisor':emisor,
                    'receptor':receptor,
                    'conceptos':conceptos,
                    'traslados':traslados,
                    'tipo': tipo,
                    'expediente': expediente,
                    'metadatos': metadatos,
                    'mensaje': 'Nuevo expediente',
                    'contiene_archivos' : contiene_arhivos,
                    'user_log': user_log,
                    'archivo_xml': archivo_xml,
                    'url_final' : url_final
                  })

# @login_required(redirect_field_name='login')
def VerExpediente(request, pk): # para mostrar el expediente
    user_log = PerfilUser.objects.get(pk=request.user.pk)
    usuarios = PerfilUser()
    usuarios = PerfilUser.objects.filter(unidad_user=user_log.unidad_user.pk, rol=3).exclude(is_active=False, pk=user_log.pk).order_by('pk')
    #usuarios = PerfilUser.objects.all().exclude(is_active=False, rol=3).order_by('pk')
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

    if expediente.usuario_crea == user_log:
        bandera = True
    else:
        bandera = False

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

    
    comprobante = []
    emisor = []
    receptor = []

    try:
        factura_xml = Xml_metadato.objects.get(expediente=expediente.pk)
        print(factura_xml)
    except:
        factura_xml = False
        print("El expediente no contiene factura XML")

    if (factura_xml):
        # Comprobante
        fecha= factura_xml.fecha_xml
        folio= factura_xml.folio
        condicionesDePago= factura_xml.cond_pago
        subTotal= factura_xml.subtotal
        moneda= factura_xml.moneda
        total1= factura_xml.total
        tipoDeComprobante= factura_xml.tipo_comprobante
        metodoPago= factura_xml.metodo_pago
        lugarExpedicion= factura_xml.lugar_exp
        try:
            descuento = factura_xml.descuento
            print(descuento)
        except:
            descuento = False
            #print(descuento)

        comprobante.append({
                            "Comprobante":1,
                            "Fecha":fecha, 
                            "Folio":folio,
                            "CondicionesDePago":condicionesDePago,
                            "SubTotal":subTotal,
                            "Moneda":moneda,
                            "Total":total1,
                            "TipoDeComprobante":tipoDeComprobante,
                            "MetodoPago":metodoPago,
                            "LugarExpedicion":lugarExpedicion,
                            "Descuento":descuento,
                            })

        # Emisor
        rfc_emisor= factura_xml.rfc_emisor
        nombre_emisor= factura_xml.nombre_emisor
        regimenFiscal_emisor= factura_xml.regimen_fiscal_emisor

        emisor.append({
                            "Emisor":1,
                            "Rfc":rfc_emisor, 
                            "Nombre":nombre_emisor,
                            "RegimenFiscal":regimenFiscal_emisor,
                            })

        # Receptor
        rfc_receptor= factura_xml.rfc_receptor
        nombre_receptor= factura_xml.nombre_receptor
        usoCFDI_receptor= factura_xml.regimen_fiscal_receptor

        receptor.append({
                            "Receptor":1,
                            "Rfc":rfc_receptor, 
                            "Nombre":nombre_receptor,
                            "UsoCFDI":usoCFDI_receptor,
                            })
        print(comprobante)
        print(emisor)
        print(receptor)
    

    return render(request,
                 'ver_expediente.html',
                 {  'comprobante': comprobante,
                    'emisor' : emisor,
                    'receptor' : receptor,
                    'expediente': expediente,
                    'metadatos': metadatos,
                    'usuarios': usuarios,
                    'etiqueta': 'Detalle expediente',
                    'seleccionados': seleccionados,
                    'contiene_arhivos' : contiene_arhivos,
                    'user_log' : user_log,
                    'bandera': bandera
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
    registro = Expediente_aprobador.objects.get(id_expediente=expediente.pk, id_usuario=user_log.pk)
    if registro.id_estatus.pk == 5:
        estado = "Aprobado"
    elif registro.id_estatus.pk == 6:
        estado = "Rechazado"
    else:
        estado = "Enviado"
    registro_log_user(user_log,"Consulta",expediente,"Expediente","Usuario")
    metadatos = Metadato.objects.filter(expediente=pk).order_by('pk')
    return render(request, 'aprobar_expediente.html', {'expediente': expediente, 'metadatos': metadatos, 'etiqueta': 'Expediente recibido','user_log':user_log, 'estado':estado})

# @login_required(redirect_field_name='login')
def ExpAprobado(request):
    user_log = PerfilUser.objects.get(pk=request.user.pk)
    unidad = Unidad.objects.get(pk=user_log.unidad_user.pk)
    estatus = Estatus()
    estatus = Estatus.objects.get(nombre="Aprobado")
    expediente = Expediente.objects.get(pk=request.POST['expediente'])
    metadatos = Metadato.objects.filter(expediente=expediente.pk).order_by('pk')
    valor = Expediente_aprobador.objects.get(id_expediente=expediente.pk, id_usuario=user_log.pk)
    Expediente_aprobador.objects.filter(pk=valor.pk).update(id_estatus=estatus)
    # Rol Revisor
    if user_log.rol.pk == 3:
        
        for metadato in metadatos:
            Metadato.objects.filter(pk=metadato.pk).update(estatus=estatus)

        # Se obtiene la cantidad de solicitudes de aprobacion del expediente 
        metas = Expediente_aprobador.objects.filter(id_expediente=expediente.pk)
        
        # Se obtienen las solicitudes aprobadas
        aprobados = Expediente_aprobador.objects.filter(id_expediente=expediente.pk, id_estatus=5, activo=True)
        reg_exp = Expediente_aprobador.objects.filter(id_expediente=expediente.pk).exclude(id_estatus=3)

        if len(metas) == len(aprobados):
            print("El archivo ya se aprobó por todos ya puede pasar al jefe de unidad")
            estatus_dos = Estatus()
            estatus_dos = Estatus.objects.get(nombre="Enviado")
            aprobador = PerfilUser()
            aprobador = PerfilUser.objects.get(pk=unidad.jefe_unidad.pk)
            exp_aprobador = Expediente_aprobador.objects.create(
                id_expediente = expediente,
                id_usuario = aprobador,
                id_estatus = estatus_dos,
                activo = True,
            )
            exp_aprobador.save()

        # if len(metas) == len(reg_exp):
        #     print("Checado pero no aprobado al 100%")
        #     estatus_tres = Estatus()
        #     estatus_tres = Estatus.objects.get(nombre="Aprobado")
        #     Expediente.objects.filter(pk=expediente.pk).update(estatus=estatus_tres)

    # Rol Aprobador
    elif user_log.rol.pk == 2:

        estatus_dos = Estatus()
        estatus_dos = Estatus.objects.get(nombre="Aprobado")
        Expediente.objects.filter(pk=expediente.pk).update(estatus=estatus_dos)
        Expediente_aprobador.objects.filter(pk=valor.pk).update(activo=False, id_estatus=estatus_dos)

    registro = Expediente_aprobador.objects.get(id_expediente=expediente.pk, id_usuario=user_log.pk)
    if registro.id_estatus.pk == 5:
        estado = "Aprobado"
    elif registro.id_estatus.pk == 6:
        estado = "Rechazado"
    else:
        estado = "Enviado"
    registro_log_user(user_log,"Aprueba",expediente,"Expediente","Usuario")
    expediente = Expediente.objects.get(pk=request.POST['expediente'])
    return render(request, 'aprobar_expediente.html', {'expediente': expediente, 'metadatos': metadatos, 'etiqueta': 'Expediente recibido','user_log':user_log, 'estado':estado})

# @login_required(redirect_field_name='login')
def RechazarExp(request):
    user_log = PerfilUser.objects.get(pk=request.user.pk)
    expediente = Expediente.objects.get(pk=request.POST['expediente'])
    metadatos = Metadato.objects.filter(expediente=expediente.pk).order_by('pk')
    estatus = Estatus()
    estatus = Estatus.objects.get(nombre="Rechazado")
    valor = Expediente_aprobador.objects.get(id_expediente=expediente.pk, id_usuario=user_log.pk)
    if user_log.rol.pk == 3:
        Expediente_aprobador.objects.filter(pk=valor.pk).update(id_estatus=estatus.pk)
        Expediente_aprobador.objects.filter(pk=valor.pk).update(motivo_rechazo=request.POST['motivo_rechazo'])
        registro = Expediente_aprobador.objects.get(id_expediente=expediente.pk, id_usuario=user_log.pk)
        Expediente.objects.filter(pk=expediente.pk).update(estatus=estatus.pk)

        # Se obtiene la cantidad de solicitudes de aprobacion del expediente 
        metas = Expediente_aprobador.objects.filter(id_expediente=expediente.pk, activo=True)
        
        # Se obtienen las solicitudes rechazadas
        rechazados = Expediente_aprobador.objects.filter(id_expediente=expediente.pk, id_estatus=6)
        if len(metas) == len(rechazados):
            print("El archivo cancelado por todos, ya se puede cancelar el expediente")
            estatus_tres = Estatus()
            estatus_tres = Estatus.objects.get(nombre="Rechazado")
            Expediente.objects.filter(pk=expediente.pk).update(estatus=estatus_tres)

        if registro.id_estatus.pk == 5:
            estado = "Aprobado"
        elif registro.id_estatus.pk == 6:
            estado = "Rechazado"
        else:
            estado = "Enviado"
        registro_log_user(user_log,"Rechaza",expediente,"Expediente","Usuario")
        expediente = Expediente.objects.get(pk=request.POST['expediente'])
        return render(request, 'aprobar_expediente.html', {'expediente': expediente, 'metadatos': metadatos, 'etiqueta': 'Expediente recibido','user_log':user_log, 'estado':estado})
    elif user_log.rol.pk == 2:
        Expediente.objects.filter(pk=expediente.pk).update(estatus=estatus.pk)
        Expediente.objects.filter(pk=expediente.pk).update(motivo_rechazo=request.POST['motivo_rechazo'])
        registro = Expediente.objects.get(pk=expediente.pk)
        if registro.estatus.pk == 5:
            estado = "Aprobado"
        elif registro.estatus.pk == 6:
            estado = "Rechazado"
        else:
            estado = "Enviado"
        registro_log_user(user_log,"Rechaza",expediente,"Expediente","Usuario")
        expediente = Expediente.objects.get(pk=request.POST['expediente'])
        return render(request, 'aprobar_expediente.html', {'expediente': expediente, 'metadatos': metadatos, 'etiqueta': 'Expediente recibido','user_log':user_log, 'estado':estado})
    

# @login_required(redirect_field_name='login')
def ExpRecibidos(request):
    user_log = PerfilUser.objects.get(pk=request.user.pk)
    registro_log_user(user_log,"Consulta Recibidos",None,"Expedientes","Usuario")
    ids_users = Expediente_aprobador.objects.filter(id_usuario=user_log.pk).order_by("-pk")
    recibidos = []
    for id_usr in ids_users:
        recibidos.append(id_usr)
    return render(request, 'exp_recibidos.html', {'recibidos': recibidos, 'etiqueta': 'Expedientes recibidos','user_log':user_log})

# @login_required(redirect_field_name='login')
def AsignaExpediente(request):
    user_log = PerfilUser.objects.get(pk=request.user.pk)
    # return HttpResponse(request.POST.items())
    if request.method == "POST":
        usuarios = User.objects.all().order_by('pk')
        expediente = Expediente()
        expediente = Expediente.objects.get(pk=request.POST['expediente'])
        registro_log_user(user_log,"Asigna",expediente,"Expediente","Usuario")
        #Expediente.objects.filter(pk=expediente.pk).update(estatus=3)
        metadatos = Metadato.objects.filter(expediente=expediente.pk).order_by('pk')
        ids_usuarios_sel = request.POST['users'].split(",")
        estatus = Estatus()
        estatus = Estatus.objects.get(pk=7)
        Expediente.objects.filter(pk=expediente.pk).update(estatus=estatus)
        expediente = Expediente.objects.get(pk=request.POST['expediente'])
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
                activo = True,
            )
            exp_aprobador.save()
        va = Expediente_aprobador()
        va = Expediente_aprobador.objects.filter(id_expediente=expediente.pk)
        for v in va:
            seleccionados.append(v)
        # return HttpResponse(request.POST.items())
        return render(request, 'ver_expediente.html', {'expediente': expediente, 'metadatos': metadatos, 'usuarios': usuarios, 'etiqueta': 'Detalle expediente', 'seleccionados': seleccionados, 'user_log': user_log, 'bandera':True})
import shutil
# @login_required(redirect_field_name='login')
def NuevoExpCompleto(request):
    user_log = PerfilUser.objects.get(pk=request.user.pk)
    if request.method == "POST":
        # return HttpResponse(request.POST.items())
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
        # for val in request.POST.items():
        #     print(val)
        # return HttpResponse(request.POST.items())
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
        if type(vars[8:]) == int:
            for otro in vars[8:]:
                metas.append(otro)
                tipo = otro[0]
        elif type(vars[23:]) == int:
            for otro in vars[8:]:
                metas.append(otro)
                tipo = otro[0]
        for valor in metas:
            #Instanciando Metadato
            meta = Metadato()
            # print("Aqui esta el valor")
            # print(valor[0])
            # return HttpResponse(request.POST.items())
            meta = Metadato.objects.get(pk=valor[0])
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
        if request.POST.get('metadato',''):
            metadato = Metadato()
            metadato = Metadato.objects.get(pk=request.POST.get('metadato',''))
            nombre_metadato = metadato.nombre
            pk_expediente = str(nuevo_expediente.pk)
            url_final = "./media/temporal/factura/v1/" + str(request.POST.get('archivo_xml',''))
            ruta_archivo = crea_carpeta('./media/'+pk_expediente+'/'+nombre_metadato+'/v1/')
            ruta_archivo = ruta_archivo + str(request.POST.get('archivo_xml',''))
            print(ruta_archivo)
            shutil.move(url_final, ruta_archivo)
            url_archivo = ruta_archivo[1:]
            print(url_archivo)
            #crear el metadato
            metadato = Metadato()
            metadato = Metadato.objects.get(pk=request.POST.get('metadato',''),)
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
        else:
            print("No viene el metadato")
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
                
                # Agregar el if si el expediente contiene XML
                if (request.POST.get('fecha_xml','')):
                    # Creando el XML
                    exp_xml = Expediente()
                    exp_xml = Expediente.objects.get(pk=nuevo_expediente.pk)
                    xml_metadato = Xml_metadato.objects.create(

                        expediente = exp_xml,

                        # Datos generales
                        fecha_xml = request.POST.get('fecha_xml',''),
                        folio = request.POST.get('folio_xml',''),
                        cond_pago = request.POST.get('pago_xml',''),
                        moneda = request.POST.get('moneda_xml',''),
                        tipo_comprobante = request.POST.get('comprobante_xml',''),
                        metodo_pago = request.POST.get('metodo_xml',''),
                        lugar_exp = request.POST.get('lugar_xml',''),
                        subtotal = request.POST.get('subtotal_xml',''),
                        descuento = request.POST.get('descuento_xml',''),
                        total = request.POST.get('total_xml',''),

                        # Datos emisor
                        rfc_emisor = request.POST.get('rfc_emisor',''),
                        nombre_emisor = request.POST.get('nombre_emisor',''),
                        regimen_fiscal_emisor = request.POST.get('regimen_emisor',''),

                        # Datos receptor
                        rfc_receptor = request.POST.get('rfc_receptor',''),
                        nombre_receptor = request.POST.get('nombre_receptor',''),
                        regimen_fiscal_receptor = request.POST.get('usoCFDI_receptor',''),

                    )
                    xml_metadato.save()


        #return HttpResponse(request.POST.items())
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
            registros = Expediente_aprobador.objects.filter(id_expediente=expediente.pk)
            for registro in registros:
                Expediente_aprobador.objects.get(pk=registro.pk).delete()
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

        comprobante = []
        emisor = []
        receptor = []

        try:
            factura_xml = Xml_metadato.objects.get(expediente=expediente.pk)
            print(factura_xml)
        except:
            factura_xml = False
            print("El expediente no contiene factura XML")

        if (factura_xml):
            # Comprobante
            fecha= factura_xml.fecha_xml
            folio= factura_xml.folio
            condicionesDePago= factura_xml.cond_pago
            subTotal= factura_xml.subtotal
            moneda= factura_xml.moneda
            total1= factura_xml.total
            tipoDeComprobante= factura_xml.tipo_comprobante
            metodoPago= factura_xml.metodo_pago
            lugarExpedicion= factura_xml.lugar_exp
            try:
                descuento = factura_xml.descuento
                print(descuento)
            except:
                descuento = False
                #print(descuento)

            comprobante.append({
                                "Comprobante":1,
                                "Fecha":fecha, 
                                "Folio":folio,
                                "CondicionesDePago":condicionesDePago,
                                "SubTotal":subTotal,
                                "Moneda":moneda,
                                "Total":total1,
                                "TipoDeComprobante":tipoDeComprobante,
                                "MetodoPago":metodoPago,
                                "LugarExpedicion":lugarExpedicion,
                                "Descuento":descuento,
                                })

            # Emisor
            rfc_emisor= factura_xml.rfc_emisor
            nombre_emisor= factura_xml.nombre_emisor
            regimenFiscal_emisor= factura_xml.regimen_fiscal_emisor

            emisor.append({
                                "Emisor":1,
                                "Rfc":rfc_emisor, 
                                "Nombre":nombre_emisor,
                                "RegimenFiscal":regimenFiscal_emisor,
                                })

            # Receptor
            rfc_receptor= factura_xml.rfc_receptor
            nombre_receptor= factura_xml.nombre_receptor
            usoCFDI_receptor= factura_xml.regimen_fiscal_receptor

            receptor.append({
                                "Receptor":1,
                                "Rfc":rfc_receptor, 
                                "Nombre":nombre_receptor,
                                "UsoCFDI":usoCFDI_receptor,
                                })
            print(comprobante)
            print(emisor)
            print(receptor)

        return render(request, 
                      'detalle_expediente.html', 
                       {'comprobante': comprobante,
                        'emisor': emisor,
                        'receptor': receptor,
                        'expediente': expediente, 
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
    usuarios = PerfilUser.objects.filter(unidad_user=user_log.unidad_user).exclude(pk=user_log.pk)
    #usuarios = PerfilUser.objects.all().exclude(pk=user_log.pk)
    expedientes = Expediente.objects.filter(usuario_crea=user, unidad=user_log.unidad_user.pk).exclude(activo=False).order_by('-fecha_creacion')
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
    #expedientes = Expediente.objects.all().order_by("-fecha_creacion")
    expedientes = Expediente.objects.filter(unidad=user_log.unidad_user.pk).exclude(estatus=1).order_by("-fecha_creacion")
    # expedientes = Expediente.objects.all().exclude(estatus=1).order_by("-fecha_creacion")
    return render(request, 'busca_expedientes.html', {'expedientes': expedientes, 'mensaje': 'Búsqueda de expedientes','user_log':user_log})

# @login_required(redirect_field_name='login')
def RecibidosDeputy(request):
    user_log = PerfilUser.objects.get(pk=request.user.pk)
    # recibidos = Expediente_deputy.objects.all()
    recibidos = Expediente_deputy.objects.filter(deputy=user_log)
    registro_log_user(user_log,"Consulta",None,"Expedientes deputy","Usuario")
    # registros = Registra_actividad.objects.all().exclude(rol="Usuario").order_by("-pk")
    return render(request, 'exp_deputy.html', {'recibidos': recibidos, 'mensaje': 'Expedientes deputy','user_log':user_log, 'bandera' : True})

from xml.dom import minidom

# @login_required(redirect_field_name='login')
def CargaXml(request):
    user_log = PerfilUser.objects.get(pk=request.user.pk)
    
    #xml= open("facturas/18043.xml","r")
    xml= open("C:/Users/Solusoft/OneDrive/Escritorio/gecva/static/facturas/8021215300.xml","r")
    
    mytree=minidom.parse(xml)

    comprobante = []

    # Comprobante
    #print("Datos del Comprobante")
    tagname=mytree.getElementsByTagName('cfdi:Comprobante')[0]
    fecha= tagname.attributes['Fecha'].value
    #comprobante.append({"Fecha":fecha})
    #print(fecha)
    folio= tagname.attributes['Folio'].value
    #print(folio)
    #comprobante.append({"Folio":folio})
    condicionesDePago= tagname.attributes['CondicionesDePago'].value
    #print(condicionesDePago)
    #comprobante.append({"CondicionesDePago":condicionesDePago})
    subTotal= tagname.attributes['SubTotal'].value
    #print(subTotal)
    #comprobante.append({"SubTotal":subTotal})
    #descuento1= tagname.attributes['Descuento'].value
    #print(descuento1)
    moneda= tagname.attributes['Moneda'].value
    #print(moneda)
    #comprobante.append({"Moneda":moneda})
    total1= tagname.attributes['Total'].value
    #print(total1)
    #comprobante.append({"Total":total1})
    tipoDeComprobante= tagname.attributes['TipoDeComprobante'].value
    #print(tipoDeComprobante)
    #comprobante.append({"TipoDeComprobante":tipoDeComprobante})
    #exportacion= tagname.attributes['Exportacion'].value
    #print(exportacion)
    metodoPago= tagname.attributes['MetodoPago'].value
    #print(metodoPago)
    #comprobante.append({"MetodoPago":metodoPago})
    lugarExpedicion= tagname.attributes['LugarExpedicion'].value
    #print(lugarExpedicion)
    #comprobante.append({"LugarExpedicion":lugarExpedicion})
    #exportacion= tagname.attributes['Exportacion'].value
    #print(exportacion)
    try:
        descuento = tagname.attributes['Descuento'].value
        print(descuento)
    except:
        descuento = False
        print(descuento)

    comprobante.append({
                        "Comprobante":1,
                        "Fecha":fecha, 
                        "Folio":folio,
                        "CondicionesDePago":condicionesDePago,
                        "SubTotal":subTotal,
                        "Moneda":moneda,
                        "Total":total1,
                        "TipoDeComprobante":tipoDeComprobante,
                        "MetodoPago":metodoPago,
                        "LugarExpedicion":lugarExpedicion,
                        "Descuento":descuento,
                        })

    # Emisor
    emisor = []
    #print("Datos del emisor")
    tagname=mytree.getElementsByTagName('cfdi:Emisor')[0]
    # print(tagname)
    rfc= tagname.attributes['Rfc'].value
    #print(rfc)
    nombre= tagname.attributes['Nombre'].value
    #print(nombre)
    regimenFiscal= tagname.attributes['RegimenFiscal'].value
    #print(regimenFiscal)

    emisor.append({
                        "Emisor":1,
                        "Rfc":rfc, 
                        "Nombre":nombre,
                        "RegimenFiscal":regimenFiscal,
                        })

    # Receptor
    receptor = []
    #print("Datos del Receptor")
    tagname=mytree.getElementsByTagName('cfdi:Receptor')[0]
    rfc= tagname.attributes['Rfc'].value
    #print(rfc)
    nombre= tagname.attributes['Nombre'].value
    #print(nombre)
    usoCFDI= tagname.attributes['UsoCFDI'].value
    #print(usoCFDI)

    receptor.append({
                        "Receptor":1,
                        "Rfc":rfc, 
                        "Nombre":nombre,
                        "UsoCFDI":usoCFDI,
                        })

    no_conceptos=mytree.getElementsByTagName('cfdi:Concepto')

    conceptos = []

    for i in range(len(no_conceptos)):

        # Concepto
        #print("Datos del Concepto")
        concepto=mytree.getElementsByTagName('cfdi:Concepto')[i]
        claveProdServ= concepto.attributes['ClaveProdServ'].value
        #print(claveProdServ)
        noIdentificacion= concepto.attributes['NoIdentificacion'].value
        #print(noIdentificacion)
        cantidad= concepto.attributes['Cantidad'].value
        #print(cantidad)
        claveUnidad= concepto.attributes['ClaveUnidad'].value
        #print(claveUnidad)
        unidad= concepto.attributes['Unidad'].value
        #print(unidad)
        descripcion= concepto.attributes['Descripcion'].value
        #print(descripcion)
        valorUnitario= concepto.attributes['ValorUnitario'].value
        #print(valorUnitario)
        importe= concepto.attributes['Importe'].value
        #print(importe)
        
        
        #objetoImp= concepto.attributes['ObjetoImp'].value
        #print(objetoImp)

        conceptos.append({
                        "concepto":i,
                        "ClaveProdServ":claveProdServ, 
                        "NoIdentificacion":noIdentificacion,
                        "Cantidad":cantidad,
                        "ClaveUnidad":claveUnidad,
                        "Unidad":unidad,
                        "Descripcion":descripcion,
                        "ValorUnitario":valorUnitario,
                        "Importe":importe,
                        })

    #comprobante.append(conceptos)

    no_traslados=mytree.getElementsByTagName('cfdi:Traslados')

    traslados = []

    for i in range(len(no_traslados)):

        # Concepto
        #print("Datos del Concepto")
        traslado=mytree.getElementsByTagName('cfdi:Traslado')[i]
        impuesto= traslado.attributes['Impuesto'].value
        #print(impuesto)
        tipoFactor= traslado.attributes['TipoFactor'].value
        #print(tipoFactor)
        tasaOCuota= traslado.attributes['TasaOCuota'].value
        #print(tasaOCuota)
        importe= traslado.attributes['Importe'].value
        #print(importe)

        traslados.append({
                        "traslado":i,
                        "Impuesto":impuesto, 
                        "TipoFactor":tipoFactor,
                        "TasaOCuota":tasaOCuota,
                        "Importe":importe,
                        })

    #comprobante.append(traslados)

    #print("Aqui se encuentra el comprobante")
    #print(comprobante)


    registro_log_user(user_log,"Carga",None,"datos de XML","Usuario")
    return render(request, 'carga_xml.html', {'comprobante': comprobante, 'emisor':emisor, 'receptor':receptor, 'conceptos':conceptos, 'traslados':traslados,'user_log':user_log, 'etiqueta':"Detalle XML"})

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

# @login_required(redirect_field_name='login')
def UsuarioLog(request):
    user_log = PerfilUser.objects.get(pk=request.user.pk)
    registro_log_user(user_log,"Consulta",None,"Log personal","Usuario")
    registros = Registra_actividad.objects.filter(usuario=user_log.pk).order_by("-fecha")
    return render(request, 'log_user.html', {'registros': registros, 'mensaje': 'Log personal','user_log':user_log})

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

        #PerfilUser.objects.filter(pk=usuario_origen.pk).update(transferido=True)
        PerfilUser.objects.filter(pk=usuario_destino.pk).update(es_deputy=True)
        PerfilUser.objects.filter(pk=usuario_origen.pk).update(deputy=True)
        PerfilUser.objects.filter(pk=usuario_origen.pk).update(usuario_deputy=usuario_destino)
        user_log = PerfilUser.objects.get(pk=request.user.pk)
        registro_log_admin(user_log,"Asigna deputy",usuario," Al usuario",usuario_destino.first_name + " " + usuario_destino.last_name + " " + usuario_destino.amaterno)
        # return HttpResponse(request.POST.items())
        return render(request, 'mis_expedientes.html', {'expedientes': expedientes, 'usuarios': usuarios ,'mensaje': 'Mis expedientes','user_log':user_log})
    except ObjectDoesNotExist:
        return redirect('principal')

# @login_required(redirect_field_name='login')
def CancelaDeputy(request):
    user_log = PerfilUser.objects.get(pk=request.user.pk)
    try:
        usuarios = PerfilUser.objects.all().exclude(pk=user_log.pk)
        expedientes_a_remover = Expediente_deputy.objects.filter(usuario_crea=user_log.pk)
        expedientes = Expediente.objects.filter(usuario_crea=user_log.pk)
        
        #return HttpResponse(request.POST.items())
        for remover in expedientes_a_remover:
            Expediente_deputy.objects.filter(pk=remover.pk).delete()
            #PerfilUser.objects.filter(pk=remover.deputy).update(transferido=False)
        #PerfilUser.objects.filter(pk=usuario_origen.pk).update(transferido=True)
        PerfilUser.objects.filter(pk=user_log.pk).update(usuario_deputy='')
        PerfilUser.objects.filter(pk=user_log.pk).update(deputy=False)
        PerfilUser.objects.filter(pk=user_log.usuario_deputy.pk).update(es_deputy=False)
        registro_log_admin(user_log,"Termina deputy",user_log," del usuario",'')
        # return HttpResponse(request.POST.items())
        user_log = PerfilUser.objects.get(pk=request.user.pk)
        return render(request, 'mis_expedientes.html', {'expedientes': expedientes, 'usuarios': usuarios ,'mensaje': 'Mis expedientes','user_log':user_log})
    except ObjectDoesNotExist:
        return redirect('principal')

# @login_required(redirect_field_name='login')
def TransferirUsuarios(request):
    user_log = PerfilUser.objects.get(pk=request.user.pk)
    usuarios = PerfilUser.objects.filter(is_active=True, unidad_user=user_log.unidad_user).exclude(pk=user_log.pk)
    #usuarios = PerfilUser.objects.all().exclude(pk=user_log.pk)
    expedientes = Expediente.objects.filter(usuario_crea=user_log)
    
    #return HttpResponse(request.POST.items())
    registro_log_user(user_log,"Consulta usuarios ",None," para transferir expedientes",'')
    return render(request, 'transferir_usuarios.html', {'expedientes': expedientes, 'usuarios': usuarios ,'mensaje': 'Seleccionar usuario','user_log':user_log})

# @login_required(redirect_field_name='login')
def TransferirExpedientes(request):
    user_log = PerfilUser.objects.get(pk=request.user.pk)
    usuarios = PerfilUser.objects.filter(is_active=True).exclude(pk=user_log.pk)
    usuario_destino = PerfilUser.objects.get(pk=request.POST['usuario_destino'])
    expedientes = Expediente.objects.filter(usuario_crea=user_log)

    ids_exp_sel = request.POST['expedientes'].split(",")
    for exp in ids_exp_sel:
        expediente = Expediente.objects.get(pk=exp)
        transferido = Expediente_transferido.objects.create(
            expediente = expediente,
            usuario_crea = expediente.usuario_crea,
            usuario_asignado = usuario_destino,
            activo = True,
        )
        Expediente.objects.filter(pk=expediente.pk).update(usuario_anterior=expediente.usuario_crea)
        Expediente.objects.filter(pk=expediente.pk).update(usuario_crea=usuario_destino)
        registro_log_user(user_log,"Transfiere ",expediente," expediente a",usuario_destino.first_name + " " + usuario_destino.last_name + " " + usuario_destino.amaterno)
        transferido.save()
    user_log = PerfilUser.objects.get(pk=request.user.pk)
    anuncio = "Expediente(s) transferido(s) correctamente"
    #return HttpResponse(request.POST.items())
    return render(request, 'transferir_usuarios.html', {'expedientes': expedientes, 'usuarios': usuarios ,'mensaje': 'Seleccionar usuario','user_log':user_log, 'anuncio': anuncio})

# @login_required(redirect_field_name='login')
def RegresarExpediente(request,pk):
    user_log = PerfilUser.objects.get(pk=request.user.pk)
    usuarios = PerfilUser.objects.filter(is_active=True).exclude(pk=user_log.pk)
    expedientes = Expediente.objects.filter(usuario_crea=user_log)

    expediente = Expediente.objects.get(pk=pk)
    usuario_destino = expediente.usuario_anterior
    
    Expediente.objects.filter(pk=expediente.pk).update(usuario_anterior=None)
    Expediente.objects.filter(pk=expediente.pk).update(usuario_crea=usuario_destino)
    Expediente_transferido.objects.filter(expediente=expediente, usuario_asignado=user_log, activo=True).update(activo=False)
    registro_log_user(user_log,"Regresa ",expediente," expediente a",usuario_destino.first_name + " " + usuario_destino.last_name + " " + usuario_destino.amaterno)

    anuncio = "Expediente regresado correctamente"
    #return HttpResponse(request.POST.items())
    return render(request, 'mis_expedientes.html', {'expedientes': expedientes, 'usuarios': usuarios ,'mensaje': 'Mis expedientes','user_log':user_log, 'anuncio': anuncio})

# @login_required(redirect_field_name='login')
def AceptarExpediente(request,pk):
    user_log = PerfilUser.objects.get(pk=request.user.pk)
    usuarios = PerfilUser.objects.filter(is_active=True).exclude(pk=user_log.pk)
    expedientes = Expediente.objects.filter(usuario_crea=user_log).exclude(activo=False).order_by('-fecha_creacion')

    expediente = Expediente.objects.get(pk=pk)
    #usuario_destino = expediente.usuario_anterior
    
    Expediente.objects.filter(pk=expediente.pk).update(usuario_anterior=None)
    # Expediente.objects.filter(pk=expediente.pk).update(usuario_crea=usuario_destino)
    Expediente_transferido.objects.filter(expediente=expediente, usuario_crea=expediente.usuario_anterior, activo=True).update(activo=False)
    anterior = PerfilUser.objects.get(pk=expediente.usuario_anterior)
    registro_log_user(user_log,"Acepta ",expediente," expediente del usuario",anterior.first_name + " " + anterior.last_name + " " + anterior.amaterno)

    anuncio = "Expediente aceptado"
    #return HttpResponse(request.POST.items())
    return render(request, 'mis_expedientes.html', {'expedientes': expedientes, 'usuarios': usuarios ,'mensaje': 'Mis expedientes','user_log':user_log, 'anuncio': anuncio})

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

    expedientes = Expediente()
    expedientes = Expediente.objects.filter(usuario_crea=usuario.pk)
    total_expedientes = len(expedientes)

    #Ver como dividir la lista en ciertos elementos
    lista_buena = particionar_lista(expedientes, 3)

    #Eliminamos listas vacias
    for x in range(len(lista_buena)-1,-1,-1):
        if lista_buena[x]:
            print("")
        else:
            #print("No tiene datos")
            lista_buena.pop(x)

    #Obtenemos el numero de listas de la lista
    total_listas = len(lista_buena)

    myDate = datetime.datetime.now()
    fecha_formateada = myDate.strftime("%d-%m-%Y")
    
    # Create the HttpResponse headers with PDF
    response = HttpResponse(content_type='applicacion/pdf')
    response['Content-Disposition'] = 'attachment; filename=REPORTE-' + usuario.first_name + '-' + usuario.last_name + '-' + usuario.amaterno + '-' + fecha_formateada + '.pdf'
    
    # Create the PDF object. using the BytesIO object as its "file"
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)
    index = 0
    pagina_actual = 0

    for lista in lista_buena:
    
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

        pagina_actual+=1
        c.setFont('Helvetica', 9)
        c.drawString(480,30,'Página ' + str(pagina_actual) +' de ' + str(total_listas))

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

        otro = []
        otro.append([id, fecha_creacion, identificador, estatus, nombre])
        for expediente in lista:
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
        c.showPage()
        # c.showPage() # save page

    registro_log_admin(user_log,"Genera",usuario,"Reporte por usuario","Administrador")
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
    
    unidad = Unidad()
    unidad = Unidad.objects.get(pk=pk)

    expedientes = Expediente()
    expedientes = Expediente.objects.filter(unidad=unidad.pk)
    total_expedientes = len(expedientes)

    #Ver como dividir la lista en ciertos elementos
    lista_buena = particionar_lista(expedientes, 3)

    #Eliminamos listas vacias
    for x in range(len(lista_buena)-1,-1,-1):
        if lista_buena[x]:
            print("")
        else:
            #print("No tiene datos")
            lista_buena.pop(x)

    #Obtenemos el numero de listas de la lista
    total_listas = len(lista_buena)

    myDate = datetime.datetime.now()
    fecha_formateada = myDate.strftime("%d-%m-%Y")
    
    # Create the HttpResponse headers with PDF
    response = HttpResponse(content_type='applicacion/pdf')
    response['Content-Disposition'] = 'attachment; filename=REPORTE-' + unidad.nombre + "-" + fecha_formateada + '.pdf'
    
    # Create the PDF object. using the BytesIO object as its "file"
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)
    index = 0
    pagina_actual = 0

    for lista in lista_buena:
    
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

        pagina_actual+=1
        c.setFont('Helvetica', 9)
        c.drawString(480,30,'Página ' + str(pagina_actual) +' de ' + str(total_listas))

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

        otro = []
        otro.append([id, fecha_creacion, identificador, estatus, nombre])
        for expediente in lista:
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
        c.showPage()
        # c.showPage() # save page

    registro_log_admin(user_log,"Genera",unidad,"Reporte por unidad","Administrador")
    # save PDF
    c.save()
    
    # get the value of BytesIO buffer and write response
    pdf = buffer.getvalue()
    buffer.close()
    response.write(pdf)
    return response

# @login_required(redirect_field_name='login')
def particionar_lista(lista, n): 
    return [lista[i*n:i*n+n] for i in range(n)]

# @login_required(redirect_field_name='login')
def ReporteGeneral(request): # estes el buenos

    user_log = PerfilUser.objects.get(pk=request.user.pk)

    expedientes = Expediente()
    expedientes = Expediente.objects.all()
    total_expedientes = len(expedientes)

    #Ver como dividir la lista en ciertos elementos
    lista_buena = particionar_lista(expedientes, 3)

    #Eliminamos listas vacias
    for x in range(len(lista_buena)-1,-1,-1):
        if lista_buena[x]:
            print("")
        else:
            #print("No tiene datos")
            lista_buena.pop(x)

    #Obtenemos el numero de listas de la lista
    total_listas = len(lista_buena)

    myDate = datetime.datetime.now()
    fecha_formateada = myDate.strftime("%d-%m-%Y")
    
    # Create the HttpResponse headers with PDF
    response = HttpResponse(content_type='applicacion/pdf')
    response['Content-Disposition'] = 'attachment; filename=REPORTE-GENERAL' + fecha_formateada + '.pdf'

    # Create the PDF object. using the BytesIO object as its "file"
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)
    index = 0
    pagina_actual = 0

    for lista in lista_buena:
        
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

        pagina_actual+=1
        c.setFont('Helvetica', 9)
        c.drawString(480,30,'Página ' + str(pagina_actual) +' de ' + str(total_listas))

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

        otro = []
        otro.append([id, fecha_creacion, identificador, estatus, unidad, nombre])
        #for expediente in expedientes:
        for expediente in lista:
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
        c.showPage()
            
    registro_log_admin(user_log,"Genera",None,"Reporte general","Administrador")

    c.save()
    
    # get the value of BytesIO buffer and write response
    pdf = buffer.getvalue()
    buffer.close()
    response.write(pdf)

    return response

# @login_required(redirect_field_name='login')
def ReporteUsuarios(request):

    user_log = PerfilUser.objects.get(pk=request.user.pk)

    usuarios = PerfilUser()
    usuarios = PerfilUser.objects.all()
    total_usuarios = len(usuarios)

    #Ver como dividir la lista en ciertos elementos
    lista_buena = particionar_lista(usuarios, 3)

    #Eliminamos listas vacias
    for x in range(len(lista_buena)-1,-1,-1):
        if lista_buena[x]:
            print("")
        else:
            #print("No tiene datos")
            lista_buena.pop(x)

    #Obtenemos el numero de listas de la lista
    total_listas = len(lista_buena)

    myDate = datetime.datetime.now()
    fecha_formateada = myDate.strftime("%d-%m-%Y")
    
    # Create the HttpResponse headers with PDF
    response = HttpResponse(content_type='applicacion/pdf')
    response['Content-Disposition'] = 'attachment; filename=REPORTE-USUARIOS' + fecha_formateada + '.pdf'
    
    # Create the PDF object. using the BytesIO object as its "file"
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)
    index = 0
    pagina_actual = 0

    for lista in lista_buena:
    
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

        pagina_actual+=1
        c.setFont('Helvetica', 9)
        c.drawString(480,30,'Página ' + str(pagina_actual) +' de ' + str(total_listas))

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

        otro = []
        otro.append([id, nombre, correo, estatus, creado, ultimo_log])
        for usuario in lista:
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
        c.showPage()
        # c.showPage() # save page
    registro_log_admin(user_log,"Genera",None,"Reporte de usuarios","Administrador")

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
    
    unidades = Unidad()
    unidades = Unidad.objects.all()
    total_unidades = len(unidades)

    #Ver como dividir la lista en ciertos elementos
    lista_buena = particionar_lista(unidades, 3)

    #Eliminamos listas vacias
    for x in range(len(lista_buena)-1,-1,-1):
        if lista_buena[x]:
            print("")
        else:
            #print("No tiene datos")
            lista_buena.pop(x)

    #Obtenemos el numero de listas de la lista
    total_listas = len(lista_buena)

    myDate = datetime.datetime.now()
    fecha_formateada = myDate.strftime("%d-%m-%Y")
    
    # Create the HttpResponse headers with PDF
    response = HttpResponse(content_type='applicacion/pdf')
    response['Content-Disposition'] = 'attachment; filename=REPORTE-UNIDADES' + fecha_formateada + '.pdf'
    
    # Create the PDF object. using the BytesIO object as its "file"
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)
    index = 0
    pagina_actual = 0

    for lista in lista_buena:
    
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

        pagina_actual+=1
        c.setFont('Helvetica', 9)
        c.drawString(480,30,'Página ' + str(pagina_actual) +' de ' + str(total_listas))

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

        otro = []
        otro.append([id, unidad, siglas, estatus])
        for unidad in lista:
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
        c.showPage()
        # c.showPage() # save page

    registro_log_admin(user_log,"Genera",None,"Reporte unidades","Administrador")
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

    tipos_exp = TipoExpediente()
    tipos_exp = TipoExpediente.objects.all()
    total_tipos = len(tipos_exp)

    #Ver como dividir la lista en ciertos elementos
    lista_buena = particionar_lista(tipos_exp, 3)

    #Eliminamos listas vacias
    for x in range(len(lista_buena)-1,-1,-1):
        if lista_buena[x]:
            print("")
        else:
            #print("No tiene datos")
            lista_buena.pop(x)

    #Obtenemos el numero de listas de la lista
    total_listas = len(lista_buena)

    myDate = datetime.datetime.now()
    fecha_formateada = myDate.strftime("%d-%m-%Y")
    
    # Create the HttpResponse headers with PDF
    response = HttpResponse(content_type='applicacion/pdf')
    response['Content-Disposition'] = 'attachment; filename=REPORTE-TIPOS-EXPEDIENTES' + fecha_formateada + '.pdf'
    
    # Create the PDF object. using the BytesIO object as its "file"
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)
    index = 0
    pagina_actual = 0

    for lista in lista_buena:
    
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

        pagina_actual+=1
        c.setFont('Helvetica', 9)
        c.drawString(480,30,'Página ' + str(pagina_actual) +' de ' + str(total_listas))

        # Table header
        styles = getSampleStyleSheet()
        styleBH = styles["Normal"]
        styleBH.alignment = TA_CENTER
        styleBH.fontSize = 10

        id = Paragraph('''#''', styleBH)
        tipo_e = Paragraph('''TIPO DE EXPEDIENTE''', styleBH)
        siglas = Paragraph('''SIGLAS''', styleBH)
        unid = Paragraph('''UNIDAD''', styleBH)
        estatus = Paragraph('''ESTATUS''', styleBH)
        
        styles = getSampleStyleSheet()
        styleN = styles["BodyText"]
        styleN.alignment = TA_CENTER
        styleN.fontSize = 7

        width, height = A4
        high = 675

        otro = []
        otro.append([id, tipo_e, siglas, unid, estatus])
        for tipo in lista:
            index += 1
            if tipo.activo:
                activo = "Activo"
            else:
                activo = "Inactivo"
            if tipo.unidad:
                id_unidad = Unidad.objects.get(pk=tipo.unidad.pk)
                siglas_unidad = id_unidad.siglas
            else:
                siglas_unidad = ""
            otro.append([index, tipo.nombre, tipo.siglas, siglas_unidad, activo])
            high = high - 18

        c.setFont('Helvetica-Bold', 12)
        c.drawString(380,700,"Total tipos de expedientes: " + str(total_tipos))

        # Table size
        table = Table(otro, colWidths=[0.5 * inch, 4.2 * inch, 0.9 * inch, 0.9 * inch, 1 * inch])
        table.setStyle(TableStyle([ # Estilos de la tabla
            ('INNERGRID', (0,0), (-1,-1), 0.25, colors.black),
            ('BOX', (0,0), (-1,-1), 0.25, colors.black),
        ]))
        
        # PDF size
        table.wrapOn(c, width, height)
        table.drawOn(c, 30, high)
        c.showPage()

    registro_log_admin(user_log,"Genera",None,"Reporte tipos expedientes","Administrador")
    # save PDF
    c.save()
    
    # get the value of BytesIO buffer and write response
    pdf = buffer.getvalue()
    buffer.close()
    response.write(pdf)
    return response