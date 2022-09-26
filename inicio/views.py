import datetime
from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, redirect, get_object_or_404

from usuarios.models import PerfilUser
from unidad.models import Unidad
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
    return render(request, 'principal.html',{'user_log': user_log,})

# @login_required(redirect_field_name='login')
def ReportesMenu(request):
    user_log = PerfilUser.objects.get(pk=request.user.pk)
    return render(request, 'reportes_admin.html',{'user_log': user_log,})

# @login_required(redirect_field_name='login')
def RepUsuarios(request):
    user_log = PerfilUser.objects.get(pk=request.user.pk)
    usuarios = PerfilUser.objects.all()
    return render(request, 'rep_usuarios.html',{'user_log': user_log, 'usuarios': usuarios})

# @login_required(redirect_field_name='login')
def RepUnidades(request):
    user_log = PerfilUser.objects.get(pk=request.user.pk)
    unidades = Unidad.objects.all()
    return render(request, 'rep_unidades.html',{'user_log': user_log, 'unidades': unidades})
