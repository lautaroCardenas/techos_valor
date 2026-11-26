import uuid

from django.test import TestCase
from django.urls import reverse

from login.models import Usuario
from obras.models import Cliente, EstadoObra, Obra, Zona
from pagos.models import Pagos
from presupuestos.models import Material, Presupuesto, Superficie
from servicios.models import EnvioFormulario


def token():
    return uuid.uuid4().hex


class EnvioUnicoTests(TestCase):
    def setUp(self):
        self.client.force_login(Usuario.objects.create_superuser('admin', 'admin@test.com', 'x'))
        self.zona = Zona.objects.create(localidad='La Plata')
        self.estado = EstadoObra.objects.create(estado='Activa')
        self.cliente = Cliente.objects.create(nombre='Ana', apellido='Paz', telefono='2214445555')
        self.material = Material.objects.create(material='Aluminio')
        self.superficie = Superficie.objects.create(superficie='Losa')

    def datos_cliente(self, **extra):
        return {'nombre': 'Arq', 'apellido': 'Catanzaro', 'telefono': '22155544468',
                'origen': 'presupuestos', **extra}

    def datos_obra(self, **extra):
        return {'cliente': self.cliente.pk, 'direccion': '455 y 132', 'zona': self.zona.pk,
                'estado': self.estado.pk, 'negocio': '', 'garantia': 'on',
                'origen': 'presupuestos', **extra}

    def crear_obra(self, **extra):
        return Obra.objects.create(cliente=self.cliente, direccion='1 y 50', zona=self.zona,
                                   estado=self.estado, negocio=False, **extra)

    def datos_presupuesto(self, obra, **extra):
        return {'obra': obra.pk, 'metro_2': '100', 'precio_metro': '1000',
                'material': self.material.pk, 'superficie': self.superficie.pk,
                'recargo_porcentaje': '0', 'observacion': '', 'descripcion_impresa': '', **extra}

    def mensajes(self, response):
        return [str(m) for m in response.context['messages']] if response.context else []

    # Doble envío del mismo formulario

    def test_cliente_doble_envio_crea_uno_solo(self):
        datos = self.datos_cliente(token_envio=token())
        self.client.post(reverse('obras:cliente_crear'), datos)
        r = self.client.post(reverse('obras:cliente_crear'), datos, follow=True)
        self.assertEqual(Cliente.objects.filter(apellido='Catanzaro').count(), 1)
        # El segundo envío se ve como un guardado normal.
        self.assertIn('Cliente cargado correctamente', self.mensajes(r))
        self.assertContains(r, 'class="aviso"')

    def test_obra_doble_envio_crea_una_sola(self):
        datos = self.datos_obra(token_envio=token())
        self.client.post(reverse('obras:obra_crear'), datos)
        self.client.post(reverse('obras:obra_crear'), datos)
        self.assertEqual(Obra.objects.count(), 1)

    def test_presupuesto_doble_envio_crea_uno_solo(self):
        datos = self.datos_presupuesto(self.crear_obra(), token_envio=token())
        self.client.post(reverse('presupuestos:presupuesto_crear'), datos)
        r = self.client.post(reverse('presupuestos:presupuesto_crear'), datos, follow=True)
        self.assertEqual(Presupuesto.objects.count(), 1)
        self.assertIn('Presupuesto cargado correctamente', self.mensajes(r))

    def test_pago_doble_envio_crea_uno_solo(self):
        obra = self.crear_obra()
        pres = Presupuesto.objects.create(obra=obra, material=self.material, superficie=self.superficie,
                                          metro_2=10, precio_metro=100, monto=0, aceptado=True)
        datos = {'presupuesto_id': pres.pk, 'numero': '1', 'monto_pagado': '100', 'token_envio': token()}
        self.client.post(reverse('pagos:pago_crear'), datos)
        r = self.client.post(reverse('pagos:pago_crear'), datos)
        self.assertEqual(Pagos.objects.count(), 1)
        self.assertRedirects(r, reverse('pagos:pago_detalle', args=[obra.pk]), fetch_redirect_response=False)

    # Lo que NO se tiene que bloquear

    def test_un_cliente_puede_tener_varias_obras(self):
        self.client.post(reverse('obras:obra_crear'), self.datos_obra(token_envio=token()))
        self.client.post(reverse('obras:obra_crear'),
                         self.datos_obra(direccion='7 y 60', token_envio=token()))
        self.assertEqual(Obra.objects.filter(cliente=self.cliente).count(), 2)

    def test_una_obra_puede_tener_varios_presupuestos(self):
        obra = self.crear_obra()
        for _ in range(2):
            self.client.post(reverse('presupuestos:presupuesto_crear'),
                             self.datos_presupuesto(obra, token_envio=token()))
        self.assertEqual(Presupuesto.objects.filter(obra=obra).count(), 2)

    def test_sin_codigo_funciona_como_antes(self):
        self.client.post(reverse('obras:cliente_crear'), self.datos_cliente())
        self.assertEqual(Cliente.objects.filter(apellido='Catanzaro').count(), 1)

    def test_con_errores_no_muestra_el_aviso_y_se_puede_reintentar(self):
        obra = self.crear_obra()
        r = self.client.post(reverse('presupuestos:presupuesto_crear'),
                             self.datos_presupuesto(obra, metro_2='-5', token_envio=token()), follow=True)
        self.assertEqual(Presupuesto.objects.count(), 0)
        self.assertNotIn('Presupuesto cargado correctamente', self.mensajes(r))
        # El formulario se vuelve a mostrar con un código nuevo, que sirve para corregir.
        self.client.post(reverse('presupuestos:presupuesto_crear'),
                         self.datos_presupuesto(obra, token_envio=token()))
        self.assertEqual(Presupuesto.objects.count(), 1)

    def test_los_formularios_traen_el_codigo(self):
        r = self.client.get(reverse('presupuestos:presupuestos_total'))
        # Presupuesto, obra y cliente: un código distinto para cada formulario.
        self.assertEqual(r.content.decode().count('name="token_envio"'), 3)
        self.assertContains(r, 'js/envio-unico.js')

    def test_el_codigo_se_registra(self):
        codigo = token()
        self.client.post(reverse('obras:cliente_crear'), self.datos_cliente(token_envio=codigo))
        self.assertTrue(EnvioFormulario.objects.filter(token=codigo).exists())
