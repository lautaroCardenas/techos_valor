from django.urls import path
from .views import ajustes

app_name = 'ajustes'

urlpatterns = [
    path('', ajustes, name="ajustes"),
]