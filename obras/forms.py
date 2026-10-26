from django import forms
from .models import Obra

class ObraForm(forms.ModelForm):
    class Meta:
        model = Obra
        fields = ['cliente', 'direccion', 'zona', 'observacion', 'negocio', 'estado', 'garantia', 'proxima_accion', 'fecha_visita']