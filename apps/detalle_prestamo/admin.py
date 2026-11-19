from django.contrib import admin
from .models import DetallePrestamo


@admin.register(DetallePrestamo)
class DetallePrestamoAdmin(admin.ModelAdmin):
    list_display = ('fk_pre_id', 'fk_eje_id', 'det_fecha_devolucion')
    search_fields = ('fk_pre_id__fk_lec_id__lec_nombres', 'fk_eje_id__eje_codigo_inventario')
    list_filter = ('det_fecha_devolucion',)
