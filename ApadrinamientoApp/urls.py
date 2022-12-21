"""docstring"""
from django.urls import path

from rest_framework import urlpatterns
from rest_framework.urlpatterns import format_suffix_patterns
from ApadrinamientoApp import views
#from DonacionesApp.views import *
#from Recoleccion.views import RecoleccionList

urlpatterns = [
        #* Institución crea chico
        path('altaChico/',
        views.ChicosCreate.as_view(),
        name='alta_chico'),

        #* Alta de la solicitud de apadrinamiento de la FS
        path('solicitud/',
        views.SolicitudCreate.as_view(),
        name='alta_solicitud'),

        #* Revisión de la solicitud por parte de la institución
        path('solicitudes/',
        views.SolicitudList.as_view(),
        name='revisa_solicitudes'),

        #* Institución elige una solicitud del listado
        path('solicitudes/<int:pk>/',
        views.EligeSolicitud.as_view(),
        name='elige_solicitud'),

        #* Institución acepta o rechaza la solicitud elegida
        path('solicitudes/<int:pk>/aceptar/',
        views.AceptaSolicitud.as_view(),
        name='acepta_solicitud'),

        #* Listado de chicos pertenecientes a una institucion en particular
        path('institucion/<int:pk>/chicos/',
        views.ChicosInstitucionList.as_view(),
        name='chicos_institucion'),

]