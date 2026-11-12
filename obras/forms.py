from django import forms
from django.utils import timezone
from .models import Obra, Cliente

class ObraForm(forms.ModelForm):

    fecha_visita = forms.DateField(required=False, label="Fecha de visita", widget=forms.DateInput(attrs={'type':'date'}))

    class Meta:
        model = Obra
        fields = ['cliente', 'direccion', 'zona', 'observacion', 'negocio', 'estado', 'garantia', 'proxima_accion']
    
    def clean_fecha_visita(self):
        fecha = self.cleaned_data.get('fecha_visita')

        if fecha and fecha < timezone.localdate():
            raise forms.ValidationError(
                "La fecha de visita no puede ser anterior a la fecha actual."
            )

        return fecha

class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ['nombre', 'apellido', 'telefono']
    def clean_nombre(self):
        nombre = self.cleaned_data['nombre'].strip()

        if not nombre.replace(" ", "").isalpha():
            raise forms.ValidationError(
                "El nombre solo puede contener letras."
            )

        return nombre

    def clean_apellido(self):
        apellido = self.cleaned_data['apellido'].strip()

        if not apellido.replace(" ", "").isalpha():
            raise forms.ValidationError(
                "El apellido solo puede contener letras."
            )

        return apellido

    def clean_telefono(self):
        telefono = self.cleaned_data['telefono'].strip()

        if not telefono.isdigit():
            raise forms.ValidationError(
                "El teléfono solo puede contener números."
            )

        if len(telefono) < 8 or len(telefono) > 20:
            raise forms.ValidationError(
                "El teléfono debe tener entre 8 y 20 dígitos."
            )

        return telefono