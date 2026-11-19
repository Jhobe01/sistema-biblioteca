from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Count, Q
from django.shortcuts import get_object_or_404, render

from .models import Libro


@login_required
def lista(request):
    q = request.GET.get('q', '').strip()
    genero = request.GET.get('genero', '')
    libros = Libro.objects.prefetch_related('lib_autores').annotate(
        disponibles=Count('ejemplares', filter=Q(ejemplares__eje_estado='disponible')),
        total=Count('ejemplares'),
    ).order_by('lib_titulo')
    if q:
        libros = libros.filter(
            Q(lib_titulo__icontains=q) | Q(lib_isbn__icontains=q)
            | Q(lib_autores__aut_nombre__icontains=q) | Q(lib_autores__aut_apellido__icontains=q)
        ).distinct()
    if genero:
        libros = libros.filter(lib_genero=genero)
    generos = (Libro.objects.exclude(lib_genero='').order_by('lib_genero')
               .values_list('lib_genero', flat=True).distinct())
    pagina = Paginator(libros, 9).get_page(request.GET.get('page'))
    return render(request, 'libros/lista.html', {
        'pagina': pagina, 'q': q, 'genero': genero, 'generos': generos,
    })


@login_required
def detalle(request, pk):
    libro = get_object_or_404(Libro.objects.prefetch_related('lib_autores', 'ejemplares'), pk=pk)
    return render(request, 'libros/detalle.html', {'libro': libro})
