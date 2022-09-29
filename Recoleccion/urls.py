"""docstring"""
from django.urls import path

from rest_framework import urlpatterns
from rest_framework.urlpatterns import format_suffix_patterns
from Recoleccion import views
#from DonacionesApp.views import *
from Recoleccion.views import RecoleccionList

urlpatterns = [
    path('seleccionaDonaciones/',
        views.DonacionesSinRecoleccionList.as_view(),
        name='selecciona_donaciones'),

    path('seleccionaDonaciones/creaRecoleccion/',
        views.RecoleccionesCreate.as_view(), 
        name='crea_recoleccion'),

    #path para paso 4 path('listaRecolecciones/')
    path('recolecciones/',
         views.RecoleccionList.as_view(),
         name='lista_recoleccion'),
    
    #path para paso 4 path('listaRecolecciones/detalleRecoleccion/<int:pk>')
    path('recolecciones/<int:pk>/',
         views.RecoleccionDetail.as_view(),
         name='detalle-institucion'),

    path('recolecciones/<int:pk>/comenzar',
         views.RecoleccionComenzarUpdate.as_view(),
         name='detalle-institucion'),
         
    #path para la generación de ruta (ACTUALMENTE NO ESTÁ DISPONIBLE)
    path('recoleccion/generaRuta/(pk_recoleccion)/',
        views.GenerarRutaRecoleccion.as_view(),
        name='generacion-ruta-recoleccion'),

    path('listaRecolecciones/detalleRecoleccion/detalleDonacion/<int:pk>/',
        views.RecoleccionDonacionDetail.as_view(),
        name='detalle_donacion_recoleccion'),

    path('listaRecolecciones/detalleRecoleccion/detalleDonacion/<int:pk>/recoger',
        views.ActualizaRecogerDonacion.as_view(),
        name='actualiza_acepta_recoleccion'),

    path('listaRecolecciones/detalleRecoleccion/detalleDonacion/<int:pk>/rechazar',
        views.ActualizaRechazarDonacion.as_view(),
        name='actualiza_rechaza_recoleccion'),

    #Path paso 6: listar recolecciones en proceso para finalizarla
    path('recoleccionEnProceso/',
    views.RecoleccionList2.as_view(),
    name = 'lista_recoleccion_en_proceso'),

    path('recoleccionEnProceso/<int:pk>/finalizadaExito',
    views.EstadoRecoleccionFinalizadaUpdate.as_view(),
    name = 'finalizar_recoleccion_en_proceso'),

    path('recoleccionEnProceso/<int:pk>/finalizadaSinExito',
    views.EstadoRecoleccionNoFinalizadaUpdate.as_view(),
    name = 'finalizar_recoleccion_en_proceso'),
]
