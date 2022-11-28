# .\tipo_dato\urls.py
#   from django.conf.urls import url
from django.urls import path, re_path
from . import views
from tipo_dato.views import EditarTipoDato, EliminarTipoDato, NuevoTipoDato, VerTipoDato, ListarTiposDatos

# Este modulo solo requiere tener activado el modelo, se creo el CRUD para cuestiones de pruebas en las primeras etapas
# Por lo que no es necesario para el funcionamiento del sistema las siguientes url y sus correspondientes vistas
# Todas las vistas de este modulo no deberia de ser accesibles por el usuario, ya que se implementan por "Fixtures"

urlpatterns = [

    ###############   Tipos de datos   #########################
    path('', views.ListarTiposDatos, name = "listar_tipos_datos"),
    path('nuevo_tipo_dato', views.NuevoTipoDato, name = "nuevo_tipo_dato"),
    re_path(r'^(?P<pk>[0-9]+)/eliminarTipoDato', EliminarTipoDato, name= "eliminar_tipo_dato"),
    re_path(r'^(?P<pk>[0-9]+)/editarTipoDato', EditarTipoDato, name= "editar_tipo_dato"),
    re_path(r'^(?P<pk>[0-9]+)/verTipoDato$', VerTipoDato, name= "ver_tipo_dato"),


]