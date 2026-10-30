from django.shortcuts import render, redirect, get_object_or_404
from .models import Obra, FechaVisita
from django.db.models import Q
from .forms import ObraForm, ClienteForm
from presupuestos.models import Presupuesto

# Create your views here.
def obras_total(request):
    obras = Obra.objects.all().order_by('fecha_contacto')

    search_input = request.GET.get('search', '').strip()
    if (search_input):
        obras = obras.filter(
            Q(cliente__nombre__icontains=search_input) | 
            Q(cliente__apellido__icontains=search_input) |
            Q(direccion__icontains=search_input)
        )

    return render(request, 'obras/obras.html', {'obras': obras, 'search_input': search_input})

def obra_detalle(request, pk):
    try:
        obra = Obra.objects.get(pk=pk)
        presupuestos = Presupuesto.objects.filter(
            obra = obra
        ).order_by('fecha_actual')

        return render(request, 'obras/obra_detalle.html', {'obra': obra, 'presupuestos':presupuestos})
    except: # Si no encuentra la obra con el id ingresado como parámetro, retorna un template de not found.
        return render(request, 'not_found.html')


def obra_crear(request):
    try:
        if request.method == 'POST':
            form = ObraForm(request.POST)

            if form.is_valid():
                obra = guardar_obra_con_fecha(form)
                campos_presupuesto = [
                    "metro_2",
                    "precio_metro",
                    "material",
                    "superficie",
                    "obra",
                    "observacion",
                    "recargo_porcentaje",
                    "descripcion_impresa",
                ]
                datos_presupuesto = {
                    campo: request.POST.get(f"presupuesto__{campo}", "")
                    for campo in campos_presupuesto
                }
                datos_presupuesto["obra"] = str(obra.pk)
                request.session["presupuesto_pendiente"] = datos_presupuesto
                if request.POST.get("origen") == "presupuestos":
                    request.session["abrir_modal_presupuesto"] = True
                return redirect("presupuestos:presupuestos_total")
        else:
            datos_obra = request.session.pop("obra_pendiente", {})
            form = ObraForm(initial=datos_obra)
        return render(request, 'obras/obra_crear.html', {
            'obra_form': form,
            'cliente_form': ClienteForm(),
            'abrir_modal_cliente': False,
        })
    except:
        return render(request, 'not_found.html')

def cliente_crear(request):
    try:
        if request.method != 'POST':
            return redirect("presupuestos:presupuestos_total")

        form_cliente = ClienteForm(request.POST)

        if form_cliente.is_valid():
            cliente = form_cliente.save()

            campos_obra = [
                "cliente", "direccion", "zona", "observacion",
                "negocio", "estado", "garantia",
                "proxima_accion", "fecha_visita",
            ]

            campos_presupuesto = [
                "metro_2", "precio_metro", "material", "superficie",
                "observacion", "recargo_porcentaje", "descripcion_impresa",               
            ]

            datos_obra = {
                campo: request.POST.get(f"obra__{campo}", "")
                for campo in campos_obra
            }

            datos_obra["cliente"] = str(cliente.pk)

            if request.POST.get("origen") == "obra_crear":
                request.session["obra_pendiente"] = datos_obra
                return redirect("obras:obra_crear")

            datos_presupuesto = {
                campo: request.POST.get(f"presupuesto__{campo}", "")
                for campo in campos_presupuesto
            }

            request.session["obra_pendiente"] = datos_obra
            request.session["presupuesto_pendiente"] = datos_presupuesto
            request.session["abrir_modal_obra"] = True
            request.session["abrir_modal_presupuesto"] = True

            return redirect("presupuestos:presupuestos_total")

        datos_obra = {
            campo: request.POST.get(f"obra__{campo}", "")
            for campo in [
                "cliente", "direccion", "zona", "observacion",
                "negocio", "estado", "garantia",
                "proxima_accion", "fecha_visita",
            ]
        }
        return render(request, "obras/obra_crear.html", {
            "obra_form": ObraForm(initial=datos_obra),
            "cliente_form": form_cliente,
            "abrir_modal_cliente": True,
        })
    except:
        return render(request, 'not_found.html')

def obra_actualizar(request, pk):
    obra = get_object_or_404(Obra, pk=pk)
    form = ObraForm(request.POST or None, instance=obra)

    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('obras:obra_detalle', pk=obra.pk)

    return render(request, 'obras/obra_crear.html', {
        'obra': obra,
        'obra_form': form,
        'cliente_form': ClienteForm(),
        'abrir_modal_cliente': False,
        'es_edicion': True,
    })


def guardar_obra_con_fecha(form):
    obra = form.save(commit=False)

    fecha = form.cleaned_data.get('fecha_visita')

    if fecha:
        ultima_fecha = FechaVisita.objects.order_by('-numero').first()
        nuevo_numero = ultima_fecha.numero + 1 if ultima_fecha else 1

        fecha_visita = FechaVisita.objects.create(
            numero=nuevo_numero,
            fecha=fecha
        )

        obra.fecha_visita = fecha_visita
    else:
        obra.fecha_visita = None

    obra.save()
    form.save_m2m()

    return obra