from django.urls import path
from .views import pagos_total, pago_detalle, pago_crear, pago_borrar

app_name = 'pagos'

app_name = 'pagos'

urlpatterns = [
    path('', pagos_total, name="pagos_total"),
    path('<int:pk>/', pago_detalle, name="pago_detalle"),
    path('crear/', pago_crear, name="pago_crear"),
    path('borrar/<int:pk>', pago_borrar, name="pago_borrar")
]