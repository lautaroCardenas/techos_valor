from django import forms
from obras.models import Zona, ProximaAccion, EstadoObra
from presupuestos.models import Material, Superficie

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

class MaterialForm(forms.ModelForm):
    class Meta:
        model = Material
        fields = ['material']

class SuperficieForm(forms.ModelForm):
    class Meta:
        model = Superficie
        fields = ['superficie']