from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q

from .models import EmailPermitido


class EmailBackend(ModelBackend):
    """Ingreso con email o nombre de usuario + contraseña. Salvo los
    superusuarios, el email tiene que seguir habilitado en EmailPermitido."""

    def authenticate(self, request, identificador=None, password=None, **kwargs):
        if not identificador or not password:
            return None
        identificador = identificador.strip()
        Usuario = get_user_model()
        candidatos = list(Usuario.objects.filter(
            Q(email__iexact=identificador) | Q(username__iexact=identificador))[:2])
        if len(candidatos) != 1:
            # Hashea igual para que el tiempo de respuesta no delate si el usuario existe.
            Usuario().set_password(password)
            return None
        usuario = candidatos[0]
        if usuario.check_password(password) and self.user_can_authenticate(usuario):
            return usuario
        return None

    def user_can_authenticate(self, user):
        if not super().user_can_authenticate(user):
            return False
        return user.is_superuser or EmailPermitido.esta_permitido(user.email)
