from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db import transaction
from django.db.models import Count, Q
from django.shortcuts import get_object_or_404, redirect, render

from apps.ejemplares.models import Ejemplar
from .forms import DetalleCrearFormSet, DetalleEditarFormSet, PrestamoForm
from .models import Prestamo


def _sincronizar(prestamo, ejemplares_previos):
    """Mantiene coherente el estado de los ejemplares con el préstamo."""
    detalles = list(prestamo.detalles.select_related('fk_eje_id'))

    # Si todos los ejemplares ya se devolvieron, el préstamo queda devuelto
    if (detalles and prestamo.pre_estado in ('activo', 'vencido')
            and all(d.det_fecha_devolucion for d in detalles)):
        prestamo.pre_estado = 'devuelto'
        prestamo.save(update_fields=['pre_estado'])

    actuales = set()
    for d in detalles:
        ejemplar = d.fk_eje_id
        actuales.add(ejemplar.pk)
        cerrado = d.det_fecha_devolucion or prestamo.pre_estado in ('devuelto', 'cancelado')
        nuevo = 'disponible' if cerrado else 'prestado'
        if ejemplar.eje_estado in ('disponible', 'prestado') and ejemplar.eje_estado != nuevo:
            ejemplar.eje_estado = nuevo
            ejemplar.save(update_fields=['eje_estado'])

    # Ejemplares que se quitaron del préstamo vuelven a estar disponibles
    Ejemplar.objects.filter(pk__in=ejemplares_previos - actuales, eje_estado='prestado') \
        .update(eje_estado='disponible')


@login_required
def lista(request):
    q = request.GET.get('q', '').strip()
    estado = request.GET.get('estado', '')
    prestamos = Prestamo.objects.select_related('fk_lec_id').annotate(total=Count('detalles')).order_by('-pre_fecha_prestamo', '-pk_pre_id')
    if q:
        filtro = (Q(fk_lec_id__lec_nombres__icontains=q) | Q(fk_lec_id__lec_apellidos__icontains=q)
                  | Q(fk_lec_id__lec_documento__icontains=q))
        if q.isdigit():
            filtro |= Q(pk_pre_id=int(q))
        prestamos = prestamos.filter(filtro)
    if estado:
        prestamos = prestamos.filter(pre_estado=estado)
    pagina = Paginator(prestamos, 8).get_page(request.GET.get('page'))
    return render(request, 'prestamos/lista.html', {
        'pagina': pagina, 'q': q, 'estado': estado, 'estados': Prestamo.ESTADOS,
    })


@login_required
def detalle(request, pk):
    prestamo = get_object_or_404(
        Prestamo.objects.select_related('fk_lec_id').prefetch_related('detalles__fk_eje_id__fk_lib_id'), pk=pk)
    return render(request, 'prestamos/detalle.html', {'prestamo': prestamo})


@login_required
def crear(request):
    prestamo = Prestamo()
    if request.method == 'POST':
        form = PrestamoForm(request.POST, instance=prestamo)
        formset = DetalleCrearFormSet(request.POST, instance=prestamo)
        if form.is_valid() and formset.is_valid():
            with transaction.atomic():
                prestamo = form.save()
                formset.instance = prestamo
                formset.save()
                _sincronizar(prestamo, set())
            messages.success(request, f'Préstamo #{prestamo.pk_pre_id} registrado correctamente.')
            return redirect('prestamos:detalle', pk=prestamo.pk_pre_id)
        messages.error(request, 'Revisa los campos marcados en el formulario.')
    else:
        form = PrestamoForm(instance=prestamo)
        formset = DetalleCrearFormSet(instance=prestamo)
    return render(request, 'prestamos/form.html', {
        'form': form, 'formset': formset, 'titulo': 'Nuevo préstamo', 'edicion': False,
    })


@login_required
def editar(request, pk):
    prestamo = get_object_or_404(Prestamo, pk=pk)
    previos = set(prestamo.detalles.values_list('fk_eje_id', flat=True))
    if request.method == 'POST':
        form = PrestamoForm(request.POST, instance=prestamo)
        formset = DetalleEditarFormSet(request.POST, instance=prestamo)
        if form.is_valid() and formset.is_valid():
            with transaction.atomic():
                prestamo = form.save()
                formset.save()
                _sincronizar(prestamo, previos)
            messages.success(request, f'Préstamo #{prestamo.pk_pre_id} actualizado.')
            return redirect('prestamos:detalle', pk=prestamo.pk_pre_id)
        messages.error(request, 'Revisa los campos marcados en el formulario.')
    else:
        form = PrestamoForm(instance=prestamo)
        formset = DetalleEditarFormSet(instance=prestamo)
    return render(request, 'prestamos/form.html', {
        'form': form, 'formset': formset, 'prestamo': prestamo,
        'titulo': f'Editar préstamo #{prestamo.pk_pre_id}', 'edicion': True,
    })


@login_required
def eliminar(request, pk):
    prestamo = get_object_or_404(Prestamo.objects.select_related('fk_lec_id'), pk=pk)
    if request.method == 'POST':
        previos = set(prestamo.detalles.values_list('fk_eje_id', flat=True))
        numero = prestamo.pk_pre_id
        with transaction.atomic():
            prestamo.delete()
            Ejemplar.objects.filter(pk__in=previos, eje_estado='prestado').update(eje_estado='disponible')
        messages.success(request, f'Préstamo #{numero} eliminado.')
        return redirect('prestamos:lista')
    return render(request, 'prestamos/confirmar_eliminar.html', {'prestamo': prestamo})
