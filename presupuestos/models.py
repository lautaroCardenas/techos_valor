from django.db import models

# Create your models here.

MATERIAL = [
    ("aluminio", "Aluminio"),
    ("antitermico", "Antitermico"),
    ("geo_pintura", "Geotextil Pintura"),
    ("geo_mordiente", "Geotextil Mordiente")
]

SUPERFICIE = [
    ("losa", "Losa"),
    ("chapa", "Chapa")
]

class Presupuesto(models.Model):
    aceptado = models.BooleanField(default=False)
    fecha_actual = models.DateTimeField(auto_now=True) # Se va a actualizar con cada actualizacion. Para que sea una sola vez al crearse sería: auto_now_add=True.
    metro_2 = models.DecimalField(max_digits=10, decimal_places=3)
    precio_metro = models.DecimalField(max_digits=10, decimal_places=3)
    material = models.CharField(max_length=20, choices=MATERIAL)
    superficie = models.CharField(max_length=20, choices=SUPERFICIE)
    observacion = models.TextField(blank=True)
    recargo_porcentaje = models.DecimalField(max_digits=10, decimal_places=3, default=0)
    descripcion_impresa = models.TextField(blank=True)
    obra = models.ForeignKey("obras.Obra", on_delete=models.RESTRICT) # Si el presupuesto se rechaza y se realiza uno nuevo, cada obra tendra mas de un presupuesto.
    monto = models.DecimalField(max_digits=10, decimal_places=3)

    def save(self, *args, **kwargs):
        subtotal = self.precio_metro * self.metro_2
        self.monto = subtotal + (subtotal * self.recargo_porcentaje / 100)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Superficie: {self.superficie} - Material: {self.material} - Precio m2: {self.precio_metro} - Aceptado: {self.aceptado}"

    class Meta:
        ordering = ["fecha_actual", "obra"]
        verbose_name = "Presupuesto"
        verbose_name_plural = "Presupuestos"