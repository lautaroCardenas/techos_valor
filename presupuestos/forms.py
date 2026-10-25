from django import forms
from .models import Presupuesto

class PresupuestoForm(forms.ModelForm):
    class Meta:
        model = Presupuesto
        fields = ['metro_2', 'precio_metro', 'material', 'superficie', 'obra', 'observacion', 'recargo_porcentaje', 'descripcion_impresa']