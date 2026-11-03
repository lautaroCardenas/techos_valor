from django.urls import path
from .views import ajustes, ajustes_borrar

app_name = 'ajustes'

urlpatterns = [
    path('', ajustes, name="ajustes"),
    path('borrar/<str:tipo>/<int:pk>/', ajustes_borrar, name="ajustes_borrar")
]