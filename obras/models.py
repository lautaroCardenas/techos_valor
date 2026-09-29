from django.db import models

# Create your models here.

class Zona(models.Model):
    localidad = models.CharField(max_length=50)

    def __str__(self):
        return self.localidad

class Cliente(models.Model):
    nombre = models.CharField(max_length=50)
    apellido = models.CharField(max_length=50)
    telefono = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.nombre} {self.apellido} - {self.telefono}"

class FechaVisita(models.Model):
    numero = models.IntegerField(null=True)
    fecha = models.DateField()

    def __str__(self):
        return f"{self.numero} - {self.fecha}"

# ESTADO_OBRA = [
#     ("medir", "Medir"),
#     ("visitar", "Visitar"),
#     ("hacer", "Hacer"),
#     ("reclamo", "Reclamo"),
#     ("completado", "Completado")
# ]
class EstadoObra(models.Model):
    estado = models.CharField(max_length=25)

    def __str__(self):
        return self.estado

# PROXIMA_ACCION = [
#     ("llamar", "Llamar"),
#     ("medir", "Medir"),
#     ("presupuesto", "Presupuesto"),
#     ("cobrar", "Cobrar"),
#     ("adelanto", "Adelanto")
# ]
class ProximaAccion(models.Model):
    accion = models.CharField(max_length=25)

    def __str__(self):
        return self.accion

class Obra(models.Model):
    direccion = models.CharField(max_length=100)
    fecha_contacto = models.DateField(auto_now_add=True)
    observacion = models.TextField(blank=True)
    negocio = models.BooleanField(default=True)
    zona = models.ForeignKey(Zona, on_delete=models.RESTRICT) 
    cliente = models.ForeignKey(Cliente, on_delete=models.RESTRICT)  
    # estado = models.CharField(max_length=50, choices=ESTADO_OBRA, null=True, blank=True)
    estado = models.ForeignKey(EstadoObra, on_delete=models.SET_NULL, null=True)
    garantia = models.BooleanField(default=True)
    # proxima_accion = models.CharField(max_length=50, choices=PROXIMA_ACCION, null=True, blank=True)
    proxima_accion = models.ForeignKey(ProximaAccion, on_delete=models.SET_NULL, null=True)
    fecha_visita = models.ForeignKey(FechaVisita, on_delete=models.RESTRICT)

    class Meta:
        ordering = ["cliente", "fecha_contacto"]
        verbose_name = "Obra"
        verbose_name_plural = "Obras"

    def __str__(self):
        return (f"{self.cliente.nombre} {self.cliente.apellido} - "
                f"Direccion: {self.direccion} | {self.zona.localidad}"
                f"Estado: {self.estado}")