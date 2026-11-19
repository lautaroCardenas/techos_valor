from django.shortcuts import render, get_object_or_404, redirect
from .forms import ZonaForm, ProximaAccionForm, EstadoObraForm, MaterialForm, SuperficieForm, ConfiguracionPDFForm
from .models import ConfiguracionPDF
from django.http import HttpResponse
from django.utils import timezone
from obras.models import Cliente, Obra
from presupuestos.models import Presupuesto
from presupuestos.pdf import generar_pdf_presupuesto
from django.contrib import messages
from obras.models import Zona, ProximaAccion, EstadoObra
from presupuestos.models import Material, Superficie

# Create your views here.
mensaje_exito = 'El dato se guardó correctamente'
mensaje_error = 'No se pudo guardar el dato'
EXTRA_TAGS = 'ajustes_messages'

def ajustes(request):
    zona_form = ZonaForm()
    accion_form = ProximaAccionForm()
    estado_form = EstadoObraForm()
    material_form = MaterialForm()
    superficie_form = SuperficieForm()

    if request.method == "POST":
        form_type = request.POST.get('form_type')
        if form_type == 'zona':
            zona_form = ZonaForm(request.POST)

            if zona_form.is_valid():
                zona_form.save()
                messages.success(request, mensaje_exito, extra_tags=EXTRA_TAGS)
                zona_form = ZonaForm() # Limpiar el input del form cuando se muestra.
            else:
                messages.error(request, mensaje_error, extra_tags=EXTRA_TAGS)

        elif form_type == 'accion':
            accion_form = ProximaAccionForm(request.POST)

            if accion_form.is_valid():
                accion_form.save()
                messages.success(request, mensaje_exito, extra_tags=EXTRA_TAGS)
                accion_form = ProximaAccionForm()
            else:
                messages.error(request, mensaje_error, extra_tags=EXTRA_TAGS)

        elif form_type == 'estado':
            estado_form = EstadoObraForm(request.POST)

            if estado_form.is_valid():
                estado_form.save()
                messages.success(request, mensaje_exito, extra_tags=EXTRA_TAGS)
                estado_form = EstadoObraForm() 
            else:
                messages.error(request, mensaje_error, extra_tags=EXTRA_TAGS)

        elif form_type == 'material':
            material_form = MaterialForm(request.POST)

            if material_form.is_valid():
                material_form.save()
                messages.success(request, mensaje_exito, extra_tags=EXTRA_TAGS)
                material_form = MaterialForm()
            else:
                messages.error(request, mensaje_error, extra_tags=EXTRA_TAGS)
        
        elif form_type == 'superficie':
            superficie_form = SuperficieForm(request.POST)

            if superficie_form.is_valid():
                superficie_form.save()
                messages.success(request, mensaje_exito, extra_tags=EXTRA_TAGS)
                superficie_form = SuperficieForm()
            else:
                messages.error(request, mensaje_error, extra_tags=EXTRA_TAGS)

    zonas_cargadas = Zona.objects.all().order_by('localidad')
    acciones_cargadas = ProximaAccion.objects.all().order_by('accion')
    estados_cargados = EstadoObra.objects.all().order_by('estado')
    materiales_cargados = Material.objects.all().order_by('material')
    superficies_cargadas = Superficie.objects.all().order_by('superficie')

    contexto = {'zona_form': zona_form, 
                'accion_form': accion_form, 
                'estado_form': estado_form, 
                'material_form': material_form,
                'superficie_form': superficie_form,
                'zonas_cargadas':zonas_cargadas, 
                'acciones_cargadas': acciones_cargadas, 
                'estados_cargados': estados_cargados,
                'materiales_cargados': materiales_cargados,
                'superficies_cargadas': superficies_cargadas
                }
    return render(request, 'ajustes.html', contexto)

def ajustes_borrar(request, tipo, pk):
    modelos = {
        'zona': Zona,
        'accion': ProximaAccion,
        'estado': EstadoObra,
        'material': Material,
        'superficie': Superficie,
    }

    modelo = modelos.get(tipo)

    if modelo is None:
        messages.error(request, 'Tipo de dato inválido.', extra_tags=EXTRA_TAGS)
        return redirect('ajustes:ajustes')
    
    elemento = get_object_or_404(modelo, pk=pk)

    try:
        elemento.delete()
        messages.success(request, f'El item se eliminó correctamente.', extra_tags=EXTRA_TAGS)
    except:
        messages.error(
            request,
            f'No se puede eliminar el item porque está siendo utilizado.',
            extra_tags=EXTRA_TAGS
        )

    return redirect('ajustes:ajustes')


def ajustes_pdf(request):
    config = ConfiguracionPDF.obtener()

    if request.method == 'POST':
        form = ConfiguracionPDFForm(request.POST, request.FILES, instance=config)
        if form.is_valid():
            form.save()
            messages.success(request, 'La configuración del PDF se guardó correctamente.', extra_tags=EXTRA_TAGS)
            return redirect('ajustes:ajustes_pdf')
        messages.error(request, 'Revisá los datos marcados.', extra_tags=EXTRA_TAGS)
    else:
        form = ConfiguracionPDFForm(instance=config)

    return render(request, 'ajustes/pdf.html', {'form': form, 'config': config})


def ajustes_pdf_vista_previa(request):
    """El PDF con la configuración guardada, usando el último presupuesto (o uno de ejemplo)."""
    pres = Presupuesto.objects.select_related(
        'material', 'superficie', 'obra__cliente', 'obra__zona'
    ).order_by('-pk').first()

    if pres is None:
        # Sin presupuestos cargados: uno de ejemplo que no se guarda en la base.
        pres = Presupuesto(
            pk=0, metro_2=100, precio_metro=48600, monto=4860000, recargo_porcentaje=0,
            material=Material(material='Membrana'),
            descripcion_impresa='Ejemplo de descripción del trabajo.',
            observacion='Ejemplo de observaciones.',
            obra=Obra(
                direccion='455 y 132', zona=Zona(localidad='La Plata'),
                cliente=Cliente(nombre='Cliente', apellido='de ejemplo', telefono='221 000-0000'),
            ),
        )
        pres.fecha_actual = timezone.now()

    pdf = generar_pdf_presupuesto(pres)
    if pdf is None:
        return HttpResponse('No se pudo generar la vista previa del PDF.', status=500)
    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename="vista-previa.pdf"'
    return response
