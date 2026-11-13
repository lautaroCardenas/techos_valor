from django import forms
from obras.models import Obra
from .models import Presupuesto

class PresupuestoForm(forms.ModelForm):
    class Meta:
        model = Presupuesto
        fields = ['metro_2', 'precio_metro', 'material', 'superficie', 'obra', 'observacion', 'recargo_porcentaje', 'descripcion_impresa', 'aceptado']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # El texto de cada opción (Obra.__str__) usa cliente, zona y estado:
        # se traen en la misma consulta para no hacer una por obra.
        self.fields['obra'].queryset = Obra.objects.select_related('cliente', 'zona', 'estado')
