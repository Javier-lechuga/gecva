# .\usuarios\views.py
import datetime
from django.http import HttpResponse
from django.shortcuts import redirect, render

from django.template import RequestContext
from django.shortcuts import render
from django.core.exceptions import ObjectDoesNotExist
from rol.models import Rol
from unidad.models import Unidad
from expediente.models import Expediente, Expediente_aprobador
from usuarios.forms import PerfilUserForm
from usuarios.models import PerfilUser
from expediente.models import Expediente_deputy
from django.contrib.auth.models import User, Group, Permission
from expediente.views import registro_log_admin
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.decorators import permission_required, login_required

# Create your views here.

#@login_required(redirect_field_name='login')
def ListarUsuarios(request):
    user_log = PerfilUser.objects.get(pk=request.user.pk)
    usuarios = PerfilUser.objects.all()
    registro_log_admin(user_log,"Consulta",None,"Usuarios","Administrador")
    return render(request, 'usuarios.html', {'usuarios': usuarios, 'mensaje': 'Usuarios','user_log':user_log})
    #return render(request, 'usuarios.html', {'usuarios': usuarios, 'mensaje': 'Usuarios'})

# @login_required(redirect_field_name='login')
def NuevoUsuario(request):
    user_log = PerfilUser.objects.get(pk=request.user.pk)
    usuarios = PerfilUser.objects.all().exclude(is_active=False).order_by('pk')

    g_administradores, creado_administradores = Group.objects.get_or_create(name='Administradores')
    ct = ContentType.objects.get_for_model(PerfilUser)
    permiso_administradores, creado1 = Permission.objects.get_or_create(codename='accion_administradores',
                                                                 name='puede hacer lo de un usuario administrador',
                                                                 content_type=ct)
    g_administradores.permissions.add(permiso_administradores)

    g_aprobadores, creado_aprobadores = Group.objects.get_or_create(name='Aprobadores')
    ct = ContentType.objects.get_for_model(PerfilUser)
    permiso_aprobadores, creado2 = Permission.objects.get_or_create(codename='accion_aprobadores',
                                                               name='puede hacer lo de un usuario aprobador',
                                                               content_type=ct)
    g_aprobadores.permissions.add(permiso_aprobadores)

    g_usuarios, creado_usuarios = Group.objects.get_or_create(name='Usuarios')
    ct = ContentType.objects.get_for_model(PerfilUser)
    permiso_usuarios, creado2 = Permission.objects.get_or_create(codename='accion_usuarios',
                                                               name='puede hacer lo de un usuario normal',
                                                               content_type=ct)
    g_usuarios.permissions.add(permiso_usuarios)
    unidades = Unidad.objects.all().order_by('pk')
    roles = Rol.objects.all().exclude(nombre='Aprobación').order_by('pk')
    try:
        if request.method == "POST":
            # Instanciando Rol
            rol_dos = Rol()
            rol_dos = Rol.objects.get(pk=request.POST['rol'])
            # Instanciando Jefe_inmediato
            jefe_inmediato_dos = User()
            try:
                jefe_inmediato_dos = User.objects.get(pk=request.POST['jefe_inmediato'])
            except:
                # Si no tiene jefe inmediato se asigna el administrador
                jefe_inmediato_dos = user_log
                #jefe_inmediato_dos = User.objects.get(pk=1)
            # Instanciando Unidad
            unidad_dos = Unidad()
            unidad_dos = Unidad.objects.get(pk=request.POST['unidad_user'])
            usuario = PerfilUser.objects.create(
                username=request.POST.get('username', ''),
                password=request.POST.get('password', ''),
                first_name=request.POST.get('first_name', ''),
                last_name=request.POST.get('last_name', ''),
                amaterno=request.POST.get('amaterno', ''),
                email=request.POST.get('email', ''),
                telefono=request.POST.get('telefono', ''),
                extension=request.POST.get('extension', ''),
                rol=rol_dos,
                jefe_inmediato=jefe_inmediato_dos,
                unidad_user=unidad_dos,
            )
            usuario.set_password(request.POST['password'])
            usuario.save()
            registro_log_admin(user_log,"Crea",usuario,"Usuario","Administrador")
            if usuario.rol.nombre == "Administrador":
                my_group = Group.objects.get(name='Administradores') 
                my_group.user_set.add(usuario)
                registro_log_admin(user_log,"Asigna al grupo Administradores",None,"Usuario","Administrador")
            elif usuario.rol.nombre == "Aprobador":
                my_group = Group.objects.get(name='Aprobadores') 
                my_group.user_set.add(usuario)
                registro_log_admin(user_log,"Asigna al grupo Aprobadores",None,"Usuario","Administrador")
            elif usuario.rol.nombre == "Revisor":
                my_group = Group.objects.get(name='Revisores') 
                my_group.user_set.add(usuario)
                registro_log_admin(user_log,"Asigna al grupo Revisores",None,"Usuario","Administrador")
            else:
                my_group = Group.objects.get(name='Administradores') 
                my_group.user_set.add(usuario)
                registro_log_admin(user_log,"Asigna al grupo Usuarios",None,"Usuario","Administrador")
            return redirect('/usuarios/')
    except:
        form = PerfilUserForm(request.POST)
        error = "El nombre de usuario y/o correo ya existe"
        return render(request, 'nuevo_usuario.html', {'form': form, 'nuevo': 'Nuevo','usuarios': usuarios, 'unidades': unidades, 'roles': roles,'user_log':user_log, 'mensaje': 'Nuevo usuario', 'error':error})
    else:
        form = PerfilUserForm()
    return render(request, 'nuevo_usuario.html', {'form': form, 'nuevo': 'Nuevo','usuarios': usuarios, 'unidades': unidades, 'roles': roles,'user_log':user_log, 'mensaje': 'Nuevo usuario'})
    # return render(request, 'nuevo_usuario.html', {'form': form, 'nuevo': 'Nuevo','usuarios': usuarios, 'unidades': unidades, 'roles': roles})

