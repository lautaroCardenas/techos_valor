from django import forms
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import AdminPasswordChangeForm, AdminUserCreationForm
from .models import EmailPermitido, Usuario

# Los usuarios que carga el administrador pueden tener una contraseña simple.
# El registro público (/registro/) sigue pidiendo una contraseña segura.
LARGO_MINIMO_ADMIN = 4


class ContraseniaSimpleMixin:
    """Reemplaza los validadores de contraseña de Django por un largo mínimo."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if "password1" in self.fields:
            self.fields["password1"].help_text = f"Mínimo {LARGO_MINIMO_ADMIN} caracteres."

    def validate_password_for_user(self, user, password_field_name="password2", **kwargs):
        if not self.cleaned_data.get("set_usable_password", True):
            return
        password = self.cleaned_data.get(password_field_name)
        if password and len(password) < LARGO_MINIMO_ADMIN:
            self.add_error(
                password_field_name,
                f"La contraseña debe tener al menos {LARGO_MINIMO_ADMIN} caracteres.")


class UsuarioCreationForm(ContraseniaSimpleMixin, AdminUserCreationForm):
    class Meta(AdminUserCreationForm.Meta):
        model = Usuario
        fields = ("username", "email", "first_name", "last_name", "telefono")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["email"].required = True

    def clean_email(self):
        email = self.cleaned_data["email"].strip().lower()
        if Usuario.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError("Ya existe un usuario con ese email.")
        return email


class UsuarioPasswordChangeForm(ContraseniaSimpleMixin, AdminPasswordChangeForm):
    pass


@admin.register(Usuario)
class UsuarioAdmin(UserAdmin):
    add_form = UsuarioCreationForm
    change_password_form = UsuarioPasswordChangeForm
    list_display = ("username", "first_name", "last_name", "email", "is_active", "is_staff")
    search_fields = ("username", "first_name", "last_name", "email")
    fieldsets = UserAdmin.fieldsets + (
        ("Datos adicionales", {"fields": ("telefono",)}),
    )
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("username", "email", "usable_password", "password1", "password2"),
        }),
        ("Datos adicionales", {"fields": ("first_name", "last_name", "telefono")}),
    )

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        # Si el admin carga el usuario, su email queda habilitado para ingresar.
        if obj.email:
            EmailPermitido.objects.get_or_create(
                email=obj.email.strip().lower(), defaults={"nota": str(obj)})


@admin.register(EmailPermitido)
class EmailPermitidoAdmin(admin.ModelAdmin):
    list_display = ("email", "nota", "activo", "creado")
    list_filter = ("activo",)
    search_fields = ("email", "nota")
    list_editable = ("activo",)
