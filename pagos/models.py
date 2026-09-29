from django.db import models
from decimal import Decimal

# Create your models here.

class Pagos(models.Model):
    numero = models.IntegerField()
    monto_pagado = models.DecimalField(max_digits=10, decimal_places=3)
    resto = models.DecimalField(max_digits=10, decimal_places=3, editable=False)
    presupuesto = models.ForeignKey('presupuestos.Presupuesto', on_delete=models.RESTRICT)
    comision_porcentaje = models.DecimalField(max_digits=10, decimal_places=3, default=0)
    comision_monto = models.DecimalField(max_digits=10, decimal_places=3)

    def save(self, *args, **kwargs):
        pagos_previos = Pagos.objects.filter(presupuesto=self.presupuesto).exclude(pk=self.pk) # Buscar pagos que pertenecen al mismo presupuesto.
        
        total_pagado = 0
        for p in pagos_previos: # Calcular cuánto el cliente ya pagó.
            total_pagado += p.monto_pagado

        total_pagado += self.monto_pagado # Agregar lo que acaba de pagar.

        self.resto = self.presupuesto.monto - total_pagado

        if self.resto < 0:
            self.resto = Decimal('0.000')

        if self.presupuesto.obra.negocio:
            self.comision_monto = self.monto_pagado * self.comision_porcentaje / 100

        super().save(*args, **kwargs)

    def __str__(self):
        return (f"N° {self.numero} - monto pagado: {self.monto_pagado} - resto: {self.resto}")

    class Meta:
        ordering = ["numero"]
        verbose_name = "Pago"
        verbose_name_plural = "Pagos"