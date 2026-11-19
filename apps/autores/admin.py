from django.contrib import admin
from .models import Autor


@admin.register(Autor)
class AutorAdmin(admin.ModelAdmin):
    list_display = ('aut_nombre', 'aut_apellido', 'aut_nacionalidad')
    search_fields = ('aut_nombre', 'aut_apellido', 'aut_nacionalidad')
    list_filter = ('aut_nacionalidad',)
