from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from django.utils import timezone
from django.utils.dateparse import parse_datetime
from django.views.decorators.http import require_POST
from .forms import EventoForm
from .models import Evento

# Create your views here.
def agenda(request):
    return render(request, 'agenda/agenda.html', {"form": EventoForm()})

def agenda_eventos(request): # Carga todos los eventos registrados.
    inicio = parse_datetime(request.GET.get("start", ""))
    fin = parse_datetime(request.GET.get("end", ""))

    evento_bd = (Evento.objects.filter(fecha__gte=inicio, fecha__lt=fin).select_related("tipo", "estado", "obra"))

    data = []

    for e in evento_bd:
        local = timezone.localtime(e.fecha)
        data.append({ # En el formato en que lo recibe FullCalendar.
            "id": e.id,
            "title": e.titulo,
            "start": local.replace(tzinfo=None).isoformat(),
            "color": e.tipo.color if e.tipo else "#1170b8",
            "classNames": [f"estado-{e.estado.estado.lower()}"] if e.estado else [],
            "extendedProps": {
                "fecha": local.strftime("%Y-%m-%dT%H:%M"),
                "tipo": e.tipo_id,
                "estado": e.estado_id,
                "obra": e.obra_id,
                "descripcion": e.descripcion,
            },
        })
    return JsonResponse(data, safe=False)

def _errores(form):
    return JsonResponse({"ok": False, "errors": form.errors.get_json_data()}, status=400)

def evento_crear(request):
    if request.method == 'POST':
        form = EventoForm(request.POST)

        if form.is_valid():
            evento = form.save()
            return JsonResponse({"ok": True, "id": evento.id})
        return _errores(form)

def evento_editar(request, pk):
    if request.method == 'POST':
        evento = get_object_or_404(Evento, pk=pk)
        form = EventoForm(request.POST, instance=evento)

        if form.is_valid():
            form.save()
            return JsonResponse({"ok": True})
        return _errores(form)

def evento_borrar(request, pk):
    if request.method == 'POST':
        evento = get_object_or_404(Evento, pk=pk)
        evento.delete()
        return JsonResponse({"ok": True})

def evento_mover(request, pk):
    if request.method == 'POST':
        evento = get_object_or_404(Evento, pk=pk)
        nueva = parse_datetime(request.POST.get("fecha", ""))
        if nueva is None:
            return JsonResponse({"ok": False, "error": "Fecha inválida."}, status=400)
        if timezone.is_naive(nueva):
            nueva = timezone.make_aware(nueva)  # la interpreta en America/Argentina/Buenos_Aires
        if nueva <= timezone.now():
            return JsonResponse(
                {"ok": False, "error": "La fecha debe ser posterior al momento actual."},
                status=400,
            )
        evento.fecha = nueva
        evento.save(update_fields=["fecha"])
        return JsonResponse({"ok": True})
