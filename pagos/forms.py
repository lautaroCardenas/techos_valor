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

    def clean_monto_pagado(self):
        monto_pagado = self.cleaned_data.get('monto_pagado')
        if monto_pagado < 0:
            raise ValidationError("El monto pagado no puede ser menor a 0")
        
        
        return monto_pagado

    def clean_numero(self):
        numero = self.cleaned_data.get('numero')
        if numero < 0:
            raise ValidationError("El número de pago no puede ser menor a 0")
        return numero

