from django.urls import path
from .views import presupuesto_crear, presupuestos_total, presupuesto_detalle, presupuesto_borrar, presupuesto_actualizar, presupuesto_editar_form   

app_name = 'presupuestos'

app_name = 'presupuestos'

urlpatterns = [
    path('', presupuestos_total, name="presupuestos_total"),
    path('crear/', presupuesto_crear, name="presupuesto_crear"),
    path('<int:pk>/', presupuesto_detalle, name="presupuesto_detalle"),
    path('borrar/<int:pk>/', presupuesto_borrar, name="presupuesto_borrar"),
    path('actualizar/<int:pk>/', presupuesto_actualizar, name="presupuesto_actualizar"),
    path('editar/<int:pk>/', presupuesto_editar_form, name="presupuesto_editar_form")
]