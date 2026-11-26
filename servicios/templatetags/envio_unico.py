import uuid

from django import template
from django.utils.html import format_html

from servicios.envio_unico import CAMPO_TOKEN

register = template.Library()


@register.simple_tag
def token_envio():
    """Campo oculto con un código nuevo cada vez que se muestra el formulario."""
    return format_html('<input type="hidden" name="{}" value="{}">', CAMPO_TOKEN, uuid.uuid4().hex)
