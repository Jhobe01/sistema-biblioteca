from django.db import models


class Ejemplar(models.Model):
    """Entidad débil: no existe sin el libro al que pertenece."""
    ESTADOS = [
        ('disponible', 'Disponible'),
        ('prestado', 'Prestado'),
        ('mantenimiento', 'Mantenimiento'),
        ('perdido', 'Perdido'),
    ]
    pk_eje_id = models.AutoField(primary_key=True)
    fk_lib_id = models.ForeignKey(
        'libros.Libro', on_delete=models.CASCADE, db_column='fk_lib_id', related_name='ejemplares'
    )
    eje_codigo_inventario = models.CharField(max_length=30, unique=True)
    eje_ubicacion = models.CharField(max_length=80, blank=True)
    eje_estado = models.CharField(max_length=20, choices=ESTADOS, default='disponible')
    eje_fecha_adquisicion = models.DateField(null=True, blank=True)

    class Meta:
        db_table = 'tbl_ejemplar'
        ordering = ['eje_codigo_inventario']
        verbose_name = 'ejemplar'
        verbose_name_plural = 'ejemplares'

    def __str__(self):
        return f'{self.eje_codigo_inventario} — {self.fk_lib_id.lib_titulo}'
