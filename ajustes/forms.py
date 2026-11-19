from django import forms
from obras.models import Zona, ProximaAccion, EstadoObra
from presupuestos.models import Material, Superficie
from .models import ConfiguracionPDF

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

class ConfiguracionPDFForm(forms.ModelForm):
    LOGO_MAX_BYTES = 1024 * 1024  # 1 MB
    TIPOS_PERMITIDOS = {'PNG': 'image/png', 'JPEG': 'image/jpeg'}

    logo_nuevo = forms.ImageField(
        label='Logo', required=False,
        help_text='PNG o JPG, hasta 1 MB. Si no subís ninguno se usa el logo de Techos Valor.')
    quitar_logo = forms.BooleanField(
        label='Volver al logo de Techos Valor', required=False)

    class Meta:
        model = ConfiguracionPDF
        fields = [
            'encabezado', 'titulo', 'prefijo_numero',
            'mostrar_telefono_cliente', 'mostrar_localidad', 'mostrar_superficies',
            'mostrar_desglose', 'mostrar_observaciones', 'condiciones',
        ]
        widgets = {
            'encabezado': forms.Textarea(attrs={'rows': 4}),
            'condiciones': forms.Textarea(attrs={'rows': 7}),
        }

    def clean_logo_nuevo(self):
        archivo = self.cleaned_data.get('logo_nuevo')
        if not archivo:
            return None
        if archivo.size > self.LOGO_MAX_BYTES:
            raise forms.ValidationError('El logo no puede pesar más de 1 MB.')
        # ImageField ya verificó que sea una imagen válida; el PDF solo acepta PNG y JPG.
        formato = getattr(archivo, 'image', None) and archivo.image.format
        if formato not in self.TIPOS_PERMITIDOS:
            raise forms.ValidationError('El logo tiene que ser PNG o JPG.')
        archivo.tipo_mime = self.TIPOS_PERMITIDOS[formato]
        return archivo

    def save(self, commit=True):
        config = super().save(commit=False)
        archivo = self.cleaned_data.get('logo_nuevo')
        if archivo:
            archivo.seek(0)
            config.logo = archivo.read()
            config.logo_tipo = archivo.tipo_mime
        elif self.cleaned_data.get('quitar_logo'):
            config.logo = None
            config.logo_tipo = ''
        if commit:
            config.save()
        return config
