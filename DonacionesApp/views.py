from django.shortcuts import render
from rest_framework import generics
from rest_framework import viewsets
from rest_framework import permissions
from DonacionesApp.serializers import DonacionBienesSerializer, BienesSerializer, DonacionIdSerializer
from DonacionesApp.models import Donacion, DonacionBienes, DonacionMonetaria, Bien
from baseApp.models import Donante, Institucion
from baseApp.serializers import DonanteSerializer, InstitucionSerializer
from DonacionesApp import serializers
# Create your views here.

class InstitucionesList(viewsets.ModelViewSet):
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

class DonacionId(generics.RetrieveAPIView):
    """docstring"""
    queryset = DonacionBienes.objects.all() #Ver como devolver uno solo
    serializer_class = DonacionIdSerializer

class BienesCreate(generics.CreateAPIView):
    """docstring"""
    queryset = Bien.objects.all()
    serializer_class = BienesSerializer

class BienesList(generics.RetrieveAPIView):
    queryset = Bien.objects.all()
    serializer_class = BienesSerializer

