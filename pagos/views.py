from django.shortcuts import render, get_object_or_404, redirect
from .models import Pagos
from .forms import PagosForm
from obras.models import Obra
from presupuestos.models import Presupuesto
from django.db.models import Q, Sum, F, Value, DecimalField
from django.db.models.functions import Coalesce

# Create your views here.
def pagos_total(request):
    # form_pago = PagosForm()
    pagos = Pagos.objects.all().order_by('presupuesto')
    # obras = Obra.objects.all()

    pagos = pagos.filter(
        presupuesto__aceptado=True
    )

    search_input = request.GET.get('search_input', '').strip()
    negocio_filter = request.GET.get('filter', '').strip()

    presupuestos = Presupuesto.objects.filter(aceptado=True)

    if (search_input):
        pagos = pagos.filter(
            Q(presupuesto__obra__cliente__nombre__icontains=search_input) |
            Q(presupuesto__obra__cliente__apellido__icontains=search_input)
        )

    if negocio_filter:
        presupuestos = presupuestos.filter(
            aceptado=True
        )

    # obras = obras.filter(
    #     presupuesto__aceptado=True
    # ).distinct()
    # obras = obras.distinct()
    presupuestos = Presupuesto.objects.filter(
        aceptado=True
    ).select_related('obra__cliente').order_by('obra')

    for p in presupuestos:
        ultimo_pago = Pagos.objects.filter(
            presupuesto=p
        ).last()

        p.resto_actual = ultimo_pago.resto if ultimo_pago else p.monto

    return render(request, 'pagos/pagos.html', {'pagos': pagos, 'presupuestos': presupuestos, 'search_input': search_input, 'negocio_filter': negocio_filter})

def pago_detalle(request, pk):
    try:
        obra = get_object_or_404(
            Obra.objects.select_related('cliente'), pk=pk
        )

        presupuesto = Presupuesto.objects.filter(
            obra = obra, aceptado=True
        ).order_by('-fecha_actual').first()

        # pagos = Pagos.objects.none()
        pagos = Pagos.objects.all()
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
            return redirect('pagos:pago_detalle', pk=presupuesto.obra_id)

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
    
