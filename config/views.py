from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from ejemplares.models import Ejemplar
from lectores.models import Lector
from libros.models import Libro
from prestamos.models import Prestamo


@login_required
def inicio(request):
    tarjetas = [
        {'titulo': 'Libros', 'valor': Libro.objects.count(), 'icono': 'bi-book'},
        {'titulo': 'Ejemplares disponibles',
         'valor': Ejemplar.objects.filter(eje_estado='disponible').count(), 'icono': 'bi-check2-circle'},
        {'titulo': 'Lectores activos',
         'valor': Lector.objects.filter(lec_activo=True).count(), 'icono': 'bi-people'},
        {'titulo': 'Préstamos activos',
         'valor': Prestamo.objects.filter(pre_estado='activo').count(), 'icono': 'bi-arrow-left-right'},
    ]
    ultimos = Prestamo.objects.select_related('fk_lec_id')[:5]
    return render(request, 'inicio.html', {'tarjetas': tarjetas, 'ultimos': ultimos})
