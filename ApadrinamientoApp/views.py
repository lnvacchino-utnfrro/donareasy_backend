from operator import contains
from django.shortcuts import render
from django.core.exceptions import ObjectDoesNotExist
from requests import Response
from rest_framework import generics, status, mixins
from rest_framework.views import APIView

from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser
from ApadrinamientoApp.models import *
from baseApp.models import *
from baseApp.permissions import IsInstitucionPermission, IsDonantePermission
from ApadrinamientoApp.serializers import *

# Create your views here.

class ChicosCreate(generics.CreateAPIView):
    """Doy de alta un nuevo chico/a dentro de la institución"""
    serializer_class = ChicosCreateSerializer
    queryset = Chicos.objects.all()
    permission_classes = [IsInstitucionPermission|IsAdminUser]

class SolicitudCreate(generics.CreateAPIView):
    """Doy de alta una nueva solicitud de apadrinamiento"""
    serializer_class = SolicitudCreateSerializer
    queryset = SolicitudApadrinamiento.objects.all()
    permission_classes = [IsDonantePermission|IsAdminUser]

class SolicitudList(generics.ListAPIView):
    """Muestra listado de solicitudes a la institución logueada"""
    serializer_class = SolicitudListSerializer
    #queryset = SolicitudApadrinamiento.objects.filter(cod_estado = 1)
    permission_classes = [IsInstitucionPermission|IsAdminUser]

    def get_queryset(self):
        user = self.request.user
        if user.groups.filter(pk=2).exists():
            institucion = Institucion.objects.get(usuario=user)
            chico = Chicos.objects.filter(institucion = institucion)
            queryset = SolicitudApadrinamiento.objects.filter(cod_estado = 1).filter(chico_apadrinado__in = chico)
        return queryset

class EligeSolicitud(generics.RetrieveAPIView): 
    """Hace como una pre-visualización para luego presionar "continuar" y aceptar la solicitud o cancelarla"""
    serializer_class = EligeSolicitudSerializer
    queryset = SolicitudApadrinamiento.objects.filter(cod_estado = 1)
    permission_classes = [IsInstitucionPermission|IsAdminUser]
    
class AceptaSolicitud(generics.UpdateAPIView): 
    """Aceptación o rechazo de la solicitud enviada"""
    serializer_class = AceptaSolicitudSerializer
    #queryset = SolicitudApadrinamiento.objects.all()
    permission_classes = [IsInstitucionPermission|IsAdminUser]

    def get_queryset(self):
        user = self.request.user
        if user.groups.filter(pk=2).exists():
            institucion = Institucion.objects.get(usuario=user)
            chico = Chicos.objects.filter(institucion = institucion)
            queryset = SolicitudApadrinamiento.objects.filter(cod_estado = 1).filter(chico_apadrinado__in = chico)
        return queryset

class ChicosList(generics.ListAPIView):
    """Listado de Chicos asociados a la intitución pasada como parámetro en la URL"""
    serializer_class = ChicosSerializer
    # permission_classes = ALL
    queryset = Chicos.objects.all()

class ChicosInstitucionList(generics.RetrieveAPIView):
    """Listado de Chicos asociados a la intitución pasada como parámetro en la URL"""
    serializer_class = ChicosInstitucionSerializer
    # permission_classes = ALL
    queryset = Institucion.objects.all()
