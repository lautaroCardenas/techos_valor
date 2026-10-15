from django.urls import path
from .views import obras_total, obra_detalle

urlpatterns = [
    path('', obras_total, name="obras_total"),
    path('<int:pk>/', obra_detalle, name="obra_detalle")
]