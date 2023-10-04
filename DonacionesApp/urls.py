"""docstring"""
from django.urls import path

from rest_framework import urlpatterns
from rest_framework.urlpatterns import format_suffix_patterns
from DonacionesApp import views

urlpatterns = [
#Usuario: Donación
    path('eligeInstitucion/',
        views.InstitucionesList.as_view(),
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

    path('cancelarDonacion/<int:pk>/',
        views.CancelarDonacion.as_view(),
        name='cancelar_donacion'),

    path('cancelarTransferencia/<int:pk>/',
        views.CancelarTransferencia.as_view(),
        name='cancelar_transferencia'),

# Informes
    path('listadoDonaciones/',          
    views.DonacionesDonanteList.as_view(),
    name='listado_donaciones_realizadas'),

    path('listadoDonaciones/<int:pk>/',          
    views.DonacionesDonanteDetail.as_view(),
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

    path('entregarDonacion/<int:pk>/',
        views.EntregarDonacionUpdate.as_view(),
        name='entregar_donacion'),

## Necesidades de las instituciones

    path('crearNecesidad/',
         views.NecesidadCreate.as_view(),
         name='crear_necesidad'),

    path('modificarNecesidad/<int:pk>/',
         views.NecesidadUpdate.as_view(),
         name='modificar_necesidad'),

    path('necesidades/',
         views.NecesidadesList.as_view(),
         name='necesidades'),
    
    path('necesidadCumplida/<int:pk>/',
         views.CumplirNecesidadUpdate.as_view(),
         name='cumplirNecesidad'),

    path('kpiInstitucion/',
         views.CalculoKpisInstitucion.as_view(),
         name='KPIs'),

    path('kpiDonante/',
         views.CalculoKpisDonante.as_view(),
         name='KPIs'),
]

# urlpatterns = format_suffix_patterns(urlpatterns)