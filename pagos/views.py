from django.shortcuts import render
from .models import Pagos

# Create your views here.
def pagos_total(request):
    return render(request, 'pagos/pagos.html')

def pago_detalle(request, pk):
    try:
        pago = Pagos.objects.get(pk=pk)
        return render(request, 'pagos/pago_detalle.html', {'pago':pago})
    except:
        return render(request, 'not_found.html')
    
