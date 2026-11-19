from django.db import models


class Autor(models.Model):
    pk_aut_id = models.AutoField(primary_key=True)
    aut_nombre = models.CharField(max_length=120)
    aut_apellido = models.CharField(max_length=120)
    aut_nacionalidad = models.CharField(max_length=80, blank=True)
    aut_fecha_nacimiento = models.DateField(null=True, blank=True)

    class Meta:
        db_table = 'tbl_autor'
        ordering = ['aut_apellido', 'aut_nombre']
        verbose_name = 'autor'
        verbose_name_plural = 'autores'

    def __str__(self):
        return f'{self.aut_nombre} {self.aut_apellido}'
