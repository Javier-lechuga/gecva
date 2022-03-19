#   from django.conf.urls import url
from django.urls import path, re_path
from . import views
from estatus.views import EditarEstatus, EliminarEstatus, NuevoEstatus, VerEstatus, ListarEstatus




urlpatterns = [

    ###############   Estatus   #########################
    path('', views.ListarEstatus, name = "Listar_estatus"),
    path('nuevo_estatus', views.NuevoEstatus, name = "nuevo_estatus"),
    re_path(r'^(?P<pk>[0-9]+)/eliminarEstatus', EliminarEstatus, name= "eliminar_estatus"),
    re_path(r'^(?P<pk>[0-9]+)/editarEstatus', EditarEstatus, name= "editar_estatus"),
    re_path(r'^(?P<pk>[0-9]+)/verEstatus$', VerEstatus, name= "ver_estatus"),


]