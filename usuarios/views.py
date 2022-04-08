import datetime
from django.http import HttpResponse
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
    usuarios = User.objects.all().exclude(is_active=False).order_by('pk')
    unidades = Unidad.objects.all().order_by('pk')
    roles = Rol.objects.all().order_by('pk')
    if request.method == "POST":
        # return HttpResponse(request.POST.items())
        # form = PerfilUserForm(request.POST)
        # usuario = None
        #if form.is_valid():
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
        # usuario.set_password(form.cleaned_data['password'])
        usuario.save()
        return redirect('/usuarios/')
    else:
        form = PerfilUserForm()
    return render(request, 'nuevo_usuario.html', {'form': form, 'nuevo': 'Nuevo','usuarios': usuarios, 'unidades': unidades, 'roles': roles})

# @login_required(redirect_field_name='login')
def EditarUsuario(request, pk):
    usuarios = User.objects.all().exclude(is_active=False).order_by('pk')
    unidades = Unidad.objects.all().order_by('pk')
    roles = Rol.objects.all().order_by('pk')
    try:
        usuario = PerfilUser.objects.get(pk=pk)
        if request.method == "POST":
            # return HttpResponse(request.POST.items())
            PerfilUser.objects.filter(pk=pk).update(username=request.POST['username'])
            PerfilUser.objects.filter(pk=pk).update(first_name=request.POST['first_name'])
            PerfilUser.objects.filter(pk=pk).update(last_name=request.POST['last_name'])
            PerfilUser.objects.filter(pk=pk).update(email=request.POST['email'])
            PerfilUser.objects.filter(pk=pk).update(amaterno=request.POST['amaterno'])
            PerfilUser.objects.filter(pk=pk).update(telefono=request.POST['telefono'])
            PerfilUser.objects.filter(pk=pk).update(extension=request.POST['extension'])
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
            # form = PerfilUserForm(request.POST, instance=usuario)
            # if form.is_valid():
            #     usuario = form.save()
            #     usuario.set_password(form.cleaned_data['password'])
            #     usuario.save()
            #     return redirect('/usuarios/')
            return redirect('/usuarios/')
        else:
            form = PerfilUserForm(instance=usuario)
        return render(request, 'edita_usuario.html', {'form': form, 'mensaje': 'Modificar usuario','usuarios': usuarios, 'unidades': unidades, 'roles': roles, 'usuario': usuario})
    except ObjectDoesNotExist:
        return redirect('/usuarios/')

# @login_required(redirect_field_name='login')
# def EliminarUsuario(request, pk):
#     try:
#         usuario = PerfilUser.objects.get(pk=pk)
#         usuario.delete()
#         return redirect('/usuarios/')
#     except ObjectDoesNotExist:
#         return redirect('/usuarios/')

# @login_required(redirect_field_name='login')
def EliminarUsuario(request, pk):
    try:
        usuario = PerfilUser.objects.get(pk=pk)
        PerfilUser.objects.filter(pk=pk).update(is_active=False)
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