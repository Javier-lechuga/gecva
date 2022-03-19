#   from django.conf.urls import url
from django.urls import path, re_path
from . import views
from expediente.views import EditarExpediente, EliminarExpediente, NuevoExpediente, VerExpediente, ListarExpedientes


urlpatterns = [

    ###############   Expedientes   #########################
    path('', views.ListarExpedientes, name = "listar_expedientes"),
    path('nuevo_expediente', views.NuevoExpediente, name = "nuevo_expediente"),
    re_path(r'^(?P<pk>[0-9]+)/eliminarExpediente', EliminarExpediente, name= "eliminar_expediente"),
    re_path(r'^(?P<pk>[0-9]+)/editarExpediente', EditarExpediente, name= "editar_expediente"),
    re_path(r'^(?P<pk>[0-9]+)/verExpediente$', VerExpediente, name= "ver_expediente"),


]