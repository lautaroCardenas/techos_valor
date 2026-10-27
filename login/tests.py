from django.contrib.auth import get_user_model
from django.core.cache import cache
from django.test import TestCase
from django.urls import reverse

from .models import EmailPermitido

PASSWORD = "Techos-2026-seguro"


class RegistroTests(TestCase):
    def datos(self, email="ana@mail.com"):
        return {
            "first_name": "Ana", "last_name": "Pérez", "email": email,
            "password1": PASSWORD, "password2": PASSWORD,
        }

    def test_email_habilitado_puede_registrarse(self):
        EmailPermitido.objects.create(email="Ana@Mail.com")
        response = self.client.post(reverse("login:registro"), self.datos("ANA@mail.com"))
        self.assertRedirects(response, reverse("login:login"))
        usuario = get_user_model().objects.get()
        self.assertEqual(usuario.email, "ana@mail.com")
        self.assertTrue(usuario.check_password(PASSWORD))

    def test_email_no_habilitado_no_puede_registrarse(self):
        response = self.client.post(reverse("login:registro"), self.datos("intruso@mail.com"))
        self.assertEqual(response.status_code, 200)
        self.assertFalse(get_user_model().objects.exists())

    def test_email_desactivado_no_puede_registrarse(self):
        EmailPermitido.objects.create(email="ana@mail.com", activo=False)
        self.client.post(reverse("login:registro"), self.datos())
        self.assertFalse(get_user_model().objects.exists())

    def test_no_se_puede_registrar_dos_veces(self):
        EmailPermitido.objects.create(email="ana@mail.com")
        self.client.post(reverse("login:registro"), self.datos())
        self.client.post(reverse("login:registro"), self.datos())
        self.assertEqual(get_user_model().objects.count(), 1)

    def test_contrasenia_debil_o_distinta(self):
        EmailPermitido.objects.create(email="ana@mail.com")
        datos = self.datos()
        datos["password1"] = datos["password2"] = "12345678"
        self.client.post(reverse("login:registro"), datos)
        datos = self.datos()
        datos["password2"] = "otra-cosa-distinta"
        self.client.post(reverse("login:registro"), datos)
        self.assertFalse(get_user_model().objects.exists())


class LoginTests(TestCase):
    def setUp(self):
        cache.clear()
        EmailPermitido.objects.create(email="ana@mail.com")
        self.usuario = get_user_model().objects.create_user(
            username="ana@mail.com", email="ana@mail.com", password=PASSWORD)

    def login(self, password=PASSWORD, email="ana@mail.com", **extra):
        return self.client.post(reverse("login:login"), {"email": email, "password": password, **extra})

    def test_login_correcto(self):
        response = self.login()
        self.assertRedirects(response, reverse("obras:obras_total"))

    def test_login_incorrecto(self):
        response = self.login(password="mala")
        self.assertContains(response, "Email o contraseña incorrectos.")
        self.assertNotIn("_auth_user_id", self.client.session)

    def test_email_desactivado_no_puede_ingresar(self):
        EmailPermitido.objects.filter(email="ana@mail.com").update(activo=False)
        response = self.login()
        self.assertContains(response, "Email o contraseña incorrectos.")

    def test_bloqueo_por_intentos_fallidos(self):
        for _ in range(5):
            self.login(password="mala")
        response = self.login()  # aun con la contraseña correcta
        self.assertContains(response, "Demasiados intentos fallidos")
        self.assertNotIn("_auth_user_id", self.client.session)

    def test_next_externo_se_ignora(self):
        response = self.login(next="https://sitio-malicioso.com/")
        self.assertRedirects(response, reverse("obras:obras_total"))

    def test_next_interno_se_respeta(self):
        response = self.login(next=reverse("ajustes:ajustes"))
        self.assertRedirects(response, reverse("ajustes:ajustes"))

    def test_logout_solo_por_post(self):
        self.client.force_login(self.usuario)
        self.assertEqual(self.client.get(reverse("login:logout")).status_code, 405)
        response = self.client.post(reverse("login:logout"))
        self.assertRedirects(response, reverse("login:login"))
        self.assertNotIn("_auth_user_id", self.client.session)


class RutasProtegidasTests(TestCase):
    def test_sin_sesion_redirige_al_login(self):
        for nombre in ["obras:obras_total", "presupuestos:presupuestos_total",
                       "pagos:pagos_total", "ajustes:ajustes"]:
            with self.subTest(nombre=nombre):
                url = reverse(nombre)
                response = self.client.get(url)
                self.assertRedirects(
                    response, f"{reverse('login:login')}?next={url}", fetch_redirect_response=False)

    def test_detalle_sin_sesion_redirige_al_login(self):
        response = self.client.get("/obras/1/")
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith(reverse("login:login")))

    def test_login_y_registro_son_publicos(self):
        self.assertEqual(self.client.get(reverse("login:login")).status_code, 200)
        self.assertEqual(self.client.get(reverse("login:registro")).status_code, 200)