# @login_required(redirect_field_name='login')
def Perfil(request):
    user_log = PerfilUser.objects.get(pk=request.user.pk)
    usuario = PerfilUser.objects.get(pk=user_log.pk)
    return render(request, 'perfil.html', {'mensaje': 'Perfil','usuario': usuario,'user_log':user_log})

# @login_required(redirect_field_name='login')
def EditarUsuario(request, pk):
    user_log = PerfilUser.objects.get(pk=request.user.pk)
    usuarios = User.objects.all().exclude(is_active=False).order_by('pk')
    unidades = Unidad.objects.all().order_by('pk')
    roles = Rol.objects.all().order_by('pk')
    try:
        usuario = PerfilUser.objects.get(pk=pk)
        if request.method == "POST":
            PerfilUser.objects.filter(pk=pk).update(username=request.POST['username'])
            PerfilUser.objects.filter(pk=pk).update(first_name=request.POST['first_name'])
            PerfilUser.objects.filter(pk=pk).update(last_name=request.POST['last_name'])
            PerfilUser.objects.filter(pk=pk).update(email=request.POST['email'])
            PerfilUser.objects.filter(pk=pk).update(amaterno=request.POST['amaterno'])
            PerfilUser.objects.filter(pk=pk).update(telefono=request.POST['telefono'])
            PerfilUser.objects.filter(pk=pk).update(extension=request.POST['extension'])
            
            #############################################################################
            # Falta la logica para la actualizacion ya que no cambiaba la contraseña
            #PerfilUser.objects.filter(pk=pk).update(password=request.POST['password'])
            #usuario.set_password(request.POST['password'])
            #usuario.save
            #return HttpResponse(usuario)
            #############################################################################

            # Instanciando Usuario Jefe inmediato
            jefe_inmediato_dos = User()
            jefe_inmediato_dos = User.objects.get(pk=request.POST['jefe_inmediato'])
            PerfilUser.objects.filter(pk=pk).update(jefe_inmediato=jefe_inmediato_dos)
            # Instanciando Unidad
            unidad_dos = Unidad()
            unidad_dos = Unidad.objects.get(pk=request.POST['unidad_user'])
            PerfilUser.objects.filter(pk=pk).update(unidad_user=unidad_dos)
            # Instanciando Rol
            rol_dos = Rol()
            rol_dos = Rol.objects.get(pk=request.POST['rol'])
            PerfilUser.objects.filter(pk=pk).update(rol=rol_dos)
            if request.POST['is_active'] == 'on':
                PerfilUser.objects.filter(pk=pk).update(is_active=True)
            else:
                PerfilUser.objects.filter(pk=pk).update(is_active=False)
            registro_log_admin(user_log,"Edita",usuario,"Usuario","Administrador")
            return redirect('/usuarios/')
        else:
            form = PerfilUserForm(instance=usuario)
        return render(request, 'edita_usuario.html', {'form': form, 'mensaje': 'Modificar usuario','usuarios': usuarios, 'unidades': unidades, 'roles': roles, 'usuario': usuario,'user_log':user_log})
    except ObjectDoesNotExist:
        return redirect('/usuarios/')

