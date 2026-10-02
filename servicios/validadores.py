from django.core.exceptions import ValidationError
from .helpers import colapsar_espacios

def solo_letras(valor):
    valor_limpio = colapsar_espacios(valor)

    if not valor_limpio:
        raise ValidationError("Este campo no puede estar vacío")

    if not all(c.isalpha() or c.isspace() or c in "-.,°" for c in valor_limpio):
        raise ValidationError("Solo puede contener letras y '-.,°'")

def valores_positivos(valor):
    valor_limpio = colapsar_espacios(valor)

    if valor_limpio <= 0:
        raise ValidationError("El número no puede ser negativo")