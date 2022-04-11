# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Unidad(models.Model):

    nombre = models.CharField(u'Nombre', max_length=245)
    descripcion = models.CharField(u'Descripción', max_length=245, null=True)
    jefe_unidad = models.ForeignKey(User, related_name='Jefe_unidad', blank=True, null=True, on_delete=models.CASCADE)
    activo = models.BooleanField(verbose_name=('Activo'), default=True)

    def __str__(self):
            return self.nombre


# creación de los roles para los tipos de usuarios que manejara el sistema
# para crear estos modelos en la base de datos utilizar la fixture unidad.json ejecutando
# el comando "python manage.py loaddata unidad.json" en la terminal
#
#   roles:
#       nombre       - Nobre de la unidad
#       descripcion  - primer usuario necesario para eliminar la redundancia ciclica 
#                      Unidad -> Usuario -> Unidad 
#       jefe_unidad  - Usuario que podra aprobar expedientes y documentos
#       activo 
# Ingreso de los estatus anteriores al modelo Estatus
#  