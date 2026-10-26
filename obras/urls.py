from django.urls import path
from .views import obras_total, obra_detalle, obra_crear

app_name = 'obras'

urlpatterns = [
    path('', obras_total, name="obras_total"),
    path('crear/', obra_crear, name="obra_crear"),
    path('<int:pk>/', obra_detalle, name="obra_detalle")
]