# @login_required(redirect_field_name='login')
def EliminarUsuario(request, pk):
    try:
        user_log = PerfilUser.objects.get(pk=request.user.pk)
        usuario = PerfilUser.objects.get(pk=pk)
        PerfilUser.objects.filter(pk=pk).update(is_active=False)
        registro_log_admin(user_log,"Elimina",usuario,"Usuario","Administrador")
        return redirect('/usuarios/')
    except ObjectDoesNotExist:
        return redirect('/usuarios/')

# @login_required(redirect_field_name='login')
def VerUsuario(request, pk): # No se usa
    user_log = PerfilUser.objects.get(pk=request.user.pk)
    try:
        usuario = PerfilUser.objects.get(pk=pk)
        registro_log_admin(user_log,"Consulta",usuario,"Usuario","Administrador")
        return render(request, 'usuarios.html', {'usuario': usuario,'user_log':user_log})
    except ObjectDoesNotExist:
        return redirect('principal')


# @login_required(redirect_field_name='login')
def TransferirExp(request): # Para transfereir los expedientes al Deputy
    user_log = PerfilUser.objects.get(pk=request.user.pk)

    try:
        usuarios = PerfilUser.objects.all()
        usuario = PerfilUser.objects.get(pk=request.POST['usuario_origen'])
        usuario_origen = PerfilUser.objects.get(pk=request.POST['usuario_origen'])
        usuario_destino = PerfilUser.objects.get(pk=request.POST['usuario_destino'])
        if usuario_origen.unidad_user == usuario_destino.unidad_user:

            expedientes_origen = Expediente.objects.filter(usuario_crea=usuario_origen)
            # expedientes_asignados = Expediente_aprobador.objects.filter(id_usuario=usuario_origen)
            for expediente in expedientes_origen:
                print(expediente)
                deputy = Expediente_deputy.objects.create(
                    expediente = expediente,
                    usuario_crea = usuario_origen,
                    deputy = usuario_destino,
                )
                deputy.save()
                Expediente.objects.filter(pk=expediente.pk).update(usuario_crea=usuario_destino)
                Expediente_aprobador.objects.filter(pk=expediente.pk).update(id_usuario=usuario_destino)

            PerfilUser.objects.filter(pk=usuario_origen.pk).update(transferido=True)
            PerfilUser.objects.filter(pk=usuario_destino.pk).update(deputy=True)
            registro_log_admin(user_log,"Transfiere expedientes",usuario," Al usuario",usuario_destino.first_name + " " + usuario_destino.last_name + " " + usuario_destino.amaterno)
            return render(request, 'usuarios.html', {'usuario': user_log,'user_log':user_log, 'usuarios': usuarios, 'mensaje':'Usuarios'})
        else:
            alerta = "Solo es posible transferir expedientes entre usuarios de la misma unidad"
            return render(request, 'usuarios.html', {'usuario': user_log,'user_log':user_log, 'usuarios': usuarios, 'alerta': alerta, 'mensaje':'Usuarios'})
    except ObjectDoesNotExist:
        return redirect('principal')



