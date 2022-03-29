#   from django.conf.urls import url
from django.urls import path, re_path
from . import views
from expediente.views import EditarExpediente, EliminarExpediente, NuevoExpediente, SeleccionaTipoExp, VerExpediente, ListarExpedientes, SeleccionaTipoExp, MuestraCamposExp, ListaMetadatosExp, GuardaMetadatosExp, ListarMisExpedientes, DetalleExpediente, ModificaExpCompleto

#para cargar archivos
from django.conf import settings
from django.conf.urls.static import static
#

urlpatterns = [
    ###############   Expedientes   #########################
    path('', views.ListarExpedientes, name = "listar_expedientes"),
    path('selecciona_expediente', views.SeleccionaTipoExp, name = "selecciona_expediente"),
    path('nuevo_expediente', views.NuevoExpediente, name = "nuevo_expediente"),
    path('muestra_campos_exp', views.MuestraCamposExp, name = "muestra_campos_exp"),
    path('lista_metadatos_exp', views.ListaMetadatosExp, name = "lista_metadatos_exp"),
    path('guarda_metadatos_exp', views.GuardaMetadatosExp, name = "guarda_metadatos_exp"),
    path('mis_expedientes', views.ListarMisExpedientes, name = "mis_expedientes"),
    path('modifica_exp_completo', views.ModificaExpCompleto, name = "modifica_exp_completo"),
    # re_path(r'^(?P<pk>[0-9]+)/guardaMetadatosExp', GuardaMetadatosExp, name= "guarda_metadatos_exp"),
    re_path(r'^(?P<pk>[0-9]+)/detalleExpediente', DetalleExpediente, name= "detalle_expediente"),
    re_path(r'^(?P<pk>[0-9]+)/eliminarExpediente', EliminarExpediente, name= "eliminar_expediente"),
    re_path(r'^(?P<pk>[0-9]+)/editarExpediente', EditarExpediente, name= "editar_expediente"),
    re_path(r'^(?P<pk>[0-9]+)/verExpediente$', VerExpediente, name= "ver_expediente"),
]

# 
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, documen_root=settings.MEDIA_ROOT)