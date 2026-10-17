from django.urls import path
from .views import presupuestos_total, presupuesto_detalle

urlpatterns = [
    path('', presupuestos_total, name="presupuestos_total"),
    path('<int:pk>/', presupuesto_detalle, name="presupuesto_detalle")
]