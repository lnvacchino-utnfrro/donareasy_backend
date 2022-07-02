from django.shortcuts import render
from requests import Response
from rest_framework import generics
from rest_framework import viewsets
from rest_framework import permissions
from DonacionesApp.serializers import *
from DonacionesApp.models import Donacion, DonacionBienes, DonacionMonetaria, Bien
from baseApp.models import Donante, Institucion
from baseApp.serializers import DonanteSerializer, InstitucionSerializer
from Recoleccion.serializers import *

class RecoleccionesCreate(generics.CreateAPIView):
    """docstring"""
    serializer_class = RecoleccionesCreateSerializer
    queryset = Recoleccion.objects.all()

class DonanteList(generics.ListAPIView):
    """APIView para listar las recolecciones creadas"""
    queryset = Recoleccion.objects.all()
    serializer_class = RecoleccionSerializer
