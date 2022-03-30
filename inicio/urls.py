#   from django.conf.urls import url
from django.urls import path, re_path
from . import views
from django.contrib.auth.views import logout_then_login
from inicio.views import entrar, principal


urlpatterns = [

    ###############   Login   #########################
    path('', views.entrar, name="login_sistema"),
    path('cerrarSesion/', logout_then_login, name="logout_sistema"),
    path('principal/', principal, name = "principal"),

]