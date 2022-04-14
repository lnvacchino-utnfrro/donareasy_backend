"""docstring"""
from django.urls import path

from rest_framework import urlpatterns
from rest_framework.urlpatterns import format_suffix_patterns
from DonacionesApp import views

urlpatterns = [
    path('/eligeInstitucion',
        views.InstitucionesList.as_view(), #Muestra la lista de instituciones para seleccionar 1 
        name='instituciones_list'),

    path('/eligeInstitucion/donarBienes',
        views.DonacionBienesCreate.as_view(),
        name='donacion_bienes'),
    
    path('/eligeInstitucion/donarBienes/bien',
        views.BienesCreate.as_view(),
        name='crear_bienes'),

  ##  path('/eligeInstitucion/donarDinero',
  ##      views.DonacionMonetaria.as_view(),
  ##      name='donacion_monetaria')
]

urlpatterns = format_suffix_patterns(urlpatterns)