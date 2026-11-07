from django.contrib import admin
from .models import Lector


@admin.register(Lector)
class LectorAdmin(admin.ModelAdmin):
    list_display = ('lec_documento', 'lec_nombres', 'lec_apellidos', 'lec_correo', 'lec_activo')
    search_fields = ('lec_documento', 'lec_nombres', 'lec_apellidos', 'lec_correo')
    list_filter = ('lec_activo', 'lec_fecha_registro')
