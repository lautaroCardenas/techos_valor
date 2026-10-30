from django.urls import path
from .views import presupuesto_crear, presupuestos_total, presupuesto_detalle

app_name = 'presupuestos'

app_name = 'presupuestos'

urlpatterns = [
    path('', presupuestos_total, name="presupuestos_total"),
    path('crear/', presupuesto_crear, name="presupuesto_crear"),
    path('<int:pk>/', presupuesto_detalle, name="presupuesto_detalle")
]