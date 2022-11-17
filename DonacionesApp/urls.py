"""docstring"""
from django.urls import path

from rest_framework import urlpatterns
from rest_framework.urlpatterns import format_suffix_patterns
from DonacionesApp import views

urlpatterns = [
    path('eligeInstitucion/',
        views.InstitucionesList.as_view(), #Muestra la lista de instituciones para seleccionar 1 
        name='instituciones_list'),

    path('eligeInstitucion/donarBienes/',
        views.DonacionBienesCreate.as_view(),
        name='donacion_bienes'),

    path('eligeInstitucionConCBU/',
       views.InstitucionesListConCBU.as_view(),
       name='instituciones_list_cbu'),

    path('eligeInstitucionConCBU/<int:pk>/',
       views.EligeInstitucionConCBU.as_view(),
       name='institucion_elegida_cbu'),

    path('donarDinero/',
        views.DonacionMonetariaCreate.as_view(),
        name='donacion_monetaria'),

# Informes
    path('listadoDonaciones/',
    views.DonacionesDonanteList.as_view(),
    name='listado_donaciones_realizadas'),

#Usuario: Institucion
    path('donacionesPendientes/',
        views.TodasDonacionesList.as_view(),
        name='ver_donaciones'),

    path('donacionesPendientes/<int:pk>/',
        views.DonacionDetail.as_view(),
        name='ver_donacion'),

    path('donacionesPendientes/<int:pk>/aceptar/',
        views.AceptarDonacion.as_view(),
        name='aceptar_donacion'),
    
    path('donacionesPendientes/<int:pk>/rechazar/',
        views.RechazarDonacion.as_view(),
        name='rechazar_donacion'),

    path('transferenciasPendientes/',
        views.VerDonacionMonetaria.as_view(),
        name='ver_transferencias'),
    
    path('transferenciasPendientes/<int:pk>/',
        views.TransferenciaDetail.as_view(),
        name='ver_transferencia'),

    path('transferenciasPendientes/<int:pk>/aceptar/',
        views.AceptarTransferencia.as_view(),
        name='aceptar_donacion'),
    
    path('transferenciasPendientes/<int:pk>/rechazar/',
        views.RechazarTransferencia.as_view(),
        name='rechazar_donacion'),
]

# urlpatterns = format_suffix_patterns(urlpatterns)