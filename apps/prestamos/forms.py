from django import forms
from django.db.models import Q
from django.forms import BaseInlineFormSet, inlineformset_factory
from django.utils import timezone

from apps.detalle_prestamo.models import DetallePrestamo
from apps.ejemplares.models import Ejemplar
from apps.lectores.models import Lector
from .models import Prestamo


class PrestamoForm(forms.ModelForm):
    class Meta:
        model = Prestamo
        fields = ['fk_lec_id', 'pre_fecha_prestamo', 'pre_fecha_limite', 'pre_estado', 'pre_observaciones']
        labels = {
            'fk_lec_id': 'Lector',
            'pre_fecha_prestamo': 'Fecha del préstamo',
            'pre_fecha_limite': 'Fecha límite de devolución',
            'pre_estado': 'Estado',
            'pre_observaciones': 'Observaciones',
        }
        widgets = {
            'fk_lec_id': forms.Select(attrs={'class': 'form-select'}),
            'pre_fecha_prestamo': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}, format='%Y-%m-%d'),
            'pre_fecha_limite': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}, format='%Y-%m-%d'),
            'pre_estado': forms.Select(attrs={'class': 'form-select'}),
            'pre_observaciones': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Solo lectores activos (más el lector actual si se está editando)
        filtro = Q(lec_activo=True)
        if self.instance.pk:
            filtro |= Q(pk=self.instance.fk_lec_id_id)
        self.fields['fk_lec_id'].queryset = Lector.objects.filter(filtro)
        self.fields['fk_lec_id'].empty_label = 'Selecciona un lector...'

    def clean(self):
        datos = super().clean()
        f_prestamo = datos.get('pre_fecha_prestamo')
        f_limite = datos.get('pre_fecha_limite')
        if f_prestamo and f_limite and f_limite < f_prestamo:
            self.add_error('pre_fecha_limite', 'La fecha límite no puede ser anterior a la fecha del préstamo.')
        return datos


class DetalleCrearForm(forms.ModelForm):
    """Fila del préstamo al crear: solo se elige el ejemplar."""

    class Meta:
        model = DetallePrestamo
        fields = ['fk_eje_id']
        labels = {'fk_eje_id': 'Ejemplar'}
        widgets = {'fk_eje_id': forms.Select(attrs={'class': 'form-select'})}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Solo ejemplares disponibles (más el que ya tiene esta fila, al editar)
        filtro = Q(eje_estado='disponible')
        if self.instance.pk:
            filtro |= Q(pk=self.instance.fk_eje_id_id)
        self.fields['fk_eje_id'].queryset = Ejemplar.objects.select_related('fk_lib_id').filter(filtro)
        self.fields['fk_eje_id'].empty_label = 'Selecciona un ejemplar...'


class DetalleEditarForm(DetalleCrearForm):
    """Fila del préstamo al editar: además se registra la devolución."""

    class Meta(DetalleCrearForm.Meta):
        fields = ['fk_eje_id', 'det_fecha_devolucion', 'det_condicion_devolucion']
        labels = {
            'fk_eje_id': 'Ejemplar',
            'det_fecha_devolucion': 'Fecha de devolución',
            'det_condicion_devolucion': 'Condición al devolver',
        }
        widgets = {
            'fk_eje_id': forms.Select(attrs={'class': 'form-select'}),
            'det_fecha_devolucion': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}, format='%Y-%m-%d'),
            'det_condicion_devolucion': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej.: buen estado'}),
        }

    def clean_det_fecha_devolucion(self):
        fecha = self.cleaned_data.get('det_fecha_devolucion')
        if fecha and fecha > timezone.localdate():
            raise forms.ValidationError('La fecha de devolución no puede estar en el futuro.')
        return fecha


class BaseDetalleFormSet(BaseInlineFormSet):
    def clean(self):
        super().clean()
        if any(self.errors):
            return
        vistos = set()
        cantidad = 0
        for form in self.forms:
            datos = getattr(form, 'cleaned_data', None)
            if not datos or datos.get('DELETE') or not datos.get('fk_eje_id'):
                continue
            ejemplar = datos['fk_eje_id']
            if ejemplar.pk in vistos:
                raise forms.ValidationError('No puedes repetir el mismo ejemplar en un préstamo.')
            vistos.add(ejemplar.pk)
            cantidad += 1
        if cantidad == 0:
            raise forms.ValidationError('Agrega al menos un ejemplar al préstamo.')


DetalleCrearFormSet = inlineformset_factory(
    Prestamo, DetallePrestamo, form=DetalleCrearForm, formset=BaseDetalleFormSet,
    extra=2, can_delete=False,
)
DetalleEditarFormSet = inlineformset_factory(
    Prestamo, DetallePrestamo, form=DetalleEditarForm, formset=BaseDetalleFormSet,
    extra=1, can_delete=True,
)
