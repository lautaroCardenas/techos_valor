from django.contrib import admin
from .models import Presupuesto, Material, Superficie

# Register your models here.
@admin.register(Material)
class MaterialAdmin(admin.ModelAdmin):
    list_display = ("material",)

@admin.register(Superficie)
class SuperficieAdmin(admin.ModelAdmin):
    list_display = ("superficie",)

@admin.register(Presupuesto)
class PresupuestoAdmin(admin.ModelAdmin):
    list_display = ("id", "aceptado", "fecha_actual", "metro_2", "precio_metro", "material", "superficie", "monto", "obra")
    list_filter = ("obra__cliente", "aceptado")
    readonly_fields = ("monto", "fecha_actual")
    ordering = ("fecha_actual",)