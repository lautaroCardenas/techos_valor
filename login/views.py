from django.conf import settings
from django.contrib import messages
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_not_required
from django.shortcuts import redirect, render, resolve_url
from django.utils.http import url_has_allowed_host_and_scheme
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.debug import sensitive_post_parameters
from django.views.decorators.http import require_POST

from .forms import LoginForm, RegistroForm


def _destino_seguro(request):
    """Respeta ?next= solo si apunta a este mismo sitio (evita redirecciones a otros dominios)."""
    destino = request.POST.get("next") or request.GET.get("next")
    if destino and url_has_allowed_host_and_scheme(
            destino, allowed_hosts={request.get_host()}, require_https=request.is_secure()):
        return destino
    return resolve_url(settings.LOGIN_REDIRECT_URL)


@login_not_required
@sensitive_post_parameters("password")
@csrf_protect
@never_cache
def login(request):
    if request.user.is_authenticated:
        return redirect(settings.LOGIN_REDIRECT_URL)

    form = LoginForm(request, data=request.POST or None)
    if request.method == "POST" and form.is_valid():
        auth_login(request, form.usuario_autenticado)  # genera un id de sesión nuevo
        return redirect(_destino_seguro(request))

    return render(request, "login/login.html", {
        "form": form,
        "next": request.POST.get("next") or request.GET.get("next", ""),
    })


@login_not_required
@sensitive_post_parameters("password1", "password2")
@csrf_protect
@never_cache
def registro(request):
    if request.user.is_authenticated:
        return redirect(settings.LOGIN_REDIRECT_URL)

    form = RegistroForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Cuenta creada. Ya podés ingresar.")
        return redirect("login:login")

    return render(request, "login/registro.html", {"form": form})


@require_POST
def logout(request):
    auth_logout(request)
    messages.info(request, "Cerraste sesión.")
    return redirect("login:login")
