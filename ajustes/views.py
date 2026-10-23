from django.shortcuts import render
from .forms import ZonaForm, ProximaAccionForm, EstadoObraForm
from django.contrib import messages
from obras.models import Zona, ProximaAccion, EstadoObra

# Create your views here.
mensaje_exito = 'El dato se guardó correctamente'
mensaje_error = 'No se pudo guardar el dato'

def ajustes(request):
    zona_form = ZonaForm()
    accion_form = ProximaAccionForm()
    estado_form = EstadoObraForm()

    if request.method == "POST":
        form_type = request.POST.get('form_type')
        if form_type == 'zona':
            zona_form = ZonaForm(request.POST)

            if zona_form.is_valid():
                zona_form.save()
                messages.success(request, mensaje_exito)
                zona_form = ZonaForm() # Limpiar el input del form cuando se muestra.
            else:
                messages.error(request, mensaje_error)

        elif form_type == 'accion':
            accion_form = ProximaAccionForm(request.POST)

            if accion_form.is_valid():
                accion_form.save()
                messages.success(request, mensaje_exito)
                accion_form = ProximaAccionForm()
            else:
                messages.error(request, mensaje_error)

        elif form_type == 'estado':
            estado_form = EstadoObraForm(request.POST)

            if estado_form.is_valid():
                estado_form.save()
                messages.success(request, mensaje_exito)
                estado_form = EstadoObraForm() 
            else:
                messages.error(request, mensaje_error)
    
    zonas_cargadas = Zona.objects.all().order_by('localidad')
    acciones_cargadas = ProximaAccion.objects.all().order_by('accion')
    estados_cargados = EstadoObra.objects.all().order_by('estado')

    contexto = {'zona_form': zona_form, 
                'accion_form': accion_form, 
                'estado_form': estado_form, 
                'zonas_cargadas':zonas_cargadas, 
                'acciones_cargadas': acciones_cargadas, 
                'estados_cargados': estados_cargados
                }
    return render(request, 'ajustes.html', contexto)