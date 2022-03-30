# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from email.policy import default
from django.db import models
from django.contrib.auth.models import User
from django.forms import IntegerField
from estatus.models import Estatus
from expediente.models import Expediente
from tipo_dato.models import TipoDato
from tipo_expediente.models import TipoExpediente

# Create your models here.
class Metadato(models.Model):

    nombre = models.CharField(u'Nombre', max_length=245)
    descripcion = models.CharField(u'Descripción', max_length=245, null=True)
    valor = models.CharField(u'Valor', max_length=245)
    version = models.CharField(u'Versión', max_length=245, null=True)
    motivo_rechazo = models.CharField(u'Motivo_rechazo', max_length=245, null=True)
    tipo_dato = models.ForeignKey(TipoDato, related_name='Tipo_dato', blank=True, null=True, on_delete=models.CASCADE)
    estatus = models.ForeignKey(Estatus, related_name='Estatus_uno', blank=False, null=True, on_delete=models.CASCADE)
    tipo_expediente = models.ForeignKey(TipoExpediente, related_name='Tipo_exp', blank=True, null=True, on_delete=models.CASCADE)
    expediente = models.ForeignKey(Expediente, related_name='Tipo_exp', blank=True, null=True, on_delete=models.CASCADE)
    obligatorio = models.BooleanField(verbose_name=('Obligatorio'), default=False)
    base = models.IntegerField(default=0)

    def __str__(self):
            return self.nombre