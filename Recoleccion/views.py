from django.shortcuts import render
from django.core.exceptions import ObjectDoesNotExist
from requests import Response
from rest_framework import generics, status, mixins
from rest_framework.views import APIView

from rest_framework import viewsets
from rest_framework import permissions
from DonacionesApp.serializers import *
from DonacionesApp.models import Donacion, DonacionBienes, DonacionMonetaria, Bien, Recoleccion
from baseApp.models import Donante, Institucion
from baseApp.serializers import DonanteSerializer, InstitucionSerializer
from Recoleccion.serializers import *


class DonacionesSinRecoleccionList(generics.ListAPIView):
    """
    Me traigo las donaciones que tienen estado "creadas" o "aceptadas y que no
    tienen asociada niguna recolección previamente creada por algún cadete
    """
    serializer_class = DonacionesSerializer
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
        # Busco la Recolección según el código ingresado. Si no existe, retorno error
        try:
            recoleccion = Recoleccion.objects.get(id=pk_recoleccion)
        except ObjectDoesNotExist:
            return Response({'mensaje':'El código de recolección ingresado no existe'},
                            status=status.HTTP_400_BAD_REQUEST)

        # Busco cuáles de las donaciones están asociadas a la recolección encontrada
        lista_todas_donaciones = DonacionBienes.objects.all()
        # Si no existen donaciones, retorno error
        if len(lista_todas_donaciones) == 0:
            return Response({'mensaje':'No existen donaciones generadas'},
                            status=status.HTTP_400_BAD_REQUEST)
        # Recorro la lista de donaciones
        donaciones = []
        for donacion in lista_todas_donaciones:
            recoleccion_donacion = donacion.recoleccion
            if recoleccion_donacion.id == recoleccion.id:
                donaciones.append(donacion)

        # si no hay ninguna donación que esté asociada a la recolección encontrada, retorno error
        if len(donaciones) == 0:
            return Response({'mensaje':'No existen donaciones asociadas a la recolección'},
                            status=status.HTTP_400_BAD_REQUEST)

        # Acá va el proceso de ordenamiento de donaciones para la generación de las rutas

        return Response({'':''}, status = status.HTTP_200_OK)


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
    serializer_class = ActualizarEstadoDonacionSerializer
    queryset = DonacionBienes.objects.all()
        

class RecoleccionList(generics.ListAPIView):
    serializer_class = RecoleccionListSerializer
    def get_queryset(self):
        return Recoleccion.objects.filter(estado_recoleccion = 2)

class EstadoRecoleccionUpdate(generics.UpdateAPIView):
    serializer_class = CambiaEstadoRecoleccionSerializer
    def get_queryset(self):
        return Recoleccion.objects.filter(estado_recoleccion = 2)
