# .\tipo_expediente\models.py
# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User

from unidad.models import Unidad

# Create your models here.
class TipoExpediente(models.Model):

    nombre = models.CharField(u'Nombre', max_length=245)
    unidad = models.ForeignKey(Unidad, related_name='Unidad_tipo_exp', blank=True, null=True, on_delete=models.CASCADE)
    siglas = models.CharField(u'Siglas', max_length=3, default='', unique=True)
    activo = models.BooleanField(verbose_name=('Activo'), default=True)

    class Meta:
        unique_together = ('nombre', 'unidad',)

    def __str__(self):
            return self.nombre