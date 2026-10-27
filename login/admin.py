from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import EmailPermitido, Usuario


@admin.register(Usuario)
class UsuarioAdmin(UserAdmin):
    list_display = ("username", "first_name", "last_name", "email", "is_active", "is_staff")
    search_fields = ("username", "first_name", "last_name", "email")
    fieldsets = UserAdmin.fieldsets + (
        ("Datos adicionales", {"fields": ("telefono",)}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ("Datos adicionales", {"fields": ("telefono",)}),
    )


@admin.register(EmailPermitido)
class EmailPermitidoAdmin(admin.ModelAdmin):
    list_display = ("email", "nota", "activo", "creado")
    list_filter = ("activo",)
    search_fields = ("email", "nota")
    list_editable = ("activo",)