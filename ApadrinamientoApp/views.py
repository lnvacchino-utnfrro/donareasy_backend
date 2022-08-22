from django.shortcuts import render
from django.core.exceptions import ObjectDoesNotExist
from requests import Response
from rest_framework import generics, status, mixins
from rest_framework.views import APIView

from rest_framework import viewsets
from rest_framework import permissions
from ApadrinamientoApp.models import *
from baseApp.models import *
from ApadrinamientoApp.serializers import *
# Create your views here.

class ChicosCreate(generics.CreateAPIView):
    """Doy de alta un nuevo chico/a dentro de la institución"""
    serializer_class = ChicosCreateSerializer
    queryset = Chicos.objects.all()

class SolicitudCreate(generics.CreateAPIView):
    """Doy de alta una nueva solicitud de apadrinamiento"""
    serializer_class = SolicitudCreateSerializer
    queryset = SolicitudApadrinamiento.objects.all()

class SolicitudList(generics.ListAPIView):
    """Muestra listado de solicitudes a la institución logueada"""
    serializer_class = SolicitudListSerializer
    queryset = SolicitudApadrinamiento.objects.filter(cod_estado = 1)

class EligeSolicitud(generics.RetrieveAPIView): 
    """Hace como una pre-visualización para luego presionar "continuar" y aceptar la solicitud o cancelarla"""
    serializer_class = EligeSolicitudSerializer
    queryset = SolicitudApadrinamiento.objects.filter(cod_estado = 1)
    
class AceptaSolicitud(generics.UpdateAPIView): 
    """Aceptación o rechazo de la solicitud enviada"""
    serializer_class = AceptaSolicitudSerializer
    queryset = SolicitudApadrinamiento.objects.all()