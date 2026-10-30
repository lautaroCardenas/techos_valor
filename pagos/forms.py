from django import forms
from django.core.exceptions import ValidationError
from .models import Pagos

class PagosForm(forms.ModelForm):
    def __init__(self, *args, presupuesto=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.presupuesto = presupuesto

        if presupuesto and presupuesto.obra.negocio:
            self.fields['comision_porcentaje'].required = True
            self.fields['comision_porcentaje'].error_messages['required'] = (
                'Indicá el porcentaje de comisión para esta obra.'
            )

    def clean_comision_porcentaje(self):
        porcentaje = self.cleaned_data.get('comision_porcentaje')
        if self.presupuesto and self.presupuesto.obra.negocio and not porcentaje:
            raise ValidationError(
                'El porcentaje de comisión debe ser mayor que cero para esta obra.'
            )
        return porcentaje

    class Meta:
        model = Pagos
        fields = ['numero', 'monto_pagado', 'comision_porcentaje']
