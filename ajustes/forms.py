from django import forms
from obras.models import Zona, ProximaAccion, EstadoObra

class ZonaForm(forms.ModelForm):
    class Meta:
        model = Zona
        fields = ['localidad']

class ProximaAccionForm(forms.ModelForm):
    class Meta:
        model = ProximaAccion
        fields = ['accion']

class EstadoObraForm(forms.ModelForm):
    class Meta:
        model = EstadoObra
        fields = ['estado'] 