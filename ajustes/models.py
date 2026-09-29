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
