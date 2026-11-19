from pathlib import Path

from django.conf import settings
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.urls import reverse

from login.models import Usuario
from obras.models import Cliente, EstadoObra, Obra, Zona
from presupuestos.models import Material, Presupuesto, Superficie
from presupuestos.pdf import formato_pesos, lineas_condiciones

from .models import ConfiguracionPDF


class ConfiguracionPDFTests(TestCase):
    def setUp(self):
        self.usuario = Usuario.objects.create_superuser('admin', 'admin@test.com', 'x')
        self.client.force_login(self.usuario)
        self.datos = {
            'encabezado': 'Techos Valor\nTel. 221 000-0000',
            'titulo': 'COTIZACIÓN',
            'prefijo_numero': 'TV-',
            'mostrar_localidad': 'on',
            'condiciones': '*Validez 15 días.*',
        }

    def crear_presupuesto(self):
        obra = Obra.objects.create(
            direccion='455 y 132', zona=Zona.objects.create(localidad='La Plata'),
            cliente=Cliente.objects.create(nombre='Ana', apellido='Paz', telefono='221'),
            estado=EstadoObra.objects.create(estado='Activa'),
        )
        return Presupuesto.objects.create(
            obra=obra, material=Material.objects.create(material='Membrana'),
            superficie=Superficie.objects.create(superficie='Losa'),
            metro_2=100, precio_metro=48600, monto=0,
        )

    def test_pagina_y_vista_previa_sin_presupuestos(self):
        self.assertEqual(self.client.get(reverse('ajustes:ajustes_pdf')).status_code, 200)
        r = self.client.get(reverse('ajustes:ajustes_pdf_vista_previa'))
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r['Content-Type'], 'application/pdf')

    def test_guardar_configuracion_con_logo(self):
        logo = (Path(settings.BASE_DIR) / 'static/images/roof.png').read_bytes()
        datos = {**self.datos, 'logo_nuevo': SimpleUploadedFile('logo.png', logo, 'image/png')}
        r = self.client.post(reverse('ajustes:ajustes_pdf'), datos)
        self.assertRedirects(r, reverse('ajustes:ajustes_pdf'))

        config = ConfiguracionPDF.obtener()
        self.assertEqual(config.titulo, 'COTIZACIÓN')
        self.assertEqual(config.logo_tipo, 'image/png')
        self.assertFalse(config.mostrar_telefono_cliente)  # casilla sin marcar

        self.client.post(reverse('ajustes:ajustes_pdf'), {**self.datos, 'quitar_logo': 'on'})
        self.assertIsNone(ConfiguracionPDF.obtener().logo)

    def test_rechaza_archivo_que_no_es_imagen(self):
        datos = {**self.datos, 'logo_nuevo': SimpleUploadedFile('logo.png', b'texto', 'image/png')}
        r = self.client.post(reverse('ajustes:ajustes_pdf'), datos)
        self.assertEqual(r.status_code, 200)
        self.assertEqual(ConfiguracionPDF.obtener().titulo, 'PRESUPUESTO')  # no se guardó

    def test_pdf_del_presupuesto(self):
        pres = self.crear_presupuesto()
        r = self.client.get(reverse('presupuestos:presupuesto_pdf', args=[pres.pk]))
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r['Content-Type'], 'application/pdf')
        self.assertTrue(r.content.startswith(b'%PDF'))

    def test_pdf_requiere_sesion(self):
        pres = self.crear_presupuesto()
        self.client.logout()
        r = self.client.get(reverse('presupuestos:presupuesto_pdf', args=[pres.pk]))
        self.assertEqual(r.status_code, 302)

    def test_formatos(self):
        self.assertEqual(formato_pesos(4860000), '4.860.000')
        self.assertEqual(formato_pesos('1234.5'), '1.234,50')
        self.assertEqual(lineas_condiciones('*a*\nb'), [
            {'texto': 'a', 'cursiva': True}, {'texto': 'b', 'cursiva': False},
        ])
