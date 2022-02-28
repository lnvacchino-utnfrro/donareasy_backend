from django.urls import path, include
from rest_framework import urlpatterns
from login import auth, views
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework import renderers
from rest_framework.routers import DefaultRouter

urlpatterns = [
    path('',auth.Login.as_view(),name='login'),
    path('logout/',auth.Logout.as_view(),name='logout'),
    path('logup/', views.UserCreate.as_view(), name='logup'),
    path('logup/donante/', views.DonanteCreate.as_view(), name='donante-create'),
    path('logup/institucion/', views.InstitucionCreate.as_view(), name='institucion-create'),
    path('recuperacion/',auth.RecuperacionContraseña.as_view(), name='recuperacion_contraseña'),
    path('recuperacion/<str:code>/',auth.CambiarContraseñaRecuperada.as_view(), name='cambiar_contraseña_recuperada')
]

urlpatterns = format_suffix_patterns(urlpatterns)