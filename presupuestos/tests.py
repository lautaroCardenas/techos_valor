from django.db import IntegrityError, transaction
from django.test import TestCase
from django.urls import reverse

from login.models import Usuario
from obras.models import Cliente, EstadoObra, Obra, Zona
from .forms import PresupuestoForm
from .models import DescripcionPredeterminada, Material, Presupuesto, Superficie


class DescripcionPredeterminadaTests(TestCase):
    def setUp(self):
        self.usuario = Usuario.objects.create_superuser('admin', 'admin@test.com', 'x')
        self.client.force_login(self.usuario)

        self.membrana = Material.objects.create(material='Membrana')
        self.chapa = Material.objects.create(material='Chapa')
        self.losa = Superficie.objects.create(superficie='Losa')
        self.techo = Superficie.objects.create(superficie='Techo')
        self.obra = Obra.objects.create(
            direccion='455 y 132', zona=Zona.objects.create(localidad='La Plata'),
            cliente=Cliente.objects.create(nombre='Ana', apellido='Paz', telefono='221'),
            estado=EstadoObra.objects.create(estado='Activa'),
        )
        self.predeterminada = DescripcionPredeterminada.objects.create(
            material=self.membrana, superficie=self.losa, texto='Membrana de 40 kg sobre losa.',
        )
        self.url = reverse('presupuestos:descripcion_predeterminada')

    def datos_form(self, **extra):
        datos = {
            'metro_2': '100', 'precio_metro': '1000', 'material': self.membrana.pk,
            'superficie': self.losa.pk, 'obra': self.obra.pk, 'recargo_porcentaje': '0',
            'descripcion_impresa': '', 'observacion': '',
        }
        datos.update(extra)
        return datos

    # Endpoint

    def test_endpoint_devuelve_el_texto(self):
        r = self.client.get(self.url, {'material': self.membrana.pk, 'superficie': self.losa.pk})
        self.assertEqual(r.json(), {'texto': 'Membrana de 40 kg sobre losa.'})

    def test_endpoint_vacio_si_no_hay_predeterminada(self):
        r = self.client.get(self.url, {'material': self.chapa.pk, 'superficie': self.techo.pk})
        self.assertEqual(r.json(), {'texto': ''})

    def test_endpoint_parametros_invalidos_o_faltantes(self):
        for params in ({}, {'material': self.membrana.pk}, {'material': 'abc', 'superficie': self.losa.pk},
                       {'material': '', 'superficie': ''}, {'material': '1.5', 'superficie': '2'}):
            r = self.client.get(self.url, params)
            self.assertEqual(r.status_code, 200, params)
            self.assertEqual(r.json(), {'texto': ''}, params)

    def test_endpoint_requiere_sesion(self):
        self.client.logout()
        r = self.client.get(self.url, {'material': self.membrana.pk, 'superficie': self.losa.pk})
        self.assertEqual(r.status_code, 302)

    # Constraint

    def test_no_se_puede_duplicar_material_y_superficie(self):
        with self.assertRaises(IntegrityError), transaction.atomic():
            DescripcionPredeterminada.objects.create(
                material=self.membrana, superficie=self.losa, texto='Otra',
            )

    # Checkbox "guardar como predeterminada"

    def test_checkbox_crea_la_predeterminada(self):
        form = PresupuestoForm(self.datos_form(
            material=self.chapa.pk, superficie=self.techo.pk,
            descripcion_impresa='Chapa sobre techo.', guardar_como_predeterminada='on',
        ))
        self.assertTrue(form.is_valid(), form.errors)
        form.save()
        self.assertEqual(
            DescripcionPredeterminada.objects.get(material=self.chapa, superficie=self.techo).texto,
            'Chapa sobre techo.',
        )

    def test_checkbox_actualiza_la_predeterminada(self):
        form = PresupuestoForm(self.datos_form(
            descripcion_impresa='Texto nuevo.', guardar_como_predeterminada='on',
        ))
        self.assertTrue(form.is_valid(), form.errors)
        form.save()
        self.predeterminada.refresh_from_db()
        self.assertEqual(self.predeterminada.texto, 'Texto nuevo.')
        self.assertEqual(DescripcionPredeterminada.objects.filter(
            material=self.membrana, superficie=self.losa).count(), 1)

    def test_sin_checkbox_no_toca_la_predeterminada(self):
        form = PresupuestoForm(self.datos_form(descripcion_impresa='Solo para esta obra.'))
        self.assertTrue(form.is_valid(), form.errors)
        form.save()
        self.predeterminada.refresh_from_db()
        self.assertEqual(self.predeterminada.texto, 'Membrana de 40 kg sobre losa.')

    def test_checkbox_desde_la_vista_de_edicion(self):
        pres = Presupuesto.objects.create(
            obra=self.obra, material=self.chapa, superficie=self.techo,
            metro_2=10, precio_metro=10, monto=0, descripcion_impresa='',
        )
        r = self.client.post(
            reverse('presupuestos:presupuesto_actualizar', args=[pres.pk]),
            self.datos_form(material=self.chapa.pk, superficie=self.techo.pk,
                            descripcion_impresa='Desde edición.', guardar_como_predeterminada='on'),
        )
        self.assertEqual(r.status_code, 200)
        self.assertTrue(DescripcionPredeterminada.objects.filter(
            material=self.chapa, superficie=self.techo, texto='Desde edición.').exists())

    # Respaldo del servidor

    def test_respaldo_completa_la_descripcion_vacia_al_crear(self):
        r = self.client.post(reverse('presupuestos:presupuesto_crear'), self.datos_form())
        self.assertEqual(r.status_code, 302)
        self.assertEqual(Presupuesto.objects.get().descripcion_impresa, 'Membrana de 40 kg sobre losa.')

    def test_respaldo_no_toca_una_descripcion_con_texto(self):
        self.client.post(reverse('presupuestos:presupuesto_crear'),
                         self.datos_form(descripcion_impresa='Trabajo puntual.'))
        self.assertEqual(Presupuesto.objects.get().descripcion_impresa, 'Trabajo puntual.')

    def test_respaldo_no_aplica_al_editar(self):
        pres = Presupuesto.objects.create(
            obra=self.obra, material=self.membrana, superficie=self.losa,
            metro_2=10, precio_metro=10, monto=0, descripcion_impresa='Vieja',
        )
        form = PresupuestoForm(self.datos_form(descripcion_impresa=''), instance=pres)
        self.assertTrue(form.is_valid(), form.errors)
        form.save()
        pres.refresh_from_db()
        self.assertEqual(pres.descripcion_impresa, '')

    def test_respaldo_sin_predeterminada_deja_vacio(self):
        form = PresupuestoForm(self.datos_form(material=self.chapa.pk, superficie=self.techo.pk))
        self.assertTrue(form.is_valid(), form.errors)
        self.assertEqual(form.save().descripcion_impresa, '')

    # Formularios

    def test_checkbox_aparece_debajo_de_la_descripcion(self):
        campos = list(PresupuestoForm().fields)
        self.assertEqual(campos.index('guardar_como_predeterminada'),
                         campos.index('descripcion_impresa') + 1)
        r = self.client.get(reverse('presupuestos:presupuestos_total'))
        self.assertContains(r, 'name="guardar_como_predeterminada"')
        self.assertContains(r, 'js/descripcion-predeterminada.js')
        self.assertContains(r, f'data-url="{self.url}"')
