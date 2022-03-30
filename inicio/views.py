from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, redirect, get_object_or_404

# Create your views here.

def entrar(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            try:
                usuario = User.objects.get(pk=request.user.id)
            except ObjectDoesNotExist:
                pass
            return redirect('/principal/')
        else:
            """return render(request, 'inicio/login.html')"""
            mensajeerror = 'Usuario y/o contrasena incorrecta'
            return render(request, 'login.html', {'mensajeerror': mensajeerror})
    else:
        return render(request, 'login.html')

# @login_required(redirect_field_name='login')
def principal(request):
    usuario = User.objects.get(pk=request.user.pk)
    return render(request, 'principal.html',{'usuario': usuario,})