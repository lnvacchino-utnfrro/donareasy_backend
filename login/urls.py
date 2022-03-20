"""docstring"""
from django.urls import path

from rest_framework import urlpatterns
from rest_framework.urlpatterns import format_suffix_patterns

from login import auth, views

urlpatterns = [
    path('',
        auth.Login.as_view(),
        name='login'),
    path('logout/',
        auth.Logout.as_view(),
        name='logout'),
    path('logup/',
        views.UserCreate.as_view(),
        name='logup'),
    path('logup/donante/',
        views.DonanteCreate.as_view(),
        name='donante-create'),
    path('logup/institucion/',
        views.InstitucionCreate.as_view(),
        name='institucion-create'),
    path('recuperacion/',
        auth.RecuperacionContrasenia.as_view(),
        name='recuperacion_contrasenia'),
    path('recuperacion/<str:code>/',
        auth.CambiarContraseniaRecuperada.as_view(),
        name='cambiar_contrasenia_recuperada'),
    path('cambioClave/',
        auth.CambioContrasenia.as_view(),
        name='cambiar_contrasenia')
]

urlpatterns = format_suffix_patterns(urlpatterns)
