from django.shortcuts import render
from .models import Obra
from django.db.models import Q

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
    