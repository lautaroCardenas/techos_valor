from django.db import models
from servicios.validadores import solo_letras, fecha_futura

# Create your models here.

class TipoEvento(models.Model):
    tipo = models.TextField(max_length=20, validators=[solo_letras])

    class Meta:
        verbose_name = "tipo de evento"
        verbose_name_plural = "tipos de evento"

    def __str__(self):
        return self.tipo

class EstadoEvento(models.Model):
    estado = models.TextField(max_length=20, validators=[solo_letras])

    class Meta:
        verbose_name = "estado de evento"
        verbose_name_plural = "estados de evento"

    def __str__(self):
        return self.estado

class Evento(models.Model):
    titulo = models.CharField(max_length=50)
    fecha = models.DateTimeField(db_index=True)
    tipo = models.ForeignKey(TipoEvento, on_delete=models.SET_NULL, blank=True, null=True, unique=True)
    estado = models.ForeignKey(EstadoEvento, on_delete=models.SET_NULL, blank=True, null=True, unique=True)
    descripcion = models.TextField(blank=True)
    obra = models.ForeignKey("obras.Obra", on_delete=models.SET_NULL, blank=True, null=True)

    class Meta:
        ordering = ["fecha"]

    def __str__(self):
        return f"{self.titulo} - {self.fecha:%d/%m/%Y %H:%M}"