from django.urls import path
from .views import pagos_total, pago_detalle

urlpatterns = [
    path('', pagos_total, name="pagos_total"),
    path('<int:pk>/', pago_detalle, name="pago_detalle")
]