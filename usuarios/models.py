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
    jefe_inmediato = models.ForeignKey(User, related_name='Jefe_inmediato', blank=False, null=True, on_delete=models.CASCADE)
    unidad_user = models.ForeignKey(Unidad, related_name='Unidad_user', blank=False, null=True, on_delete=models.CASCADE)