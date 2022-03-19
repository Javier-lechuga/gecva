# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User
from estatus.models import Estatus
from tipo_dato.models import TipoDato

# Create your models here.
class Metadato(models.Model):

    nombre = models.CharField(u'Nombre', max_length=245)
    descripcion = models.CharField(u'Descripción', max_length=245, null=True)
    valor = models.CharField(u'Valor', max_length=245)
    version = models.CharField(u'Versión', max_length=245, null=True)
    motivo_rechazo = models.CharField(u'Motivo_rechazo', max_length=245, null=True)
    tipo_dato = models.ForeignKey(TipoDato, related_name='Tipo_dato', blank=True, null=True, on_delete=models.CASCADE)
    estatus = models.ForeignKey(Estatus, related_name='Estatus_uno', blank=False, null=True, on_delete=models.CASCADE)
    obligatorio = models.BooleanField(verbose_name=('Obligatorio'), default=False)

    def __str__(self):
            return self.nombre