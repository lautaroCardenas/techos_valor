from django.shortcuts import render, redirect
from .models import Obra
from django.db.models import Q
from .forms import ObraForm, ClienteForm

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
        return render(request, 'obras/obra_detalle.html', {'obra': obra})
    except: # Si no encuentra la obra con el id ingresado como parámetro, retorna un template de not found.
        return render(request, 'not_found.html')


def obra_crear(request):
    try:
        if request.method == 'POST':
            form = ObraForm(request.POST)

            if form.is_valid():
                obra = form.save()
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