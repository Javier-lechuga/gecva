# .\metadato\urls.py
#   from django.conf.urls import url
from django.urls import path, re_path
from . import views
from metadato.views import EditarMetadato, EliminaMetadato, NuevoMetadato, VerMetadato, ListarMetadatos, MetadatoTipoExp, ListarMetadatosTipoEXp




urlpatterns = [

    ###############   Metadatos   #########################
    path('', views.ListarMetadatos, name = "listar_metadatos"), # No deberia ser accesible por el usuario, no se utiliza en esta versión
    path('nuevo_metadato', views.NuevoMetadato, name = "nuevo_metadato"), # No deberia ser accesible por el usuario
    re_path(r'^(?P<pk>[0-9]+)/listarMetadatosTipoExp', ListarMetadatosTipoEXp, name= "listar_metadatos_tipo_exp"),
    re_path(r'^(?P<pk>[0-9]+)/metadatoTipoExp', MetadatoTipoExp, name= "metadato_tipo_exp"),
    re_path(r'^(?P<pk>[0-9]+)/eliminarMetadato', EliminaMetadato, name= "eliminar_metadato"),
    re_path(r'^(?P<pk>[0-9]+)/editarMetadato', EditarMetadato, name= "editar_metadato"),
    re_path(r'^(?P<pk>[0-9]+)/verMetadato$', VerMetadato, name= "ver_metadato"), # No debe ser accesible por el usuario


]