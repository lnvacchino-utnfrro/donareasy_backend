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


class DonacionesSinRecoleccionList(generics.ListAPIView):
    """
    Me traigo las donaciones que tienen estado "creadas" o "aceptadas y que no
    tienen asociada niguna recolección previamente creada por algún cadete
    """
    serializer_class = VerDonacionSerializer
    queryset = DonacionBienes.objects.filter(cod_estado = 1).filter(recoleccion__isnull=True)


class RecoleccionesCreate(generics.CreateAPIView):
    """docstring"""
    serializer_class = RecoleccionesCreateSerializer
    queryset = Recoleccion.objects.all()


class RecoleccionList(generics.ListAPIView):
    """APIView para listar las recolecciones creadas"""
    queryset = Recoleccion.objects.all()
    serializer_class = RecoleccionSerializer


class RecoleccionDetail(generics.RetrieveUpdateDestroyAPIView):
    """APIView para recuperar, actualizar y destruir una instancia de la clase Recoleccion"""
    queryset = Recoleccion.objects.all()
    serializer_class = RecoleccionSerializer


class GenerarRutaRecoleccion(APIView):
    """docstring"""
    def get(self,request,pk_recoleccion):
        """docstring"""
        recoleccion = Recoleccion.objects.get(id=pk_recoleccion)

        # si la recoleccion no existe, devolver error

        donaciones = DonacionBienes.objects.all()

        # Si no existen donaciones, devolver error

        for donacion in donaciones:
            recoleccion_donacion = donacion.recoleccion
            if recoleccion_donacion.id == recoleccion.id:
                #Agregarlo a una lista de donaciones

        # si la lista está vacía, devolver error
        
        # Acá va el proceso de ordenamiento de donaciones para la generación de las rutas

        return Response({'':''}, status = status.HTTP_200_OK)
