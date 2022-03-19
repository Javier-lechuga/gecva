from django.contrib import admin

from metadato.models import Metadato
from rol.models import Rol
from tipo_dato.models import TipoDato
from tipo_expediente.models import TipoExpediente
from unidad.models import Unidad
from estatus.models import Estatus
from expediente.models import Expediente

# Register your models here.

# Para mostrar los campos deseados y agregar búsquedas también por campos
class Administracion(admin.ModelAdmin):
    list_display=("identificador","nombre","descripcion")
    search_fields=("identificador","nombre","descripcion")

# Agregando filtros
class FiltrosBuenos(admin.ModelAdmin):
    list_filter=("identificador",)

# Filtros avanzados
class FiltrosAvanzados(admin.ModelAdmin):
    list_display=("nombre","fecha")
    list_filter=("fecha",)
    date_hierarchy="fecha"

admin.site.register(Metadato)
admin.site.register(Rol)
admin.site.register(TipoDato)
admin.site.register(TipoExpediente)
admin.site.register(Unidad)
admin.site.register(Estatus)
admin.site.register(Expediente, Administracion)