# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Rol(models.Model):

    nombre = models.CharField(u'Nombre', max_length=245)
    descripcion = models.CharField(u'Descripción', max_length=245, null=True)

    def __str__(self):
            return self.nombre

# creación de los roles para los tipos de usuarios que manejara el sistema
# para crear estos modelos en la base de datos utilizar la fixture rol.json ejecutando
# el comando "python manage.py loaddata rol.json" en la terminal
#
#   roles:
#       Administrador   - Usuario que administrara el sistema.
#       Usuario  - Usuario que podra crear expedientes.
#       Aprobación  - Usuario que podra aprobar expedientes y documentos 

#
# Ingreso de los estatus anteriores al modelo Estatus
#  