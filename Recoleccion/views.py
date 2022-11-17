from django.shortcuts import render
from django.core.exceptions import ObjectDoesNotExist
from requests import Response
from rest_framework import generics, status, mixins
from rest_framework.views import APIView
from rest_framework.permissions import IsAdminUser

from rest_framework import viewsets
from rest_framework import permissions
from DonacionesApp.serializers import *
from DonacionesApp.models import Donacion, DonacionBienes, DonacionMonetaria, Bien, Recoleccion
from baseApp.models import Donante, Institucion
from baseApp.serializers import DonanteSerializer, InstitucionSerializer
from baseApp.permissions import IsInstitucionPermission, IsDonantePermission, IsCadetePermission
from Recoleccion.serializers import *


class DonacionesSinRecoleccionList(generics.ListAPIView):
    """
    Me traigo las donaciones que tienen estado "aceptadas" y que no
    tienen asociada niguna recolección previamente creada por algún cadete
    """
    serializer_class = DonacionesSerializer
    queryset = DonacionBienes.objects.filter(cod_estado = 2).filter(recoleccion__isnull=True)
    permission_classes = [IsCadetePermission|IsAdminUser]
    

class RecoleccionesCreate(generics.CreateAPIView):
    """docstring"""
    serializer_class = RecoleccionesCreateSerializer
    queryset = Recoleccion.objects.all()
    permission_classes = [IsCadetePermission|IsAdminUser]


class RecoleccionList(generics.ListAPIView):
    """APIView para listar las recolecciones creadas"""
    #queryset = Recoleccion.objects.all()
    serializer_class = RecoleccionSerializer
    permission_classes = [IsCadetePermission|IsAdminUser]

    def get_queryset(self):
        user = self.request.user
        if user.groups.filter(pk=3).exists():
            cadete = Cadete.objects.get(usuario=user)
            queryset = Recoleccion.objects.filter(estado_recoleccion = 1).filter(cadete=cadete)
        return queryset



class RecoleccionDetail(generics.RetrieveUpdateDestroyAPIView):
    """APIView para recuperar, actualizar y destruir una instancia de la clase Recoleccion"""
    #queryset = Recoleccion.objects.all()
    serializer_class = RecoleccionSerializer
    permission_classes = [IsCadetePermission|IsAdminUser]
    def get_queryset(self):
        user = self.request.user
        if user.groups.filter(pk=3).exists():
            cadete = Cadete.objects.get(usuario=user)
            queryset = Recoleccion.objects.filter(estado_recoleccion = 1).filter(cadete=cadete)
        return queryset

#Actualizo el estado de la recolección a 2 cuando la quiero comenzar a realizar
class RecoleccionComenzarUpdate(generics.UpdateAPIView):
    """Actualizo el estado de la recolección a 2 cuando la quiero comenzar a realizar y generar la ruta"""
    serializer_class = RecoleccionComenzarSerializer
    permission_classes = [IsCadetePermission|IsAdminUser]
    def get_queryset(self):
        user = self.request.user
        if user.groups.filter(pk=3).exists():
            cadete = Cadete.objects.get(usuario=user)
            queryset = Recoleccion.objects.filter(estado_recoleccion = 1).filter(cadete=cadete)
        return queryset

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

#Esta vista sirve para ver el detalle de la donación dentro de una recolección para luego cambiar el estado
class RecoleccionDonacionDetail(generics.RetrieveAPIView): #mixins.ListModelMixin,viewsets.GenericViewSet):
    """docstring"""   
    serializer_class = RecoleccionDonacionDetailSerializer
    #queryset = DonacionBienes.objects.all()
    permission_classes = [IsCadetePermission|IsAdminUser]
    def get_queryset(self):
        user = self.request.user
        if user.groups.filter(pk=3).exists():
            cadete = Cadete.objects.get(usuario=user)
            recoleccion = Recoleccion.objects.filter(estado_recoleccion = 2).filter(cadete=cadete)
            queryset = DonacionBienes.objects.filter(cod_estado = 5).filter(recoleccion__in=recoleccion)
        return queryset

class ActualizaRecogerDonacion(generics.UpdateAPIView):
    """docstring"""   
    serializer_class = RecogerDonacionSerializer
    permission_classes = [IsCadetePermission|IsAdminUser]
    def get_queryset(self):
        user = self.request.user
        if user.groups.filter(pk=3).exists():
            cadete = Cadete.objects.get(usuario=user)
            recoleccion = Recoleccion.objects.filter(estado_recoleccion = 2).filter(cadete=cadete)
            queryset = DonacionBienes.objects.filter(cod_estado = 5).filter(recoleccion__in=recoleccion)
        return queryset

class ActualizaRechazarDonacion(generics.UpdateAPIView):
    """docstring"""   
    serializer_class = RechazarDonacionSerializer
    permission_classes = [IsCadetePermission|IsAdminUser]
    def get_queryset(self):
        user = self.request.user
        if user.groups.filter(pk=3).exists():
            cadete = Cadete.objects.get(usuario=user)
            recoleccion = Recoleccion.objects.filter(estado_recoleccion = 2).filter(cadete=cadete)
            queryset = DonacionBienes.objects.filter(cod_estado = 5).filter(recoleccion__in=recoleccion)
        return queryset
        

class RecoleccionList2(generics.ListAPIView):
    serializer_class = RecoleccionListSerializer
    permission_classes = [IsCadetePermission|IsAdminUser]
    def get_queryset(self):
        user = self.request.user
        if user.groups.filter(pk=3).exists():
            cadete = Cadete.objects.get(usuario=user)
            queryset = Recoleccion.objects.filter(estado_recoleccion = 2).filter(cadete=cadete)
        return queryset


class EstadoRecoleccionFinalizadaUpdate(generics.UpdateAPIView):
    serializer_class = FinalizaRecoleccionSerializer
    permission_classes = [IsCadetePermission|IsAdminUser]
    def get_queryset(self):
        user = self.request.user
        if user.groups.filter(pk=3).exists():
            cadete = Cadete.objects.get(usuario=user)
            queryset = Recoleccion.objects.filter(estado_recoleccion = 2).filter(cadete=cadete)
        return queryset


class EstadoRecoleccionNoFinalizadaUpdate(generics.UpdateAPIView):
    serializer_class = NoFinalizaRecoleccionSerializer
    permission_classes = [IsCadetePermission|IsAdminUser]
    def get_queryset(self):
        user = self.request.user
        if user.groups.filter(pk=3).exists():
            cadete = Cadete.objects.get(usuario=user)
            queryset = Recoleccion.objects.filter(estado_recoleccion = 2).filter(cadete=cadete)
        return queryset

