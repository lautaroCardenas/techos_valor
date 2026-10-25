from django.shortcuts import render, redirect
from .models import Presupuesto
from django.db.models import Q
from obras.models import ProximaAccion, EstadoObra
from .forms import PresupuestoForm

# Create your views here.
def presupuestos_total(request):
    presupuestos = Presupuesto.objects.all().order_by('fecha_actual')

    search_input = request.GET.get('search', '').strip()
    if (search_input):
        presupuestos = presupuestos.filter(
            Q(obra__cliente__nombre__icontains=search_input) |
            Q(obra__cliente__apellido__icontains=search_input) |
            Q(obra__direccion__icontains=search_input) |
            Q(material__material__icontains=search_input)
        )

    search_filter = request.GET.get('filter', '').strip()
    if (search_filter):
        presupuestos = presupuestos.filter(
            Q(obra__proxima_accion__accion__icontains=search_filter)
        )

    estado_filter = request.GET.get('estado_filter', '').strip()
    if (estado_filter):
        presupuestos = presupuestos.filter(
            obra__estado_obra__estado=estado_filter
        ) 

    negocio_filter = request.GET.get('negocio_filter') == 'on'
    if negocio_filter:
        presupuestos = presupuestos.filter(
            obra__negocio=True
        )

    proxima_acciones = ProximaAccion.objects.all().order_by('accion')
    estados_obra = EstadoObra.objects.all().order_by('estado')
    form = PresupuestoForm()

    return render(request, 'presupuestos/presupuestos.html', {'presupuestos': presupuestos, 'search_input': search_input, 'search_filter': search_filter, 'proxima_acciones': proxima_acciones, 'estado_filter': estado_filter, 'estados_obra': estados_obra, 'negocio_filter': negocio_filter, 'form': form})

def presupuesto_detalle(request, pk):
    try:
        pres = Presupuesto.objects.get(pk=pk)
        return render(request, 'presupuestos/presupuesto_detalle.html', {'presupuesto': pres})
    except:
        return render(request, 'not_found.html')

def presupuesto_crear(request):
    try:
        if request.method == 'POST':
            form = PresupuestoForm(request.POST)

            if form.is_valid():
                form.save()
                return redirect('presupuestos:presupuestos_total')
        else:
            form = PresupuestoForm()
        return render(request, 'presupuestos/presupuesto_crear.html', {'form': form})
    except:
        return render(request, 'not_found.html')