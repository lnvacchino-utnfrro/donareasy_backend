from django.shortcuts import render
from rest_framework import generics
from rest_framework import viewsets
from rest_framework import permissions
from DonacionesApp.serializers import *
from DonacionesApp.models import Donacion, DonacionBienes, DonacionMonetaria, Bien
from baseApp.models import Donante, Institucion
from baseApp.serializers import DonanteSerializer, InstitucionSerializer
from DonacionesApp import serializers
# Create your views here.

class InstitucionesList(generics.ListAPIView):
    """docstring"""
    queryset = Institucion.objects.all()
    serializer_class = InstitucionSerializer

class DonacionBienesCreate(generics.CreateAPIView):
    """docstring"""
    queryset = DonacionBienes.objects.all()
    serializer_class = DonacionBienesSerializer

class DonacionBienesDetail(generics.RetrieveUpdateDestroyAPIView):
    """docstring"""
    queryset = DonacionBienes.objects.all()
    serializer_class = DonacionBienesSerializer

class BienesCreate(generics.CreateAPIView):
    """docstring"""
    queryset = Bien.objects.all()
    serializer_class = BienesSerializer

class BienesList(generics.RetrieveAPIView):
    """docstring"""
    queryset = Bien.objects.all()
    serializer_class = BienesSerializer

class AceptarDonacion(generics.UpdateAPIView):
    """docstring"""
    queryset = DonacionBienes.objects.all()
    serializer_class = AceptarDonacionSerializer

class VerDonacion(generics.ListAPIView):
    """docstring"""   
    serializer_class = VerDonacionSerializer
    def get_queryset(self):
        return DonacionBienes.objects.filter(cod_estado = 1) #or DonacionBienes.objects.filter(cod_estado = 2)
        # Me traigo las donaciones que tienen estado "creadas" o "aceptadas"
