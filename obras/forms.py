from django import forms
from .models import Obra, Cliente

class ObraForm(forms.ModelForm):
    class Meta:
        model = Obra
        fields = ['cliente', 'direccion', 'zona', 'observacion', 'negocio', 'estado', 'garantia', 'proxima_accion', 'fecha_visita']

class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ['nombre', 'apellido', 'telefono']