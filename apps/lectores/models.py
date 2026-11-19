from django.db import models


class Lector(models.Model):
    pk_lec_id = models.AutoField(primary_key=True)
    lec_documento = models.CharField(max_length=25, unique=True)
    lec_nombres = models.CharField(max_length=100)
    lec_apellidos = models.CharField(max_length=100)
    lec_correo = models.EmailField(unique=True)
    lec_telefono = models.CharField(max_length=25, blank=True)
    lec_fecha_registro = models.DateField(auto_now_add=True)
    lec_activo = models.BooleanField(default=True)

    class Meta:
        db_table = 'tbl_lector'
        ordering = ['lec_apellidos', 'lec_nombres']
        verbose_name = 'lector'
        verbose_name_plural = 'lectores'

    def __str__(self):
        return f'{self.lec_nombres} {self.lec_apellidos} ({self.lec_documento})'
