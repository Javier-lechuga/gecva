# .\inicio\urls.py
#   from django.conf.urls import url
from django.urls import path, re_path
from . import views
from django.contrib.auth.views import logout_then_login
from inicio.views import Privacidad, RepUsuarios, Terminos, entrar, principal, ReportesMenu, RepUnidades
from expediente.views import ReporteGeneral


urlpatterns = [

    ###############   Login   #########################
    path('', views.entrar, name="login_sistema"),
    path('cerrarSesion/', logout_then_login, name="logout_sistema"),
    path('principal/', principal, name = "principal"),
    path('reportes_menu/', ReportesMenu, name = "reportes_nemu"),
    path('rep_usuarios/', RepUsuarios, name = "rep_usuarios"),
    path('rep_unidades/', RepUnidades, name = "rep_unidades"),
    path('rep_general/', ReporteGeneral, name = "rep_general"),
    path('privacidad/', Privacidad, name = "privacidad"),
    path('terminos/', Terminos, name = "terminos"),
    
]