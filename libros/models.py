from django.db import models


class Libro(models.Model):
    pk_lib_id = models.AutoField(primary_key=True)
    lib_titulo = models.CharField(max_length=180)
    lib_isbn = models.CharField(max_length=20, unique=True)
    lib_editorial = models.CharField(max_length=120, blank=True)
    lib_anio_publicacion = models.PositiveSmallIntegerField(null=True, blank=True)
    lib_genero = models.CharField(max_length=80, blank=True)
    lib_descripcion = models.TextField(blank=True)
    lib_autores = models.ManyToManyField(
        'autores.Autor', through='libro_autor.LibroAutor', related_name='libros', blank=True
    )

    class Meta:
        db_table = 'tbl_libro'
        ordering = ['lib_titulo']
        verbose_name = 'libro'
        verbose_name_plural = 'libros'

    def __str__(self):
        return f'{self.lib_titulo} ({self.lib_isbn})'
