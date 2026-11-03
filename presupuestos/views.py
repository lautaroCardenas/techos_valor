from django.shortcuts import render, redirect
from .models import Presupuesto
from django.db.models import Q, Count, Prefetch
from obras.models import Obra, ProximaAccion, EstadoObra
from obras.forms import ObraForm, ClienteForm
from .forms import PresupuestoForm

# Create your views here.
def presupuestos_total(request):
    # presupuestos = Presupuesto.objects.all().order_by('fecha_actual')
    obras = Obra.objects.annotate(
        cant_presupuestos=Count('presupuesto', distinct=True)
    ).order_by('id')

    search_input = request.GET.get('search', '').strip()
    if search_input:
        obras = obras.filter(
            Q(cliente__nombre__icontains=search_input) |
            Q(cliente__apellido__icontains=search_input) |
            Q(direccion__icontains=search_input) |
            Q(presupuesto__material__material__icontains=search_input)
        )

    search_filter = request.GET.get('filter', '').strip()
    if (search_filter):
        obras = obras.filter(
            Q(proxima_accion__accion__icontains=search_filter)
        )

    estado_filter = request.GET.get('estado_filter', '').strip()
    if (estado_filter):
        obras = obras.filter(
            estado__estado=estado_filter
        ) 

    negocio_filter = request.GET.get('negocio_filter') == 'on'
    if negocio_filter:
        obras = obras.filter(
            negocio=True
        )

    # Cada tarjeta muestra datos de la obra y de todos sus presupuestos. Sin esto el
    # template hacía una consulta por cada cliente, zona, presupuesto, material, etc.
    obras = obras.distinct().select_related(
        'cliente', 'zona', 'estado', 'proxima_accion', 'fecha_visita'
    ).prefetch_related(
        Prefetch(
            'presupuesto_set',
            queryset=Presupuesto.objects.select_related('material', 'superficie').order_by('fecha_actual'),
            to_attr='presupuestos',
        )
    )

    proxima_acciones = ProximaAccion.objects.all().order_by('accion')
    estados_obra = EstadoObra.objects.all().order_by('estado')
    # form = PresupuestoForm()
    datos_presupuesto = request.session.get(
        "presupuesto_pendiente", {}
    )
    datos_obra = request.session.get("obra_pendiente", {})
    form = PresupuestoForm(initial=datos_presupuesto)
    obra_form = ObraForm(initial=datos_obra)
    cliente_form = ClienteForm()

    abrir_modal_obra = request.session.pop("abrir_modal_obra", False)
    abrir_modal_presupuesto = request.session.pop(
        "abrir_modal_presupuesto", False
    )

    return render(request, 'presupuestos/presupuestos.html', {'obras': obras, 'search_input': search_input, 'search_filter': search_filter, 'proxima_acciones': proxima_acciones, 'estado_filter': estado_filter, 'estados_obra': estados_obra, 'negocio_filter': negocio_filter, 'form': form, 'obra_form': obra_form, 'cliente_form': cliente_form, 'abrir_modal_obra':abrir_modal_obra, 'abrir_modal_presupuesto': abrir_modal_presupuesto})

def presupuesto_detalle(request, pk):
    try:
        pres = Presupuesto.objects.select_related(
            'material', 'superficie', 'obra__cliente', 'obra__zona',
            'obra__estado', 'obra__proxima_accion', 'obra__fecha_visita',
        ).get(pk=pk)
        return render(request, 'presupuestos/presupuesto_detalle.html', {'presupuesto': pres})
    except:
        return render(request, 'not_found.html')

def presupuesto_crear(request):
    try:
        form = PresupuestoForm()
        obra_form = ObraForm()
        if request.method == 'POST':
            form = PresupuestoForm(request.POST)

            if form.is_valid():
                form.save()
                return redirect('presupuestos:presupuestos_total')
        else:
            form = PresupuestoForm()
        return render(request, 'presupuestos/presupuesto_crear.html', {'form': form, 'obra_form': obra_form})
    except:
        return render(request, 'not_found.html')