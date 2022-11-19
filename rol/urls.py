#   from django.conf.urls import url
from django.urls import path, re_path
from . import views
from rol.views import EditarRol, EliminarRol, NuevoRol, VerRol, ListarRoles


# Este modulo solo requiere tener activado el modelo, se creo el CRUD para cuestiones de pruebas en las primeras etapas
# Por lo que no es necesario para el funcionamiento del sistema las siguientes url y sus correspondientes vistas
# Todas las vistas de este modulo no deberia de ser accesibles por el usuario, ya que se implementan por "Fixtures"

urlpatterns = [

    ###############   Unidades   #########################
    path('', views.ListarRoles, name = "Listar_roles"), 
    path('nuevo_rol', views.NuevoRol, name = "nuevo_rol"),
    re_path(r'^(?P<pk>[0-9]+)/eliminarRol', EliminarRol, name= "eliminar_rol"),
    re_path(r'^(?P<pk>[0-9]+)/editarRol', EditarRol, name= "editar_rol"),
    re_path(r'^(?P<pk>[0-9]+)/verRol$', VerRol, name= "ver_rol"),


]