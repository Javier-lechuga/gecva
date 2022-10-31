import datetime
from itertools import count
from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, redirect, get_object_or_404
from expediente.models import Expediente

from usuarios.models import PerfilUser
from unidad.models import Unidad
from expediente.models import Expediente_aprobador
from expediente.models import Expediente_deputy
from tipo_expediente.models import TipoExpediente
from expediente.views import registro_log_user

# Create your views here.

def entrar(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            try:
                user_log = PerfilUser.objects.get(pk=request.user.id)
            except ObjectDoesNotExist:
                pass
            if user_log.rol.nombre == "Administrador":
                registro_log_user(user_log,"Entra",None,"Sistema","Administrador")
            else:
                registro_log_user(user_log,"Entra",None,"Sistema","Usuario")
            return redirect('/principal/')
        else:
            """return render(request, 'inicio/login.html')"""
            mensajeerror = 'Usuario y/o contrasena incorrecta'
            return render(request, 'login.html', {'mensajeerror': mensajeerror})
    else:
        return render(request, 'login.html')

# @login_required(redirect_field_name='login')
def principal(request):
    user_log = PerfilUser.objects.get(pk=request.user.pk)
    print(user_log.rol.nombre)
    if user_log.rol.nombre == "Administrador":
        tipos_expedientes = TipoExpediente.objects.all()
        unidades = Unidad.objects.all()
        usuarios = PerfilUser.objects.all()
        return render(request, 'principal.html',{'user_log': user_log, 'tipos_exp': len(tipos_expedientes), 'unidades': len(unidades), 'usuarios':len(usuarios)})
    else:
        expedientes = Expediente.objects.filter(usuario_crea=user_log).exclude(activo=False)
        ids_users = Expediente_aprobador.objects.filter(id_usuario=user_log.pk)
        recibidos = []
        for id_usr in ids_users:
            recibidos.append(id_usr)
        deputy = Expediente_deputy.objects.filter(deputy=user_log)
        return render(request, 'principal.html',{'user_log': user_log, 'expedientes': len(expedientes), 'recibidos': len(recibidos), 'deputy':len(deputy)})
    

# @login_required(redirect_field_name='login')
def ReportesMenu(request):
    user_log = PerfilUser.objects.get(pk=request.user.pk)
    return render(request, 'reportes_admin.html',{'user_log': user_log,})

# @login_required(redirect_field_name='login')
def RepUsuarios(request):
    user_log = PerfilUser.objects.get(pk=request.user.pk)
    usuarios = PerfilUser.objects.all()
    return render(request, 'rep_usuarios.html',{'user_log': user_log, 'usuarios': usuarios, 'mensaje':'Seleccionar usuario'})

# @login_required(redirect_field_name='login')
def RepUnidades(request):
    user_log = PerfilUser.objects.get(pk=request.user.pk)
    unidades = Unidad.objects.all()
    return render(request, 'rep_unidades.html',{'user_log': user_log, 'unidades': unidades, 'mensaje':'Seleccionar unidad'})

# @login_required(redirect_field_name='login')
def Privacidad(request):
    user_log = PerfilUser.objects.get(pk=request.user.pk)
    return render(request, 'privacidad.html',{'user_log': user_log, 'mensaje':'Aviso de privacidad'})

# @login_required(redirect_field_name='login')
def Terminos(request):
    user_log = PerfilUser.objects.get(pk=request.user.pk)
    return render(request, 'terminos.html',{'user_log': user_log, 'mensaje':'Terminos y condiciones'})
