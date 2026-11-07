from django.contrib import admin
from .models import Prestamo
from detalle_prestamo.models import DetallePrestamo


class DetallePrestamoInline(admin.TabularInline):
    model = DetallePrestamo
    extra = 1
    autocomplete_fields = ['fk_eje_id']


@admin.register(Prestamo)
class PrestamoAdmin(admin.ModelAdmin):
    list_display = ('pk_pre_id', 'fk_lec_id', 'pre_fecha_prestamo', 'pre_fecha_limite', 'pre_estado')
    search_fields = ('fk_lec_id__lec_nombres', 'fk_lec_id__lec_apellidos', 'fk_lec_id__lec_documento')
    list_filter = ('pre_estado', 'pre_fecha_prestamo', 'pre_fecha_limite')
    inlines = [DetallePrestamoInline]
