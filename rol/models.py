# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Rol(models.Model):

    nombre = models.CharField(u'Nombre', max_length=245)
    descripcion = models.CharField(u'Descripción', max_length=245, null=True)

    def __str__(self):
            return self.nombre