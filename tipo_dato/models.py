# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class TipoDato(models.Model):

    tipo = models.CharField(u'Tipo', max_length=245)

    def __str__(self):
            return self.tipo