"""docstring"""
from django.urls import path

from rest_framework import urlpatterns
from rest_framework.urlpatterns import format_suffix_patterns
from DonacionesApp import views

urlpatterns = [
    path('/eligeInstitucion/',
        views.InstitucionesList.as_view(), #Muestra la lista de instituciones para seleccionar 1 
        name='instituciones_list'),

    path('/eligeInstitucion/donarBienes/',
        views.DonacionBienesCreate.as_view(),
        name='donacion_bienes'),

    path('/InstitucionConCBU/',
       views.InstitucionesListConCBU.as_view(),
       name='instituciones_list_cbu'),

    path('/InstitucionConCBU/elegida/<int:pk>/',
       views.EligeInstitucionConCBU.as_view(),
       name='institucion_elegida_cbu'),

    path('/donarDinero/',
        views.DonacionMonetariaCreate.as_view(),
        name='donacion_monetaria'),

#Usuario: Institucion
    path('/eligeDonacion/',
        views.VerDonacion.as_view(),
        name='ver_donacion'),

    path('/eligeDonacion/aceptar/<int:pk>/',
        views.AceptarDonacion.as_view(),
        name='aceptar_donacion'),
    
    path('/verTransferencia/',
        views.VerDonacionMonetaria.as_view(),
        name='ver_transferencia'),
    
    path('/verTransferencia/aceptar/<int:pk>/',
        views.AceptarTransferencia.as_view(),
        name='aceptar_transferencia'),
]

urlpatterns = format_suffix_patterns(urlpatterns)