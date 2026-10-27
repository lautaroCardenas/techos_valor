from django import forms
from django.conf import settings
from django.contrib.auth import authenticate, get_user_model, password_validation
from django.core.cache import cache

from .models import EmailPermitido

MAX_INTENTOS = getattr(settings, "LOGIN_MAX_INTENTOS", 5)
BLOQUEO_SEGUNDOS = getattr(settings, "LOGIN_BLOQUEO_SEGUNDOS", 15 * 60)


class LoginForm(forms.Form):
    email = forms.EmailField(
        label="Email", max_length=254,
        widget=forms.EmailInput(attrs={"autocomplete": "email", "autofocus": True}))
    password = forms.CharField(
        label="Contraseña", strip=False,
        widget=forms.PasswordInput(attrs={"autocomplete": "current-password"}))

    error_credenciales = "Email o contraseña incorrectos."
    error_bloqueo = "Demasiados intentos fallidos. Probá de nuevo en unos minutos."

    def __init__(self, request, *args, **kwargs):
        self.request = request
        self.usuario = None
        super().__init__(*args, **kwargs)

    def _clave_intentos(self, email):
        ip = self.request.META.get("REMOTE_ADDR", "")
        return f"login-intentos:{ip}:{email.lower()}"

    def clean(self):
        email = self.cleaned_data.get("email")
        password = self.cleaned_data.get("password")
        if not email or not password:
            return self.cleaned_data

        clave = self._clave_intentos(email)
        if cache.get(clave, 0) >= MAX_INTENTOS:
            raise forms.ValidationError(self.error_bloqueo, code="bloqueado")

        self.usuario = authenticate(self.request, email=email, password=password)
        if self.usuario is None:
            cache.set(clave, cache.get(clave, 0) + 1, BLOQUEO_SEGUNDOS)
            # Mensaje genérico: no revela si el email existe o está habilitado.
            raise forms.ValidationError(self.error_credenciales, code="credenciales")

        cache.delete(clave)
        return self.cleaned_data


class RegistroForm(forms.ModelForm):
    password1 = forms.CharField(
        label="Contraseña", strip=False,
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password"}),
        help_text=password_validation.password_validators_help_text_html())
    password2 = forms.CharField(
        label="Repetir contraseña", strip=False,
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password"}))

    error_email = "No es posible registrarse con este email. Consultá con el administrador."

    class Meta:
        model = get_user_model()
        fields = ["first_name", "last_name", "email"]
        labels = {"first_name": "Nombre", "last_name": "Apellido", "email": "Email"}
        widgets = {"email": forms.EmailInput(attrs={"autocomplete": "email"})}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for campo in ("first_name", "last_name", "email"):
            self.fields[campo].required = True

    def clean_email(self):
        email = self.cleaned_data["email"].strip().lower()
        ya_existe = get_user_model().objects.filter(email__iexact=email).exists()
        # Mismo mensaje en ambos casos: no revela qué emails están cargados.
        if ya_existe or not EmailPermitido.esta_permitido(email):
            raise forms.ValidationError(self.error_email, code="email_no_permitido")
        return email

    def clean(self):
        cleaned = super().clean()
        p1, p2 = cleaned.get("password1"), cleaned.get("password2")
        if p1 and p2 and p1 != p2:
            self.add_error("password2", "Las contraseñas no coinciden.")
        elif p1:
            # Valida largo, contraseñas comunes y parecido con el nombre/email.
            self.instance.email = cleaned.get("email") or ""
            self.instance.username = self.instance.email
            self.instance.first_name = cleaned.get("first_name") or ""
            self.instance.last_name = cleaned.get("last_name") or ""
            try:
                password_validation.validate_password(p1, self.instance)
            except forms.ValidationError as error:
                self.add_error("password1", error)
        return cleaned

    def save(self, commit=True):
        usuario = super().save(commit=False)
        usuario.username = usuario.email
        usuario.set_password(self.cleaned_data["password1"])
        if commit:
            usuario.save()
        return usuario
