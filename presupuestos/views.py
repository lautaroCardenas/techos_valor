from django.shortcuts import render
from .models import Presupuesto

# Create your views here.
def presupuestos_total(request):
    return render(request, 'presupuestos/presupuestos.html')

def presupuesto_detalle(request, pk):
    try:
        pres = Presupuesto.objects.get(pk=pk)
        return render(request, 'presupuestos/presupuesto_detalle.html', {'presupuesto': pres})
    except:
        return render(request, 'not_found.html')