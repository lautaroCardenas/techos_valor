"""Generación del PDF de un presupuesto a partir de un template HTML."""
from decimal import Decimal
from io import BytesIO

from django.conf import settings
from django.contrib.staticfiles import finders
from django.template.loader import render_to_string
from xhtml2pdf import pisa

from ajustes.models import ConfiguracionPDF
from .models import Superficie


def formato_pesos(monto):
    """4860000 -> '4.860.000'; 1234.5 -> '1.234,50' (formato argentino)."""
    monto = Decimal(monto or 0).quantize(Decimal("0.01"))
    texto = f"{monto:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    return texto[:-3] if texto.endswith(",00") else texto


def lineas_condiciones(texto):
    """Separa las condiciones en renglones; los que van entre *asteriscos* salen en cursiva."""
    lineas = []
    for linea in (texto or "").splitlines():
        linea = linea.strip()
        cursiva = len(linea) > 2 and linea.startswith("*") and linea.endswith("*")
        lineas.append({"texto": linea[1:-1].strip() if cursiva else linea, "cursiva": cursiva})
    return lineas


def _resolver_archivo(uri, rel):
    """xhtml2pdf lee archivos del disco: traduce las URLs /static/... a su ruta real."""
    if uri.startswith(settings.STATIC_URL):
        ruta = finders.find(uri[len(settings.STATIC_URL):])
        if ruta:
            return ruta
    return uri


def generar_pdf_presupuesto(presupuesto, config=None):
    """Devuelve los bytes del PDF, o None si xhtml2pdf no pudo generarlo."""
    config = config or ConfiguracionPDF.obtener()
    html = render_to_string("presupuestos/pdf/presupuesto.html", {
        "config": config,
        "encabezado": [l for l in config.encabezado.splitlines()],
        "condiciones": lineas_condiciones(config.condiciones),
        "presupuesto": presupuesto,
        "obra": presupuesto.obra,
        "cliente": presupuesto.obra.cliente,
        "superficies": Superficie.objects.order_by("superficie") if config.mostrar_superficies else [],
        "monto": formato_pesos(presupuesto.monto),
        "precio_metro": formato_pesos(presupuesto.precio_metro),
        "metros": formato_pesos(presupuesto.metro_2),
    })
    salida = BytesIO()
    resultado = pisa.CreatePDF(html, dest=salida, encoding="utf-8", link_callback=_resolver_archivo)
    if resultado.err:
        return None
    return salida.getvalue()
