from django.urls import path
from .views import ajustes, ajustes_borrar, ajustes_pdf, ajustes_pdf_vista_previa

app_name = 'ajustes'

urlpatterns = [
    path('', ajustes, name="ajustes"),
    path('borrar/<str:tipo>/<int:pk>/', ajustes_borrar, name="ajustes_borrar"),
    path('pdf/', ajustes_pdf, name="ajustes_pdf"),
    path('pdf/vista-previa/', ajustes_pdf_vista_previa, name="ajustes_pdf_vista_previa"),
]
