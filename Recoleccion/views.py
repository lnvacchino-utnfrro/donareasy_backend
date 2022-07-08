from django.shortcuts import render
from requests import Response
from rest_framework import generics,mixins
from rest_framework import viewsets
from rest_framework import permissions
from DonacionesApp.serializers import *
from DonacionesApp.models import Donacion, DonacionBienes, DonacionMonetaria, Bien, Recoleccion
from baseApp.models import Donante, Institucion
from baseApp.serializers import DonanteSerializer, InstitucionSerializer
from Recoleccion.serializers import *
# Create your views here.

class RecoleccionesCreate(generics.CreateAPIView):
    """docstring"""
    serializer_class = RecoleccionesCreateSerializer
    queryset = Recoleccion.objects.all()


class RecoleccionDonacionDetail(generics.RetrieveAPIView): #mixins.ListModelMixin,viewsets.GenericViewSet):
    """docstring"""   
    serializer_class = RecoleccionDonacionDetailSerializer
    #queryset = DonacionBienes.objects.all()
    def get_queryset(self):
        #recoleccion = Recoleccion.objects.all()
        donacion = DonacionBienes.objects.all()
        return donacion
        # Me traigo las donaciones que tienen estado "creadas" o "aceptadas"

class ActualizaEstadoDonacion(generics.UpdateAPIView):
    """docstring"""   
    serializer_class = AceptarDonacionSerializer
    queryset = DonacionBienes.objects.all()
        

class RecoleccionList(generics.ListAPIView):
    serializer_class = RecoleccionListSerializer
    def get_queryset(self):
        return Recoleccion.objects.filter(estado_recoleccion = 2)

class EstadoRecoleccionUpdate(generics.UpdateAPIView):
    serializer_class = CambiaEstadoRecoleccionSerializer
    def get_queryset(self):
        return Recoleccion.objects.filter(estado_recoleccion = 2)