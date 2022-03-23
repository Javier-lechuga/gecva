import datetime
from django.shortcuts import redirect, render

from django.template import RequestContext
from django.shortcuts import render
from django.core.exceptions import ObjectDoesNotExist
from rol.models import Rol
from unidad.models import Unidad
from usuarios.forms import PerfilUserForm
from usuarios.models import PerfilUser
from django.contrib.auth.models import User

# Create your views here.

# @login_required(redirect_field_name='login')
def ListarUsuarios(request):
    usuarios = PerfilUser.objects.all()
    return render(request, 'usuarios.html', {'usuarios': usuarios, 'mensaje': 'Usuarios'})

# @login_required(redirect_field_name='login')
def NuevoUsuario(request):
    if request.method == "POST":
        form = PerfilUserForm(request.POST)
        usuario = None
        if form.is_valid():
            # user = get_user(request)
            # user = request.user
            # Instanciando Rol
            rol_dos = Rol()
            rol_dos = Rol.objects.get(pk=request.POST['rol'])
            # Instanciando Jefe_inmediato
            jefe_inmediato_dos = User()
            jefe_inmediato_dos = User.objects.get(pk=request.POST['jefe_inmediato'])
            # Instanciando Unidad
            unidad_dos = Unidad()
            unidad_dos = Unidad.objects.get(pk=request.POST['unidad_user'])
            # Asignando el valor de Vigente
            if request.POST.get('vigente','') == 'on':
                vigente_dos = True
            else:
                vigente_dos = False
            usuario = PerfilUser.objects.create(
                username=request.POST.get('username', ''),
                password=request.POST.get('passwor', ''),
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
            usuario.set_password(form.cleaned_data['password'])
            usuario.save()
            return redirect('/usuarios/')
    else:
        form = PerfilUserForm()
    return render(request, 'nuevo_usuario.html', {'form': form, 'nuevo': 'Nuevo'})

# @login_required(redirect_field_name='login')
def EditarUsuario(request, pk):
    try:
        usuario = PerfilUser.objects.get(pk=pk)
        if request.method == "POST":
            form = PerfilUserForm(request.POST, instance=usuario)
            if form.is_valid():
                usuario = form.save()
                usuario.set_password(form.cleaned_data['password'])
                usuario.save()
                return redirect('/usuarios/')
        else:
            form = PerfilUserForm(instance=usuario)
        return render(request, 'edita_usuario.html', {'form': form, 'mensaje': 'Modificar usuario'})
    except ObjectDoesNotExist:
        return redirect('/usuarios/')

# @login_required(redirect_field_name='login')
def EliminarUsuario(request, pk):
    try:
        usuario = PerfilUser.objects.get(pk=pk)
        usuario.delete()
        return redirect('/usuarios/')
    except ObjectDoesNotExist:
        return redirect('/usuarios/')

# @login_required(redirect_field_name='login')
def VerUsuario(request, pk):
    try:
        usuario = PerfilUser.objects.get(pk=pk)
        return render(request, 'usuarios.html', {'usuario': usuario})
    except ObjectDoesNotExist:
        return redirect('principal')