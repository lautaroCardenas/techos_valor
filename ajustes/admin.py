from django.contrib import admin
from django.shortcuts import redirect
from django.urls import reverse

from .models import Configuracion, Material, Zona


@admin.register(Material)
class MaterialAdmin(admin.ModelAdmin):
    list_display = ("nombre", "precio_m2", "activo")
    list_editable = ("precio_m2", "activo")
    list_filter = ("activo",)
    search_fields = ("nombre",)


@admin.register(Zona)
class ZonaAdmin(admin.ModelAdmin):
    list_display = ("localidad", "activo")
    list_editable = ("activo",)
    list_filter = ("activo",)
    search_fields = ("localidad",)


@admin.register(Configuracion)
class ConfiguracionAdmin(admin.ModelAdmin):
    fieldsets = (
        ("Porcentajes", {"fields": ("porcentaje_comision", "recargo_no_efectivo")}),
        ("Presupuesto", {"fields": ("template_presupuesto",)}),
        (None, {"fields": ("actualizado",)}),
    )
    readonly_fields = ("actualizado",)

    def changelist_view(self, request, extra_context=None):
        # Hay un solo registro: en vez de un listado, se abre directo para editar
        obj = Configuracion.obtener()
        return redirect(reverse("admin:ajustes_configuracion_change", args=[obj.pk]))

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
