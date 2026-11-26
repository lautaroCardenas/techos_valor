from django import forms
from django.utils import timezone
from .models import Obra, Cliente, FechaVisita
from django.forms import inlineformset_factory  

class ObraForm(forms.ModelForm):

    class Meta:
        model = Obra
        fields = ['cliente', 'direccion', 'zona', 'observacion', 'negocio', 'estado', 'garantia', 'proxima_accion', 'fecha_inicio', 'fecha_fin']
        widgets =  {'fecha_inicio': forms.DateInput(attrs={'type':'date'}), 'fecha_fin': forms.DateInput(attrs={'type':'date'})}

    def clean(self):
        cleaned_data = super().clean()

        fecha_inicio = cleaned_data.get('fecha_inicio')
        fecha_fin = cleaned_data.get('fecha_fin')

        if fecha_inicio and fecha_fin and fecha_fin < fecha_inicio:
            self.add_error(
                'fecha_fin',
                'La fecha de finalización no puede ser anterior a la fecha de inicio.'
            )

        return cleaned_data

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

class FechaVisitaForm(forms.ModelForm):
    class Meta:
        model = FechaVisita
        fields = ['fecha']
        widgets= {'fecha': forms.DateInput(attrs={'type':'date'})}

    def clean_fecha(self):
        fecha = self.cleaned_data.get('fecha')

        if fecha and fecha < timezone.localdate():
            raise forms.ValidationError(
                "La fecha de visita no puede ser anterior a la fecha actual."
            )

        return fecha

FechaVisitaFormSet = inlineformset_factory(
    Obra,
    FechaVisita, 
    form=FechaVisitaForm, 
    extra=1,
    can_delete=True
)