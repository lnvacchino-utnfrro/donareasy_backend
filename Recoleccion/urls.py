"""docstring"""
from django.urls import path

from rest_framework import urlpatterns
from rest_framework.urlpatterns import format_suffix_patterns
from Recoleccion import views
from DonacionesApp.views import VerDonacion
from Recoleccion.views import RecoleccionList

urlpatterns = [
    path('seleccionaDonaciones/',
        VerDonacion.as_view(), #Muestra la lista de instituciones para seleccionar 1 
        name='selecciona_donaciones'),

    path('seleccionaDonaciones/creaRecoleccion/',
        views.RecoleccionesCreate.as_view(), 
        name='crea_recoleccion'),

    #path para paso 4 path('listaRecolecciones/')
    #path para paso 4 path('listaRecolecciones/detalleRecoleccion/<int:pk>')

    path('listaRecolecciones/detalleRecoleccion/detalleDonacion/<int:pk>/',
        views.RecoleccionDonacionDetail.as_view(),
        name='detalle_donacion_recoleccion'),

    path('listaRecolecciones/detalleRecoleccion/actualizaDonacion/<int:pk>/',
        views.ActualizaEstadoDonacion.as_view(),
        name='actualiza_donacion_recoleccion'),

    #Path paso 6: listar recolecciones en proceso para finalizarla
    path('recoleccionEnProceso/',
    views.RecoleccionList.as_view(),
    name = 'lista_recoleccion_en_proceso'),

    path('recoleccionEnProceso/finalizar/<int:pk>',
    views.EstadoRecoleccionUpdate.as_view(),
    name = 'finalizar_recoleccion_en_proceso')
]