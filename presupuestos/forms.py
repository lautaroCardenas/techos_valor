from django import forms
from .models import Presupuesto

class PresupuestoForm(forms.ModelForm):
    class Meta:
        model = Presupuesto
        fields = ['metro_2', 'precio_metro', 'material', 'superficie', 'obra', 'observacion', 'recargo_porcentaje', 'descripcion_impresa', 'aceptado']

    def clean_metro_2(self):
        metro_2 = self.cleaned_data.get('metro_2')
        if metro_2 <= 0:
            raise forms.ValidationError("Los metros no pueden ser valores negativos")
        return metro_2

    def clean_precio_metro(self):
        precio_metro = self.cleaned_data.get('precio_metro')

        if precio_metro < 0:
            raise forms.ValidationError("El precio no puede ser menor a 0")
        return precio_metro