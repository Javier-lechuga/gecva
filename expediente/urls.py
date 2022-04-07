#   from django.conf.urls import url
from django.urls import path, re_path
from . import views
from expediente.views import AprobarExp, BuscaMetadatosExp, EditarExpediente, EliminarExpediente,NuevoExpediente, SeleccionaTipoExp, VerExpediente
from expediente.views import ListarExpedientes, SeleccionaTipoExp, MuestraCamposExp, ListaMetadatosExp, GuardaMetadatosExp, ExpRecibidos
from expediente.views import ListarMisExpedientes, DetalleExpediente, ModificaExpCompleto, NuevoExpCompleto, BuscaMetadatosExp, AprobarExp, ExpAprobado

#para cargar archivos
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    ###############   Expedientes   #########################
    path('', views.ListarExpedientes, name = "listar_expedientes"),
    path('selecciona_expediente', views.SeleccionaTipoExp, name = "selecciona_expediente"),
    path('nuevo_expediente', views.NuevoExpediente, name = "nuevo_expediente"),
    path('nuevo_exp_completo', views.NuevoExpCompleto, name = "nuevo_exp_completo"),
    path('muestra_campos_exp', views.MuestraCamposExp, name = "muestra_campos_exp"),
    path('lista_metadatos_exp', views.ListaMetadatosExp, name = "lista_metadatos_exp"),
    path('guarda_metadatos_exp', views.GuardaMetadatosExp, name = "guarda_metadatos_exp"),
    path('mis_expedientes', views.ListarMisExpedientes, name = "mis_expedientes"),
    path('modifica_exp_completo', views.ModificaExpCompleto, name = "modifica_exp_completo"),
    path('busca_metadatos_exp', views.BuscaMetadatosExp, name = "busca_metadatos_exp"),
    path('ver_expediente', views.VerExpediente, name = "ver_expediente"),
    path('asigna_expediente', views.AsignaExpediente, name = "asigna_expediente"),
    path('exp_recibidos', views.ExpRecibidos, name = "exp_recibidos"),
    # re_path(r'^(?P<pk>[0-9]+)/guardaMetadatosExp', GuardaMetadatosExp, name= "guarda_metadatos_exp"),
    re_path(r'^(?P<pk>[0-9]+)/detalleExpediente', DetalleExpediente, name= "detalle_expediente"),
    # re_path(r'^(?P<pk>[0-9]+)/verExpediente', DetalleExpediente, name= "ver_expediente"),
    re_path(r'^(?P<pk>[0-9]+)/eliminarExpediente', EliminarExpediente, name= "eliminar_expediente"),
    re_path(r'^(?P<pk>[0-9]+)/editarExpediente', EditarExpediente, name= "editar_expediente"),
    re_path(r'^(?P<pk>[0-9]+)/verExpediente$', VerExpediente, name= "ver_expediente"),
    re_path(r'^(?P<pk>[0-9]+)/aprobarExp$', AprobarExp, name= "aprobar_exp"),
    path('rechazar_exp', views.RechazarExp, name = "rechazar_exp"),
    path('expediente_aprob', views.ExpAprobado, name = "expediente_aprob"),
]

# 
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, documen_root=settings.MEDIA_ROOT)