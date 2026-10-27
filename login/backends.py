from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend

from .models import EmailPermitido


class EmailBackend(ModelBackend):
    """Ingreso con email + contraseña. Salvo los superusuarios, el email
    tiene que seguir habilitado en EmailPermitido."""

    def authenticate(self, request, email=None, password=None, **kwargs):
        if not email or not password:
            return None
        Usuario = get_user_model()
        try:
            usuario = Usuario.objects.get(email__iexact=email.strip())
        except Usuario.DoesNotExist:
            # Hashea igual para que el tiempo de respuesta no delate si el email existe.
            Usuario().set_password(password)
            return None
        if usuario.check_password(password) and self.user_can_authenticate(usuario):
            return usuario
        return None

    def user_can_authenticate(self, user):
        if not super().user_can_authenticate(user):
            return False
        return user.is_superuser or EmailPermitido.esta_permitido(user.email)
