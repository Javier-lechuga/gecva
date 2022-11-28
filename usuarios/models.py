# .\usuarios\models.py
from django.db import models

from django.contrib.auth.models import User

from rol.models import Rol
from unidad.models import Unidad

# Create your models here.


class PerfilUser(User):
    amaterno=models.CharField(u'Materno', max_length=25)
    telefono=models.CharField(u'Teléfono', max_length=25)
    extension=models.CharField(u'Extensión', max_length=25)
    rol = models.ForeignKey(Rol, related_name='Rol', blank=False, null=True, on_delete=models.CASCADE)
    jefe_inmediato = models.ForeignKey(User, related_name='Jefe_inmediato', blank=True, null=True, on_delete=models.CASCADE)
    unidad_user = models.ForeignKey(Unidad, related_name='Unidad_user', blank=False, null=True, on_delete=models.CASCADE)
    transferido = models.BooleanField(verbose_name=('Transferido'), default=False)
    deputy = models.BooleanField(verbose_name=('Deputy'), default=False)
    es_deputy = models.BooleanField(verbose_name=('Es_deputy'), default=False)
    usuario_deputy = models.ForeignKey(User, related_name='user_deputy', blank=True, null=True, on_delete=models.CASCADE)