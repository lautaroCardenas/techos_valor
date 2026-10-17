"""
URL configuration for techos_valor project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from .views import not_found

handler404 = not_found

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('login.urls'), namespace="login"),
    path('obras/', include('obras.urls'), namespace="obras"),
    path('presupuestos/', include('presupuestos.urls'), namespace="presupuestos"),
    path('pagos/', include('pagos.urls'), namespace="pagos"),
    path('ajustes/', include('ajustes.urls'), namespace="ajustes")
]
