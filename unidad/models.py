# .\unidad\models.py
# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from enum import unique
from re import T
from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Unidad(models.Model):

    nombre = models.CharField(u'Nombre', max_length=245)
    siglas = models.CharField(u'Siglas', max_length=3, default='')
    descripcion = models.CharField(u'Descripción', max_length=245, null=True)
    jefe_unidad = models.ForeignKey(User, related_name='Jefe_unidad', blank=True, null=True, on_delete=models.CASCADE)
    activo = models.BooleanField(verbose_name=('Activo'), default=True)

    class Meta:
        unique_together = ('nombre', 'siglas',)

    def __str__(self):
            return self.nombre