"""Vistas para ABM de modelos."""

from rest_framework import generics

from baseApp.models import Cadete, Donante, Institucion
from baseApp.serializers import CadeteSerializer, DonanteSerializer, InstitucionSerializer

# pylint: disable=no-member

class DonanteList(generics.ListCreateAPIView):
    """APIView para listar y crear instancias de la clase Donante"""
    queryset = Donante.objects.all()
    serializer_class = DonanteSerializer


class DonanteDetail(generics.RetrieveUpdateDestroyAPIView):
    """APIView para recuperar, actualizar y destruir una instancia de la clase Donante"""
    queryset = Donante.objects.all()
    serializer_class = DonanteSerializer


class InstitucionList(generics.ListCreateAPIView):
    """APIView para listar y crear instancias de la clase Institucion"""
    queryset = Institucion.objects.all()
    serializer_class = InstitucionSerializer


class InstitucionDetail(generics.RetrieveUpdateDestroyAPIView):
    """APIView para recuperar, actualizar y destruir una instancia de la clase Institucion"""
    queryset = Institucion.objects.all()
    serializer_class = InstitucionSerializer


class CadeteList(generics.ListCreateAPIView):
    """APIView para listar y crear instancias de la clase Cadete"""
    queryset = Cadete.objects.all()
    serializer_class = CadeteSerializer


class CadeteDetail(generics.RetrieveUpdateDestroyAPIView):
    """APIView para recuperar, actualizar y destruir una instancia de la clase Cadete"""
    queryset = Cadete.objects.all()
    serializer_class = CadeteSerializer
