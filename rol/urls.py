#   from django.conf.urls import url
from django.urls import path, re_path
from . import views
from rol.views import EditarRol, EliminarRol, NuevoRol, VerRol, ListarRoles




urlpatterns = [

    ###############   Unidades   #########################
    path('', views.ListarRoles, name = "Listar_roles"),
    path('nuevo_rol', views.NuevoRol, name = "nuevo_rol"),
    re_path(r'^(?P<pk>[0-9]+)/eliminarRol', EliminarRol, name= "eliminar_rol"),
    re_path(r'^(?P<pk>[0-9]+)/editarRol', EditarRol, name= "editar_rol"),
    re_path(r'^(?P<pk>[0-9]+)/verRol$', VerRol, name= "ver_rol"),


]