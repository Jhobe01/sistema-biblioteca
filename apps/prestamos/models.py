from django.db import models
from django.utils import timezone


class Prestamo(models.Model):
    ESTADOS = [
        ('activo', 'Activo'),
        ('devuelto', 'Devuelto'),
        ('vencido', 'Vencido'),
        ('cancelado', 'Cancelado'),
    ]
    pk_pre_id = models.AutoField(primary_key=True)
    fk_lec_id = models.ForeignKey(
        'lectores.Lector', on_delete=models.PROTECT, db_column='fk_lec_id', related_name='prestamos'
    )
    pre_fecha_prestamo = models.DateField(default=timezone.localdate)
    pre_fecha_limite = models.DateField()
    pre_estado = models.CharField(max_length=20, choices=ESTADOS, default='activo')
    pre_observaciones = models.TextField(blank=True)

    class Meta:
        db_table = 'tbl_prestamo'
        ordering = ['-pre_fecha_prestamo', '-pk_pre_id']
        verbose_name = 'préstamo'
        verbose_name_plural = 'préstamos'

    def __str__(self):
        return f'Préstamo #{self.pk_pre_id} — {self.fk_lec_id}'
