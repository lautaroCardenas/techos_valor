from django import forms
from .models import Pagos

class PagosForm(forms.ModelForm):
    class Meta:
        model = Pagos
        fields = ['numero', 'monto_pagado', 'comision_porcentaje']
