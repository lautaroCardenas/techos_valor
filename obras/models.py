from django.db import models
from servicios.validadores import solo_letras, valores_positivos

# Create your models here.

class Zona(models.Model):
    localidad = models.CharField(max_length=50, validators=[solo_letras])

    def __str__(self):
        return self.localidad

class Cliente(models.Model):
    nombre = models.CharField(max_length=50, validators=[solo_letras])
    apellido = models.CharField(max_length=50, validators=[solo_letras])
    telefono = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.nombre} {self.apellido} - {self.telefono}"

class FechaVisita(models.Model):
    numero = models.IntegerField(null=True, validators=[valores_positivos])
    fecha = models.DateField()

    def __str__(self):
        return f"{self.numero} - {self.fecha}"

class EstadoObra(models.Model):
    estado = models.CharField(max_length=25, validators=[solo_letras])

    def __str__(self):
        return self.estado

class ProximaAccion(models.Model):
    accion = models.CharField(max_length=25, validators=[solo_letras])

    def __str__(self):
        return self.accion

class Obra(models.Model):
    direccion = models.CharField(max_length=100)
    fecha_contacto = models.DateField(auto_now_add=True)
    observacion = models.TextField(blank=True)
    negocio = models.BooleanField(default=True)
    zona = models.ForeignKey(Zona, on_delete=models.RESTRICT) 
    cliente = models.ForeignKey(Cliente, on_delete=models.RESTRICT)  
    estado = models.ForeignKey(EstadoObra, on_delete=models.SET_NULL, null=True)
    garantia = models.BooleanField(default=True)
    proxima_accion = models.ForeignKey(ProximaAccion, on_delete=models.SET_NULL, null=True, blank=True)
    fecha_visita = models.ForeignKey(FechaVisita, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        ordering = ["cliente", "fecha_contacto"]
        verbose_name = "Obra"
        verbose_name_plural = "Obras"

    def __str__(self):
        return (f"{self.cliente.nombre} {self.cliente.apellido} - "
                f"Direccion: {self.direccion} | {self.zona.localidad}"
                f"Estado: {self.estado}")