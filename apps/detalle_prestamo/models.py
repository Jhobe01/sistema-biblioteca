from django.db import models


class DetallePrestamo(models.Model):
    """Tabla intermedia del N:M Préstamo - Ejemplar."""
    pk_det_id = models.AutoField(primary_key=True)
    fk_pre_id = models.ForeignKey(
        'prestamos.Prestamo', on_delete=models.CASCADE, db_column='fk_pre_id', related_name='detalles'
    )
    fk_eje_id = models.ForeignKey(
        'ejemplares.Ejemplar', on_delete=models.PROTECT, db_column='fk_eje_id',
        related_name='detalles_prestamo'
    )
    det_fecha_devolucion = models.DateField(null=True, blank=True)
    det_condicion_devolucion = models.CharField(max_length=120, blank=True)

    class Meta:
        db_table = 'tbl_detalle_prestamo'
        ordering = ['fk_pre_id', 'fk_eje_id']
        constraints = [
            models.UniqueConstraint(fields=['fk_pre_id', 'fk_eje_id'], name='uq_prestamo_ejemplar')
        ]
        verbose_name = 'detalle de préstamo'
        verbose_name_plural = 'detalles de préstamo'

    def __str__(self):
        return f'{self.fk_pre_id} / {self.fk_eje_id}'
