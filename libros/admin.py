from django.contrib import admin
from .models import Libro
from ejemplares.models import Ejemplar
from libro_autor.models import LibroAutor


class EjemplarInline(admin.TabularInline):
    model = Ejemplar
    extra = 1


class LibroAutorInline(admin.TabularInline):
    model = LibroAutor
    extra = 1


@admin.register(Libro)
class LibroAdmin(admin.ModelAdmin):
    list_display = ('lib_titulo', 'lib_isbn', 'lib_editorial', 'lib_anio_publicacion', 'lib_genero')
    search_fields = ('lib_titulo', 'lib_isbn', 'lib_editorial')
    list_filter = ('lib_genero', 'lib_editorial', 'lib_anio_publicacion')
    inlines = [LibroAutorInline, EjemplarInline]
