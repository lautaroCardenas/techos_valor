from django.urls import path
from .views import login, logout, registro

app_name = 'login'

urlpatterns = [
    path('', login, name="login"),
    path('registro/', registro, name="registro"),
    path('salir/', logout, name="logout"),
]
