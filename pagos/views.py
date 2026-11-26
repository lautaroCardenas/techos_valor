from django.shortcuts import render, get_object_or_404, redirect
from .models import Pagos
from .forms import PagosForm
from obras.models import Obra
from presupuestos.models import Presupuesto
from django.db.models import Q, Sum, F, Value, DecimalField
from django.db.models.functions import Coalesce
from django.urls import reverse
from servicios.envio_unico import envio_unico

# Create your views here.
def pagos_total(request):
    # form_pago = PagosForm()
    pagos = Pagos.objects.all().order_by('presupuesto')
    # obras = Obra.objects.all()

    pagos = pagos.filter(
        presupuesto__aceptado=True
    )

    search_input = request.GET.get('search_input', '').strip()
    negocio_filter = request.GET.get('negocio', '').strip()

    presupuestos = Presupuesto.objects.filter(aceptado=True).select_related('obra__cliente', 'obra__zona').order_by('obra')

    if (search_input):
        presupuestos = presupuestos.filter(
            Q(obra__cliente__nombre__icontains=search_input) |
            Q(obra__cliente__apellido__icontains=search_input)
        )

    if negocio_filter:
        presupuestos = presupuestos.filter(
            obra__negocio=True
        )

    # presupuestos = Presupuesto.objects.filter(
    #     aceptado=True
    # ).select_related('obra__cliente').order_by('obra')

    for p in presupuestos:
        ultimo_pago = Pagos.objects.filter(
            presupuesto=p
        ).last()

        p.resto_actual = ultimo_pago.resto if ultimo_pago else p.monto

    return render(request, 'pagos/pagos.html', {'pagos': pagos, 'presupuestos': presupuestos, 'search_input': search_input, 'negocio_filter': negocio_filter})

def pago_detalle(request, obra_pk, presupuesto_pk):
    try:
        obra = get_object_or_404(
            Obra.objects.select_related('cliente', 'zona'), pk=obra_pk
        )

        presupuesto = get_object_or_404(Presupuesto, pk=presupuesto_pk, obra=obra, aceptado=True)

        # pagos = Pagos.objects.none()
        pagos = Pagos.objects.filter(
            presupuesto=presupuesto
        ).order_by('numero')

        form_pago = PagosForm(presupuesto=presupuesto)

        if presupuesto:
            pagos = Pagos.objects.filter(
                presupuesto=presupuesto
            ).order_by('numero')

        
        return render(request, 'pagos/pago_detalle.html', {
            'pagos': pagos,
            'obra': obra,
            'presupuesto': presupuesto,
            'form_pago': form_pago,
        })
    except:
        return render(request, 'not_found.html')


def _destino_pago_duplicado(request):
    presupuesto = Presupuesto.objects.filter(
        pk=request.POST.get("presupuesto_id") or None
    ).values("pk", "obra_id").first()
    if presupuesto:
        return reverse("pagos:pago_detalle", args=[presupuesto["obra_id"], presupuesto["pk"]])
    return reverse("pagos:pagos_total")


@envio_unico("Pago cargado correctamente", _destino_pago_duplicado)
def pago_crear(request):
    if request.method == 'POST':
        presupuesto = get_object_or_404(
            Presupuesto,
            pk=request.POST.get('presupuesto_id'),
            aceptado=True,
        )
        form_pago = PagosForm(request.POST, presupuesto=presupuesto)
        form_pago.instance.presupuesto = presupuesto
        
        if form_pago.is_valid():
            form_pago.save()
            return redirect('pagos:pago_detalle', obra_pk=presupuesto.obra_id, presupuesto_pk=presupuesto.pk)

        obra = presupuesto.obra
        pagos = Pagos.objects.filter(
            presupuesto=presupuesto
        ).order_by('numero')
        return render(request, 'pagos/pago_detalle.html', {
            'pagos': pagos,
            'obra': obra,
            'presupuesto': presupuesto,
            'form_pago': form_pago,
            'abrir_modal_pago': True,
        })

    return render(request, 'pagos/pago_crear.html', {'form_pago': PagosForm()})
    
def pago_borrar(request, pk):
    if request.method == 'POST':
        pago = get_object_or_404(Pagos, pk=pk)

        # obra_id = pago.presupuesto.obra_id
        presupuesto = pago.presupuesto

        ultimo_pago = Pagos.objects.filter(
            presupuesto=presupuesto
        ).order_by('-numero').first()

        if ultimo_pago and ultimo_pago.pk == pago.pk:
            pago.delete()

        return redirect('pagos:pago_detalle', obra_pk=presupuesto.obra_id, presupuesto_pk=presupuesto.pk)

    return redirect('pagos:pagos_total')