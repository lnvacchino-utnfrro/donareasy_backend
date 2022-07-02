from django.shortcuts import render
from requests import Response
from rest_framework import generics,mixins
from rest_framework import viewsets
from rest_framework import permissions
from DonacionesApp.serializers import *
from DonacionesApp.models import Donacion, DonacionBienes, DonacionMonetaria, Bien
from baseApp.models import Donante, Institucion
from baseApp.serializers import DonanteSerializer, InstitucionSerializer
from Recoleccion.serializers import *
# Create your views here.

class RecoleccionesCreate(generics.CreateAPIView):
    """docstring"""
    serializer_class = RecoleccionesCreateSerializer
    queryset = Recoleccion.objects.all()

class RecoleccionDetail(generics.RetrieveAPIView):
    serializer_class = RecoleccionesDetailSerializer
    queryset = Recoleccion.objects.all()

class RecoleccionDonacionDetail(generics.RetrieveAPIView): #mixins.ListModelMixin,viewsets.GenericViewSet):
    """docstring"""   
    serializer_class = RecoleccionDonacionDetailSerializer
    #queryset = DonacionBienes.objects.all()
    def get_queryset(self):
        recoleccion = Recoleccion.objects.all()
        donacion = DonacionBienes.objects.filter(recoleccion = recoleccion)
        return donacion
        # Me traigo las donaciones que tienen estado "creadas" o "aceptadas"