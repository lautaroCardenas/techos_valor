from django import forms
from django.utils import timezone
from .models import Evento


class EventoForm(forms.ModelForm):
    class Meta:
        model = Evento
        fields = ["titulo", "fecha", "tipo", "estado", "descripcion", "obra"]
        widgets = {
            "fecha": forms.DateTimeInput(
                attrs={"type": "datetime-local"},
                format="%Y-%m-%dT%H:%M",
            ),
        }

    def clean_fecha(self):
        fecha = self.cleaned_data["fecha"]
        # Solo exigir fecha futura si es nuevo o si se cambió la fecha.
        if (not self.instance.pk or "fecha" in self.changed_data) and fecha <= timezone.now():
            raise forms.ValidationError("La fecha debe ser posterior al momento actual.")
        return fecha