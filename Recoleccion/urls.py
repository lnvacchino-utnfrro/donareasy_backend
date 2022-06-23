"""docstring"""
from django.urls import path

from rest_framework import urlpatterns
from rest_framework.urlpatterns import format_suffix_patterns
from Recoleccion import views
from DonacionesApp.views import VerDonacion

urlpatterns = [
    path('seleccionaDonaciones/',
        VerDonacion.as_view(), #Muestra la lista de instituciones para seleccionar 1 
        name='selecciona_donaciones'),

    path('seleccionaDonaciones/creaRecoleccion/',
        views.RecoleccionesCreate.as_view(), 
        name='crea_recoleccion'),
]