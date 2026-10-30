from django import forms
from .models import Obra, Cliente

class ObraForm(forms.ModelForm):

    fecha_visita = forms.DateField(required=False, label="Fecha de visita", widget=forms.DateInput(attrs={'type':'date'}))

    class Meta:
        model = Obra
        fields = ['cliente', 'direccion', 'zona', 'observacion', 'negocio', 'estado', 'garantia', 'proxima_accion']

class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ['nombre', 'apellido', 'telefono']