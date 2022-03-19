#   from django.conf.urls import url
from django.urls import path, re_path
from . import views
from tipo_expediente.views import EditarTipoExp, EliminarTipoExp, NuevoTipoExp, VerTipoExp, ListarTiposExpedientes




urlpatterns = [

    ###############   Tipos de expedientes   #########################
    path('', views.ListarTiposExpedientes, name = "listar_tipos_exp"),
    path('nuevo_tipo_exp', views.NuevoTipoExp, name = "nuevo_tipo_exp"),
    re_path(r'^(?P<pk>[0-9]+)/eliminarTipoExp', EliminarTipoExp, name= "eliminar_tipo_exp"),
    re_path(r'^(?P<pk>[0-9]+)/editarTipoExp', EditarTipoExp, name= "editar_tipo_exp"),
    re_path(r'^(?P<pk>[0-9]+)/verTipoExp$', VerTipoExp, name= "ver_tipo_exp"),


]