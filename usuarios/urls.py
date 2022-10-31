#   from django.conf.urls import url
from django.urls import path, re_path
from . import views
from usuarios.views import EliminarUsuario, EditarUsuario, TransferirExp, VerUsuario, ListarUsuarios, NuevoUsuario


urlpatterns = [

    ###############   Usuarios   #########################
    path('', views.ListarUsuarios, name = "listar_usuarios"),
    path('nuevo_usuario', views.NuevoUsuario, name = "nuevo_usuario"),
    re_path(r'^(?P<pk>[0-9]+)/eliminarUsuario', EliminarUsuario, name= "eliminar_usuario"),
    re_path(r'^(?P<pk>[0-9]+)/editarUsuario', EditarUsuario, name= "editar_usuario"),
    re_path(r'^(?P<pk>[0-9]+)/verUsuario$', VerUsuario, name= "ver_usuario"),
    # re_path(r'^(?P<pk>[0-9]+)/transferirExp$', TransferirExp, name= "transferir_exp"),
    path('transferir_exp', views.TransferirExp, name = "transferir_exp"),
    path('perfil', views.Perfil, name = "perfil"),

]