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
# creación de los estatus en los que se puede encontrar un expediente o documento.
# para crear estos modelos en la base de datos utilizar la fixture estatus.json ejecutando
# el comando "python manage.py loaddata estatus.json" en la terminal
#   Estatus:
#       Enviado   - cuando el expediente fue enviado para su aprobación.
#       Guardado  - cuando el expediente aun no a sido terminado y sigue recibiendo modificaciones.
#       Recibido  - cuando el expediente fue abierto por el usuario responsable de su aprobación o 
#                   revisión.
#       Aprobado  - cuando el usuario responsable de la aprobación señala que el documento o 
#                   expediente están correctos.
#       Rechazado - cuando el usuario responsable de la aprobación señala que el documento o 
#                   expediente están incorrectos.
#
#   Ingreso de los estatus anteriores al modelo Estatus
#        
