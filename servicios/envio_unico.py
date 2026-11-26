"""Evita que un mismo formulario de alta se guarde dos veces.

Uso en una vista:

    @envio_unico('Presupuesto cargado correctamente', destino_duplicado)
    def presupuesto_crear(request): ...

y en el template, dentro del <form>: {% load envio_unico %}{% token_envio %}
"""
from datetime import timedelta
from functools import wraps

from django.contrib import messages
from django.db import IntegrityError, transaction
from django.shortcuts import redirect
from django.utils import timezone

CAMPO_TOKEN = 'token_envio'

# Etiqueta de los mensajes que se muestran como cartel flotante (ver base.html).
TAG_AVISO = 'aviso_flotante'

# Los códigos usados se borran pasado este tiempo: alcanza para cubrir reenvíos.
VIGENCIA_TOKENS = timedelta(days=2)


def avisar(request, texto):
    """Cartel verde con ✓ que se cierra solo."""
    messages.success(request, texto, extra_tags=TAG_AVISO)


def _es_exito(response):
    # Las vistas de alta redirigen cuando guardan; si muestran el formulario de nuevo es
    # porque hubo errores. Los casos de error que también redirigen se filtran con
    # exito_si (ver presupuesto_crear y obra_crear).
    return 300 <= response.status_code < 400


def envio_unico(texto_exito, destino_duplicado, exito_si=None):
    """Decorador para vistas de alta.

    - texto_exito: el cartel que se muestra al guardar.
    - destino_duplicado(request): a dónde ir si el formulario ya se había guardado.
    - exito_si(request, response): opcional, para vistas que redirigen también con errores.
    """
    def decorador(vista):
        @wraps(vista)
        def envoltura(request, *args, **kwargs):
            token = request.POST.get(CAMPO_TOKEN, '') if request.method == 'POST' else ''
            if not token:
                # GET, o un formulario sin código (página vieja en caché): sigue normal.
                return vista(request, *args, **kwargs)

            from servicios.models import EnvioFormulario

            # El código y lo que guarde la vista van en la misma transacción: si la vista
            # explota, no queda el código marcado sin haberse guardado nada. Si hay errores
            # de validación el código queda usado igual, pero no importa: el formulario se
            # vuelve a mostrar con un código nuevo.
            with transaction.atomic():
                try:
                    # Savepoint propio: así solo se atrapa el código repetido y no un
                    # IntegrityError de lo que guarde la vista.
                    with transaction.atomic():
                        EnvioFormulario.objects.create(token=token[:64])
                except IntegrityError:
                    duplicado = True
                else:
                    duplicado = False
                    response = vista(request, *args, **kwargs)

            if duplicado:
                # Ya se guardó con este código: no se crea nada de nuevo. Para quien hizo
                # doble clic, el navegador muestra esta respuesta y no la primera, así que
                # se ve igual que un guardado normal.
                avisar(request, texto_exito)
                return redirect(destino_duplicado(request))

            if _es_exito(response) and (exito_si is None or exito_si(request, response)):
                avisar(request, texto_exito)
                _limpiar_viejos()
            return response
        return envoltura
    return decorador


def _limpiar_viejos():
    from servicios.models import EnvioFormulario
    EnvioFormulario.objects.filter(creado__lt=timezone.now() - VIGENCIA_TOKENS).delete()
