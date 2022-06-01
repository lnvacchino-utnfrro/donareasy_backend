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

class InstitucionesListConCBU(generics.ListAPIView):
    serializer_class = InstitucionSerializer
    def get_queryset(self):
        return Institucion.objects.filter(cbu__isnull=False)

class EligeInstitucionConCBU(generics.RetrieveAPIView):
    serializer_class = DatosBancariosInstitucion
    def get_queryset(self):
        return Institucion.objects.filter(cbu__isnull=False)

class DonacionMonetariaCreate(generics.CreateAPIView):
    """docstring"""
    queryset = DonacionMonetaria.objects.all()
    serializer_class = DonacionMonetariaSerializer

class VerDonacionMonetaria(generics.ListAPIView):
    """docstring"""   
    serializer_class = VerTransferenciaSerializer
    def get_queryset(self):
        return DonacionMonetaria.objects.filter(cod_estado = 3)

class AceptarTransferencia(generics.UpdateAPIView):
    """docstring"""
    serializer_class = AceptarTransferenciaSerializer
    def get_queryset(self):
        return DonacionMonetaria.objects.filter(cod_estado = 3)