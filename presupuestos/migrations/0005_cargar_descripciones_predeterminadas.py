"""Carga las descripciones predeterminadas que usa el cliente hoy en sus presupuestos.

- Crea la superficie "Chapa" y el material "Antitérmico" si no existen.
- Los materiales se buscan por nombre sin importar mayúsculas: si alguno no existe
  en la base, se saltea (no se inventan materiales salvo Antitérmico).
- Los textos sin superficie definida se cargan para todas las superficies que haya.
- No pisa descripciones que ya existan (por ejemplo, editadas desde el formulario).
"""
from django.db import migrations


ALUMINIO_CHAPA = (
    "Imprimación asfáltica y colocación de membrana de 40 kg profesional y aluminio puro, "
    "respetando el sentido de escurrimiento."
)
ALUMINIO_LOSA = (
    "Imprimación asfáltica y colocación de membrana de 40 kg profesional y aluminio puro,\n"
    "adherido en su totalidad y respetando el sentido de escurrimiento."
)
GEO_PINTURA = (
    "Imprimación asfáltica y colocación de membrana geotextil transitable de 40 kg profesional, "
    "adherido en su totalidad y respetando el sentido de escurrimiento. "
    "Acabado de pintura (color a elección)."
)
GEO_MORDIENTE = (
    "Imprimación asfáltica y colocación de membrana geotextil de 40 kg profesional, "
    "adherido en su totalidad y respetando el sentido de escurrimiento. Acabado de mordiente."
)
ANTITERMICO = (
    "Colocación de EPS (telgopor) de 30 mm de espesor y 15 kg de densidad sobre toda la superficie "
    "y luego colocación de membrana de 40 kg profesional y aluminio puro, "
    "respetando el sentido de escurrimiento."
)

# (material, superficie o None = todas, texto)
DESCRIPCIONES = [
    ("Aluminio", "Chapa", ALUMINIO_CHAPA),
    ("Aluminio", "Losa", ALUMINIO_LOSA),
    ("Geotextil pintura", None, GEO_PINTURA),
    ("Geotextil no mordiente", None, GEO_PINTURA),
    ("Geotextil (mordiente)", None, GEO_MORDIENTE),
    ("Antitérmico", None, ANTITERMICO),
]


def buscar_o_crear(modelo, campo, nombre):
    obj = modelo.objects.filter(**{f"{campo}__iexact": nombre}).first()
    return obj or modelo.objects.create(**{campo: nombre})


def cargar(apps, schema_editor):
    Material = apps.get_model("presupuestos", "Material")
    Superficie = apps.get_model("presupuestos", "Superficie")
    DescripcionPredeterminada = apps.get_model("presupuestos", "DescripcionPredeterminada")

    buscar_o_crear(Superficie, "superficie", "Chapa")
    buscar_o_crear(Material, "material", "Antitérmico")

    for nombre_material, nombre_superficie, texto in DESCRIPCIONES:
        material = Material.objects.filter(material__iexact=nombre_material).first()
        if material is None:
            continue

        if nombre_superficie:
            superficies = Superficie.objects.filter(superficie__iexact=nombre_superficie)
        else:
            superficies = Superficie.objects.all()

        for superficie in superficies:
            DescripcionPredeterminada.objects.get_or_create(
                material=material, superficie=superficie, defaults={"texto": texto},
            )


class Migration(migrations.Migration):

    dependencies = [
        ("presupuestos", "0004_descripcion_predeterminada"),
    ]

    # Al revertir no se borra nada: las descripciones pueden haberse editado después.
    operations = [
        migrations.RunPython(cargar, migrations.RunPython.noop),
    ]
