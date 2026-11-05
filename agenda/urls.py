from django.urls import path
from .views import agenda, agenda_eventos, evento_crear, evento_borrar, evento_editar, evento_mover

app_name = 'agenda'

urlpatterns = [
   path('', agenda, name='agenda'),
   path('/agenda/eventos', agenda_eventos, name='agenda_eventos'),
   path("agenda/eventos/crear/", evento_crear, name="evento_crear"),
   path("agenda/eventos/<int:pk>/editar/", evento_editar, name="evento_editar"),
   path("agenda/eventos/<int:pk>/eliminar/", evento_borrar, name="evento_borrar"),
   path("agenda/eventos/<int:pk>/mover/", evento_mover, name="evento_mover"),
]