from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import Q
from django.db.models.functions import Lower


class Usuario(AbstractUser):
    telefono = models.CharField(max_length=30, blank=True)

    class Meta:
        verbose_name = "usuario"
        verbose_name_plural = "usuarios"
        constraints = [
            models.UniqueConstraint(
                Lower("email"), condition=~Q(email=""), name="usuario_email_unico",
                violation_error_message="Ya existe un usuario con ese email."),
        ]

    def __str__(self):
        return self.get_full_name() or self.username


class EmailPermitido(models.Model):
    """Lista blanca: solo estos emails pueden registrarse e ingresar al sistema.
    Desactivar uno le corta el acceso al usuario aunque ya tenga cuenta."""
    email = models.EmailField(unique=True)
    activo = models.BooleanField(
        default=True, help_text="Desmarcar para bloquear el registro y el ingreso de este email.")
    nota = models.CharField(max_length=150, blank=True, help_text="Ej.: nombre de la persona.")
    creado = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "email permitido"
        verbose_name_plural = "emails permitidos"
        ordering = ["email"]

    def __str__(self):
        return self.email

    def save(self, *args, **kwargs):
        self.email = self.email.strip().lower()
        super().save(*args, **kwargs)

    @classmethod
    def esta_permitido(cls, email):
        return cls.objects.filter(email__iexact=(email or "").strip(), activo=True).exists()
