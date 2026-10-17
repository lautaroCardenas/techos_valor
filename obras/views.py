from django.shortcuts import render
from .models import Obra

# Create your views here.
def obras_total(request):
    return render(request, 'obras/obras.html')

def obra_detalle(request, pk):
    try:
        obra = Obra.objects.get(pk=pk)
        return render(request, 'obras/obra_detalle.html', {'obra': obra})
    except: # Si no encuentra la obra con el id ingresado como parámetro, retorna un template de not found.
        return render(request, 'not_found.html')
    