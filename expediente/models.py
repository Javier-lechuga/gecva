# .\expediente\models.py

# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User
from tipo_expediente.models import TipoExpediente
from estatus.models import Estatus
from unidad.models import Unidad
from usuarios.models import PerfilUser

# Create your models here.
class Expediente(models.Model):

    identificador = models.CharField(u'Identificador', max_length=30, unique=True)
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
    usuario_crea = models.ForeignKey(PerfilUser, blank=True, null=True, on_delete=models.CASCADE)
    activo = models.BooleanField(verbose_name=('Activo'), default=True)
    usuario_anterior = models.ForeignKey(PerfilUser, related_name='Usuario_anterior', blank=True, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.nombre

class Expediente_aprobador(models.Model):

    id_expediente = models.ForeignKey(Expediente, related_name='Expediente', blank=True, null=True, on_delete=models.CASCADE)
    id_usuario = models.ForeignKey(PerfilUser, related_name='Usuario_realiza', blank=True, null=True, on_delete=models.CASCADE)
    id_estatus = models.ForeignKey(Estatus, related_name='id_Estatus', blank=True, null=True, on_delete=models.CASCADE)
    motivo_rechazo = models.CharField(u'motivo_rechazo', max_length=245, null=True)
    activo = models.BooleanField(verbose_name=('Activo'), default=True)

    def __str__(self):
        return self.id_expediente

class Registra_actividad(models.Model):

    fecha = models.CharField(u'Hora', max_length=245, null=True)
    hora = models.CharField(u'Hora', max_length=245, null=True)
    rol = models.CharField(u'Rol', max_length=245, null=True)
    usuario = models.ForeignKey(PerfilUser, related_name='Usuario', blank=True, null=True, on_delete=models.CASCADE)
    actividad = models.CharField(u'Actividad', max_length=245, null=False)
    detalle_objeto = models.CharField(u'Detalle_objeto', max_length=245, null=True)
    objeto = models.CharField(u'Destino', max_length=245, null=False)

    def __str__(self):
        return self.actividad

class Expediente_deputy(models.Model):

    expediente = models.ForeignKey(Expediente, related_name='Exp', blank=True, null=True, on_delete=models.CASCADE)
    usuario_crea = models.ForeignKey(PerfilUser, related_name='Usuario_crea', blank=True, null=True, on_delete=models.CASCADE)
    deputy = models.ForeignKey(PerfilUser, related_name='Deputy', blank=True, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.expediente

class Expediente_transferido(models.Model):

    expediente = models.ForeignKey(Expediente, related_name='Expdiente_en_cuestion', blank=True, null=True, on_delete=models.CASCADE)
    usuario_crea = models.ForeignKey(PerfilUser, related_name='Usuario_creador', blank=True, null=True, on_delete=models.CASCADE)
    usuario_asignado = models.ForeignKey(PerfilUser, related_name='Usuario_asignado', blank=True, null=True, on_delete=models.CASCADE)
    activo = models.BooleanField(verbose_name=('Activo'), default=True)

    def __str__(self):
        return self.expediente