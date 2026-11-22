from django import forms
from obras.models import Obra
from .models import Presupuesto, DescripcionPredeterminada

class PresupuestoForm(forms.ModelForm):
    guardar_como_predeterminada = forms.BooleanField(
        required=False,
        label="Guardar esta descripción como predeterminada para este material y superficie",
    )

    class Meta:
        model = Presupuesto
        # guardar_como_predeterminada no es del modelo: se lista acá solo para que
        # aparezca justo debajo de la descripción en los formularios con as_p.
        fields = ['metro_2', 'precio_metro', 'material', 'superficie', 'obra', 'observacion', 'recargo_porcentaje', 'descripcion_impresa', 'guardar_como_predeterminada', 'aceptado']

    def clean_metro_2(self):
        metro_2 = self.cleaned_data.get('metro_2')
        if metro_2 <= 0:
            raise forms.ValidationError("Los metros no pueden ser valores negativos")
        return metro_2

    def clean_precio_metro(self):
        precio_metro = self.cleaned_data.get('precio_metro')

        if precio_metro < 0:
            raise forms.ValidationError("El precio no puede ser menor a 0")
        return precio_metro

    def clean(self):
        cleaned_data = super().clean()
        material = cleaned_data.get('material')
        superficie = cleaned_data.get('superficie')

        # Respaldo por si el JS no completó la descripción (sin JS, o el formulario que
        # vuelve de la sesión al crear una obra). Solo al crear: al editar, una
        # descripción vacía puede ser intencional y no se pisa.
        if (self.instance.pk is None and material and superficie
                and not cleaned_data.get('descripcion_impresa', '').strip()):
            predeterminada = DescripcionPredeterminada.objects.filter(
                material=material, superficie=superficie
            ).first()
            if predeterminada:
                cleaned_data['descripcion_impresa'] = predeterminada.texto

        return cleaned_data

    def save(self, commit=True):
        presupuesto = super().save(commit=commit)
        texto = self.cleaned_data.get('descripcion_impresa', '').strip()

        if self.cleaned_data.get('guardar_como_predeterminada') and texto:
            DescripcionPredeterminada.objects.update_or_create(
                material=presupuesto.material,
                superficie=presupuesto.superficie,
                defaults={'texto': self.cleaned_data['descripcion_impresa']},
            )
        return presupuesto

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # El texto de cada opción (Obra.__str__) usa cliente, zona y estado:
        # se traen en la misma consulta para no hacer una por obra.
        self.fields['obra'].queryset = Obra.objects.select_related('cliente', 'zona', 'estado')
