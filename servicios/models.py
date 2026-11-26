from django.db import models


class EnvioFormulario(models.Model):
    """Código de un formulario que ya se guardó, para no guardarlo dos veces.

    Cada formulario de alta lleva un código único oculto ({% token_envio %}). El primer
    envío lo registra acá; si llega otro con el mismo código (doble clic, Enter repetido,
    reintento del navegador), la restricción unique lo rechaza aunque lleguen a la vez.
    """
    token = models.CharField(max_length=64, unique=True)
    creado = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "envío de formulario"
        verbose_name_plural = "envíos de formularios"

    def __str__(self):
        return self.token
