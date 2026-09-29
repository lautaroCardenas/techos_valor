from django.contrib import admin
from .models import Obra, Zona, Cliente, FechaVisita, EstadoObra, ProximaAccion

# Register your models here.
@admin.register(Zona)
class ZonaAdmin(admin.ModelAdmin):
    list_display = ("localidad",)
    search_fields = ("localidad",)

@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ("nombre", "apellido", "telefono")
    search_fields = ("nombre", "apellido", "telefono")

@admin.register(FechaVisita)
class FechaVisitaAdmin(admin.ModelAdmin):
    list_display = ("numero", "fecha")

@admin.register(EstadoObra)
class EstadoObraAdmin(admin.ModelAdmin):
    list_display = ("estado",)

@admin.register(ProximaAccion)
class ProximaAccionAdmin(admin.ModelAdmin):
    list_display = ("accion",)

@admin.register(Obra)
class ObraAdmin(admin.ModelAdmin):
    list_display = ("cliente", "direccion", "zona", "estado", "proxima_accion", "fecha_contacto")
    ordering = ("fecha_contacto",)
    readonly_fields = ("fecha_contacto",)
    list_filter = ("proxima_accion", "estado", "garantia", "negocio")
    search_fields = ("direccion", "cliente__nombre", "cliente__apellido")
    autocomplete_fields = ("zona", "cliente")
    