"""docstring"""
from django.urls import path

from rest_framework import urlpatterns
from rest_framework.urlpatterns import format_suffix_patterns
from Recoleccion import views

urlpatterns = [
    path('seleccionaDonaciones/',
        views.DonacionesSinRecoleccionList.as_view(),
        name='selecciona_donaciones'),

    path('seleccionaDonaciones/creaRecoleccion/',
        views.RecoleccionesCreate.as_view(), 
        name='crea_recoleccion'),

    path('recolecciones/',
         views.RecoleccionList.as_view(),
         name='lista_recoleccion'),

    path('recolecciones/<int:pk>/',
         views.RecoleccionDetail.as_view(),
         name='detalle-institucion'),

    path('recoleccion/generaRuta/(pk_recoleccion)/',
        views.GenerarRutaRecoleccion.as_view(),
        name='generacion-ruta-recoleccion')
]