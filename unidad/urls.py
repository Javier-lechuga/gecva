#   from django.conf.urls import url
from django.urls import path, re_path
from . import views
from unidad.views import EditarUnidad, EliminarUnidad, NuevaUnidad, VerUnidad, ListarUnidades




urlpatterns = [

    ###############   Unidades   #########################
    path('', views.ListarUnidades, name = "Listar_unidades"),
    path('nueva_unidad', views.NuevaUnidad, name = "nueva_unidad"),
    #re_path(r'^$', ListarUnidades, name ="listar_unidades"),
    #re_path(r'^nuevaUnidad/$', NuevaUnidad, name = "nueva_unidad"),
    re_path(r'^(?P<pk>[0-9]+)/eliminarUnidad', EliminarUnidad, name= "eliminar_unidad"),
    re_path(r'^(?P<pk>[0-9]+)/editarUnidad', EditarUnidad, name= "editar_unidad"),
    re_path(r'^(?P<pk>[0-9]+)/verPlantilla$', VerUnidad, name= "ver_unidad"),


]