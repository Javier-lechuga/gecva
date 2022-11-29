# .\estatus\models.py

# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User

# Create your models here.


"""
Modelo estatus, este modelo se utiliza para controlar el estado que pueden tener los flujos(expedientes),
los estatus posibles son los siguientes:
    1.- Creado ->para cuando el flujo fue creado por el usuario, en esta etapa el flujo 
                 puede ser modificado, eliminado o asignado para aprobación.
                 Al eliminar el expediente en el sistema, este se conserva en la base de datos
                 y se le cambia el campo de activo de 1 a 0.
                 # Nota hay que revisar el proceso de la eliminación
    2.- Revisión -> el usuario creador paso el flujo a aprobación(revisión), en esta etapa el flujo puede ser 
                    aprobado(Revisado). en esta etapa el flujo no puede ser modificado por el usuario creador
                    # Nota hai que acomodar para eliminar confuciones, en el template dice aprobar
                    pero deberia decir revisar.
    3.- 
"""

class Estatus(models.Model):

    nombre = models.CharField(u'Nombre', max_length=245)
    es_doc = models.BooleanField(verbose_name=('Documento'), default=False) # No se esta utilizando por el momento

    def __str__(self):
            return self.nombre
     
