from django.contrib import admin
from .models import Pagos

# Register your models here.
@admin.register(Pagos)
class PagosAdmin(admin.ModelAdmin):
    list_display = ("numero", "presupuesto__monto", "monto_pagado", "resto", "comision_monto", "presupuesto__obra")
    ordering = ("presupuesto__obra",)
    readonly_fields = ("comision_monto",)
    search_fields = ("presupuesto__obra__cliente__nombre", "presupuesto__obra__cliente__apellido")
