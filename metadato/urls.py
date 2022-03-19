#   from django.conf.urls import url
from django.urls import path, re_path
from . import views
from metadato.views import EditarMetadato, EliminaMetadato, NuevoMetadato, VerMetadato, ListarMetadatos




urlpatterns = [

    ###############   Metadatos   #########################
    path('', views.ListarMetadatos, name = "listar_metadatos"),
    path('nuevo_metadato', views.NuevoMetadato, name = "nuevo_metadato"),
    re_path(r'^(?P<pk>[0-9]+)/eliminarMetadato', EliminaMetadato, name= "eliminar_metadato"),
    re_path(r'^(?P<pk>[0-9]+)/editarMetadato', EditarMetadato, name= "editar_metadato"),
    re_path(r'^(?P<pk>[0-9]+)/verMetadato$', VerMetadato, name= "ver_metadato"),


]