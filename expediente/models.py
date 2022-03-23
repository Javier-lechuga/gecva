# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User
from tipo_expediente.models import TipoExpediente
from estatus.models import Estatus
from unidad.models import Unidad

# Create your models here.
class Expediente(models.Model):

    identificador = models.CharField(u'Identificador', max_length=30)
    nombre = models.CharField(u'Nombre', max_length=245)
    descripcion = models.CharField(u'Descripción', max_length=245, null=True)
    asunto = models.CharField(u'Asunto', max_length=245)
    fecha_creacion = models.DateTimeField(u'Creación',null=True)
    fecha_cierre = models.DateTimeField(u'Cierre',null=True)
    ubicacion = models.CharField(u'Ubicación', max_length=245)
    motivo_rechazo = models.CharField(u'motivo_rechazo', max_length=245)
    tipo_expediente = models.ForeignKey(TipoExpediente, related_name='Tipo_expediente', blank=False, null=True, on_delete=models.CASCADE)
    estatus = models.ForeignKey(Estatus, related_name='Estatus', blank=False, null=True, on_delete=models.CASCADE)
    unidad = models.ForeignKey(Unidad, related_name='Unidad', blank=False, null=True, on_delete=models.CASCADE)
    usuario_crea = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE)
    activo = models.BooleanField(verbose_name=('Activo'), default=True)

def __unicode__(self):
        return self.nombre