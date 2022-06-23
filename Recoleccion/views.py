from django.shortcuts import render

from rest_framework import generics

from Recoleccion.models import Recoleccion
from Recoleccion.serializers import RecoleccionSerializer

class DonanteList(generics.ListAPIView):
    """APIView para listar las recolecciones creadas"""
    queryset = Recoleccion.objects.all()
    serializer_class = RecoleccionSerializer