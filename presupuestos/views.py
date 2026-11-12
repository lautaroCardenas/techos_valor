from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Presupuesto
from django.db.models import Q, Count
from obras.models import Obra, ProximaAccion, EstadoObra
from obras.forms import ObraForm, ClienteForm
from .forms import PresupuestoForm

# Create your views here.
EXTRA_TAG = 'presupuestos_messages'

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

    obras = obras.distinct()

    proxima_acciones = ProximaAccion.objects.all().order_by('accion')
    estados_obra = EstadoObra.objects.all().order_by('estado')
    # form = PresupuestoForm()
    # datos_presupuesto = request.session.get(
    #     "presupuesto_pendiente", {}
    # )
    datos_presupuesto = request.session.pop(
        "presupuesto_pendiente", None
    )

    if datos_presupuesto:
        form = PresupuestoForm(datos_presupuesto)
        form.is_valid()
    else:
        form = PresupuestoForm()
    
    datos_obra = request.session.pop("obra_pendiente", None)

    if datos_obra:
        obra_form = ObraForm(datos_obra)
        obra_form.is_valid()
    else:
        obra_form = ObraForm()
    
    datos_cliente = request.session.pop("cliente_pendiente", None)

    if datos_cliente:
        cliente_form = ClienteForm(datos_cliente)
        cliente_form.is_valid()
    else:
        cliente_form = ClienteForm()

    abrir_modal_obra = request.session.pop("abrir_modal_obra", False)
    abrir_modal_cliente = request.session.pop(
        "abrir_modal_cliente", False
    )
    abrir_modal_presupuesto = request.session.pop(
        "abrir_modal_presupuesto", False
    )

    return render(request, 'presupuestos/presupuestos.html', {'obras': obras, 'search_input': search_input, 'search_filter': search_filter, 'proxima_acciones': proxima_acciones, 'estado_filter': estado_filter, 'estados_obra': estados_obra, 'negocio_filter': negocio_filter, 'form': form, 'obra_form': obra_form, 'cliente_form': cliente_form, 'abrir_modal_obra':abrir_modal_obra, 'abrir_modal_presupuesto': abrir_modal_presupuesto, 'abrir_modal_cliente': abrir_modal_cliente,})

def presupuesto_detalle(request, pk):
    try:
        pres = Presupuesto.objects.get(pk=pk)
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
            
            request.session["presupuesto_pendiente"] = request.POST.dict()
            request.session["abrir_modal_presupuesto"] = True

            return redirect('presupuestos:presupuestos_total')
        else:
            form = PresupuestoForm()
        return render(request, 'presupuestos/presupuesto_crear.html', {'form': form, 'obra_form': obra_form})
    except:
        return render(request, 'not_found.html')

def presupuesto_borrar(request, pk):
    if request.method == 'POST':
        presupuesto = get_object_or_404(Presupuesto, pk=pk)

        if presupuesto.pagos_set.exists():
            messages.error(request, 'No se puede eliminar un presupuesto que tiene pagos asociados', extra_tags=EXTRA_TAG)
        else:
            presupuesto.delete()
            messages.success(request, 'Presupuesto eliminado correctamente', extra_tags=EXTRA_TAG)

    return redirect('presupuestos:presupuestos_total')

def presupuesto_actualizar(request, pk):
    pres = get_object_or_404(Presupuesto, pk=pk)

    if request.method == 'POST':
        presupuesto_form = PresupuestoForm(
            request.POST,
            instance=pres
        )

        if presupuesto_form.is_valid():
            presupuesto_form.save()

            messages.success(
                request,
                'Presupuesto actualizado correctamente',
                extra_tags=EXTRA_TAG
            )

            return render(
                request,
                'presupuestos/presupuesto_actualizado.html',
                {'presupuesto': pres}
            )

        return render(
            request,
            'presupuestos/_form_editar.html',
            {
                'pres': pres,
                'presupuesto_form': presupuesto_form
            },
            status=400
        )

def presupuesto_editar_form(request, pk):
    pres = get_object_or_404(Presupuesto, pk=pk)

    presupuesto_form = PresupuestoForm(instance=pres)

    return render(request, 'presupuestos/_form_editar.html', {
        'pres': pres,
        'presupuesto_form': presupuesto_form
    })