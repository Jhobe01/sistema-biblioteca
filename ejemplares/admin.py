from django.contrib import admin
from .models import Ejemplar


@admin.register(Ejemplar)
class EjemplarAdmin(admin.ModelAdmin):
    list_display = ('eje_codigo_inventario', 'fk_lib_id', 'eje_estado', 'eje_ubicacion')
    search_fields = ('eje_codigo_inventario', 'fk_lib_id__lib_titulo')
    list_filter = ('eje_estado', 'eje_ubicacion')
