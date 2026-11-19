import base64
from decimal import Decimal

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.db.models.functions import Lower


PORCENTAJE = [MinValueValidator(Decimal("0")), MaxValueValidator(Decimal("100"))]


class Material(models.Model):
    """Material que se ofrece al presupuestar. El precio se copia a cada
    ItemPresupuesto, así que cambiarlo acá no altera presupuestos viejos."""
    nombre = models.CharField(max_length=100)
    precio_m2 = models.DecimalField(
        "precio por m²", max_digits=12, decimal_places=2,
        validators=[MinValueValidator(Decimal("0"))])
    activo = models.BooleanField(
        default=True,
        help_text="Desmarcar para que no aparezca al cargar nuevos presupuestos.")

    class Meta:
        verbose_name = "material"
        verbose_name_plural = "materiales"
        ordering = ["nombre"]
        constraints = [
            models.UniqueConstraint(
                Lower("nombre"), name="material_nombre_unico",
                violation_error_message="Ya existe un material con ese nombre."),
        ]

    def __str__(self):
        return self.nombre


class Zona(models.Model):
    """Localidad donde se hace la obra."""
    localidad = models.CharField(max_length=100)
    activo = models.BooleanField(
        default=True,
        help_text="Desmarcar para que no aparezca al cargar nuevas obras.")

    class Meta:
        verbose_name = "zona"
        verbose_name_plural = "zonas"
        ordering = ["localidad"]
        constraints = [
            models.UniqueConstraint(
                Lower("localidad"), name="zona_localidad_unica",
                violation_error_message="Ya existe una zona con ese nombre."),
        ]

    def __str__(self):
        return self.localidad


class Configuracion(models.Model):
    """Parámetros globales del sistema. Existe un único registro (pk = 1)."""
    porcentaje_comision = models.DecimalField(
        "porcentaje de comisión", max_digits=5, decimal_places=2,
        default=Decimal("10"), validators=PORCENTAJE,
        help_text="Porcentaje sobre el total cuando la obra viene de un tercero.")
    recargo_no_efectivo = models.DecimalField(
        "recargo por pago no efectivo", max_digits=5, decimal_places=2,
        default=Decimal("0"), validators=PORCENTAJE,
        help_text="Porcentaje adicional si el pago no es en efectivo.")
    template_presupuesto = models.TextField(
        "template del presupuesto", blank=True,
        help_text="Texto base del presupuesto que se envía al cliente.")
    actualizado = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "configuración"
        verbose_name_plural = "configuración"

    def __str__(self):
        return "Configuración del sistema"

    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)

    @classmethod
    def obtener(cls):
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj


ENCABEZADO_PDF_DEFAULT = (
    "Tel. (1):  221 434-7167\n"
    "Tel. (2):  221 505-5637\n"
    "(1900) La Plata - Pcia. de Bs. As."
)

CONDICIONES_PDF_DEFAULT = (
    "*Incluye todos los materiales necesarios y la mano de obra.*\n"
    "*No incluye factura, el precio es en efectivo.*\n"
    "Otros medios de pago tienen recargo.\n"
    "*Garantía escrita.*\n"
    "\n"
    "50% para confirmar el presupuesto y el resto al finalizar la obra."
)


class ConfiguracionPDF(models.Model):
    """Cómo se ve el PDF de los presupuestos. Existe un único registro (pk = 1)."""

    # El logo se guarda en la base (no como archivo) para que no se pierda al
    # hacer deploy en hostings que borran los archivos subidos.
    logo = models.BinaryField("logo", null=True, blank=True, editable=False)
    logo_tipo = models.CharField(max_length=50, blank=True, editable=False)

    encabezado = models.TextField(
        "datos de la empresa", blank=True, default=ENCABEZADO_PDF_DEFAULT,
        help_text="Se muestran arriba a la derecha. Una línea por renglón.")
    titulo = models.CharField("título", max_length=60, default="PRESUPUESTO")
    prefijo_numero = models.CharField(
        "prefijo del número", max_length=10, blank=True, default="P",
        help_text='Va delante del número de presupuesto, por ejemplo "P" para P486.')

    mostrar_telefono_cliente = models.BooleanField("mostrar teléfono del cliente", default=True)
    mostrar_localidad = models.BooleanField("mostrar localidad junto al domicilio", default=True)
    mostrar_superficies = models.BooleanField(
        "mostrar casillas de superficie", default=True,
        help_text="Las opciones (Chapa, Losa...) con la del presupuesto marcada.")
    mostrar_desglose = models.BooleanField(
        "mostrar desglose del precio", default=False,
        help_text="Material, m², precio por m² y recargo, además del total.")
    mostrar_observaciones = models.BooleanField("mostrar observaciones", default=True)

    condiciones = models.TextField(
        "condiciones / pie", blank=True, default=CONDICIONES_PDF_DEFAULT,
        help_text="Se muestran al final. Escribí una línea entre *asteriscos* para ponerla en cursiva.")

    actualizado = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "configuración del PDF"
        verbose_name_plural = "configuración del PDF"

    def __str__(self):
        return "Configuración del PDF"

    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)

    @classmethod
    def obtener(cls):
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj

    @property
    def logo_data_uri(self):
        """El logo como data URI para usarlo en <img src> (en la página y en el PDF)."""
        if not self.logo:
            return ""
        return f"data:{self.logo_tipo};base64,{base64.b64encode(bytes(self.logo)).decode()}"
