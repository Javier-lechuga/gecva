# .\tipo_dato\models.py
# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class TipoDato(models.Model):

    tipo = models.CharField(u'Tipo', max_length=245)

    def __str__(self):
            return self.tipo

# creación de los tipos de datos que puede ser un metadato
# para crear estos modelos en la base de datos utilizar la fixture tipo_datos.json ejecutando
# el comando "python manage.py loaddata tipo_datos.json" en la terminal
#   Tipo de dato:
#       Archivo   - 
#       Numérico  - 
#       Fecha     - 
#       Texto     - 
#
#
#     Ingreso de los tipos de datos anteriores al modelo TipoDato
#    