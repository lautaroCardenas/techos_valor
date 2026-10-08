from django.db import models
from servicios.validadores import solo_letras, valores_positivos

# Create your models here.

class Material(models.Model):
    material = models.CharField(max_length = 25, validators=[solo_letras])

    def __str__(self):
        return self.material

class Superficie(models.Model):
    superficie = models.CharField(max_length = 25, validators=[solo_letras])

    def __str__(self):
        return self.superficie

class Presupuesto(models.Model):
    aceptado = models.BooleanField(default=False)
    fecha_actual = models.DateTimeField(auto_now=True) # Se va a actualizar con cada actualizacion. Para que sea una sola vez al crearse sería: auto_now_add=True.
    metro_2 = models.DecimalField(max_digits=10, decimal_places=3, validators=[valores_positivos])
    precio_metro = models.DecimalField(max_digits=10, decimal_places=3, validators=[valores_positivos])
    material = models.ForeignKey(Material, on_delete=models.RESTRICT)
    superficie = models.ForeignKey(Superficie, on_delete=models.RESTRICT)
    observacion = models.TextField(blank=True)
    recargo_porcentaje = models.DecimalField(max_digits=10, decimal_places=3, default=0, validators=[valores_positivos])
    descripcion_impresa = models.TextField(blank=True)
    obra = models.ForeignKey("obras.Obra", on_delete=models.RESTRICT) # Si el presupuesto se rechaza y se realiza uno nuevo, cada obra tendra mas de un presupuesto.
    monto = models.DecimalField(max_digits=10, decimal_places=3, validators=[valores_positivos])

    def save(self, *args, **kwargs):
        subtotal = self.precio_metro * self.metro_2
        self.monto = subtotal + (subtotal * self.recargo_porcentaje / 100)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Cliente: {self.obra.cliente.nombre} {self.obra.cliente.apellido} - Monto: {self.monto} - Aceptado: {self.aceptado}"

    class Meta:
        ordering = ["fecha_actual", "obra"]
        verbose_name = "Presupuesto"
        verbose_name_plural = "Presupuestos"