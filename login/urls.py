"""Urls, módulo logging"""
from django.urls import path

from rest_framework import urlpatterns
from rest_framework.urlpatterns import format_suffix_patterns

from login import auth, views

urlpatterns = [
    # CASO BÁSICO
    path('',
        auth.Login.as_view(),
        name='login'),
    # EXTRA
    path('logout/',
        auth.Logout.as_view(),
        name='logout'),
    # CAMINO ALTERNATIVO A
    path('recuperacion/',
        auth.GenerarCodigoRecuperacionContrasenia.as_view(),
        name='recuperacion_contrasenia'),
    path('recuperacion/codigo/',
        auth.ValidarCodigoRecuperacionContrasenia.as_view(),
        name='validar_codigo_recuperacion'),
    path('recuperacion/cambioClave/',
        auth.RecuperacionContrasenia.as_view(),
        name='cambiar_contrasenia_recuperada'),
    # CAMINO EXTRA
    path('cambioClave/',
        auth.CambioContrasenia.as_view(),
        name='cambiar_contrasenia'),
    # CAMINO ALTERNATIVO B
    path('logup/donante/',
        views.DonanteUserCreate.as_view(),
        name='donante-create'),
    path('logup/institucion/',
        views.InstitucionUserCreate.as_view(),
        name='institucion-create'),
    path('logup/cadete/',
        views.CadeteUserCreate.as_view(),
        name='cadete-create'),
    path('logup/',
        views.groupLinkList.as_view(),
        name='logup'),    
]   

# urlpatterns = format_suffix_patterns(urlpatterns)
