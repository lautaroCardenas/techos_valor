from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('obras', '0003_alter_obra_fecha_visita_alter_obra_proxima_accion'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='obra',
            name='fecha_visita',
        ),
    ]