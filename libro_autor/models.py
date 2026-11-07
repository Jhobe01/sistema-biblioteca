from django.db import models


class LibroAutor(models.Model):
    """Tabla intermedia del N:M Libro - Autor."""
    pk_lia_id = models.AutoField(primary_key=True)
    fk_lib_id = models.ForeignKey(
        'libros.Libro', on_delete=models.CASCADE, db_column='fk_lib_id', related_name='autoria'
    )
    fk_aut_id = models.ForeignKey(
        'autores.Autor', on_delete=models.CASCADE, db_column='fk_aut_id', related_name='participaciones'
    )

    class Meta:
        db_table = 'tbl_libro_autor'
        constraints = [
            models.UniqueConstraint(fields=['fk_lib_id', 'fk_aut_id'], name='uq_libro_autor')
        ]
        verbose_name = 'relación libro-autor'
        verbose_name_plural = 'relaciones libro-autor'

    def __str__(self):
        return f'{self.fk_lib_id.lib_titulo} — {self.fk_aut_id}'
