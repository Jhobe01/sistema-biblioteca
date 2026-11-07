from django.contrib import admin
from .models import LibroAutor


@admin.register(LibroAutor)
class LibroAutorAdmin(admin.ModelAdmin):
    list_display = ('fk_lib_id', 'fk_aut_id')
    search_fields = ('fk_lib_id__lib_titulo', 'fk_aut_id__aut_apellido')
    list_filter = ('fk_aut_id__aut_nacionalidad',)
