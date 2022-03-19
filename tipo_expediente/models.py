# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class TipoExpediente(models.Model):

    nombre = models.CharField(u'Nombre', max_length=245)
    activo = models.BooleanField(verbose_name=('Activo'), default=True)

    def __str__(self):
            return self.nombre