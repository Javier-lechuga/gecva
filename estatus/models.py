# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Estatus(models.Model):

    nombre = models.CharField(u'Nombre', max_length=245)
    es_doc = models.BooleanField(verbose_name=('Documento'), default=False)

    def __str__(self):
            return self.nombre