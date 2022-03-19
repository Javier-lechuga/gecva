from django.shortcuts import render

from django.template import RequestContext
from django.shortcuts import render_to_response
from usuarios.forms import UsuarioForm

# Create your views here.

def add_user(request):
    if request.method=="POST":
        perfil_form=UsuarioForm(request.POST)

        if perfil_form.is_valid:
            try:
                perfil_form.save()

                return render_to_response(
                    "index.html",
                    {
                        'mensaje':'Se guardo ok!'
                    },
                        context_instance=RequestContext(request)
                )
            except:
                return render_to_response(
                    "index.html",locals(),
                    context_instance=RequestContext(request)
                )
        
    else :
        perfil_form=UsuarioForm()

    return render_to_response(
        "index.html",
        locals(),
        contex_instance=RequestContext(request)
    )