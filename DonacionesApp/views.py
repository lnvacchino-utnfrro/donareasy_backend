
from rest_framework import generics
from rest_framework.permissions import IsAdminUser

from DonacionesApp.serializers import *
from DonacionesApp.models import Donacion, DonacionBienes, DonacionMonetaria, Bien

from baseApp.models import Donante, Institucion
from baseApp.serializers import InstitucionSerializer
from baseApp.permissions import IsInstitucionPermission, IsDonantePermission

# Create your views here.

class InstitucionesList(generics.ListAPIView):
    """
    Se devuelven todas las instituciones que existen para elegir uno para la
    donación a realizar
    """
    queryset = Institucion.objects.all()
    serializer_class = InstitucionSerializer
    permission_classes = [IsDonantePermission|IsAdminUser]


class DonacionBienesCreate(generics.CreateAPIView):
    """
    Carga de todos los bienes a donar por el donante para la institución elegida
    por el donante en la página anterior.
    En el campo 'institucion' se debe indicar el id de la institución seleccionada.
    """
    queryset = DonacionBienes.objects.all()
    serializer_class = DonacionBienesSerializer
    permission_classes = [IsDonantePermission|IsAdminUser]


class DonacionBienesDetail(generics.RetrieveUpdateDestroyAPIView):
    """docstring"""
    queryset = DonacionBienes.objects.all()
    serializer_class = DonacionBienesSerializer


class BienesList(generics.RetrieveAPIView):
    """docstring"""
    queryset = Bien.objects.all()
    serializer_class = BienesSerializer


class DonacionDetail(generics.RetrieveUpdateAPIView):
    """docstring"""
    queryset = DonacionBienes.objects.all()
    serializer_class = ActualizarEstadoDonacionSerializer
    permission_classes = [IsInstitucionPermission|IsAdminUser]
    # def retrieve(self,request):
    #     queryset = self.get_object()
    #     serializer = DonacionBienesSerializer(queryset)
    #     return Response(serializer.data)


class TodasDonacionesList(generics.ListAPIView):
    """Me traigo las donaciones que tienen estado 'creadas' o 'aceptadas'"""
    serializer_class = DonacionesSerializer
    # queryset = DonacionBienes.objects.filter(cod_estado = 1) #or DonacionBienes.objects.filter(cod_estado = 2)
    permission_classes = [IsInstitucionPermission|IsAdminUser]

    def get_queryset(self):
        user = self.request.user
        if user.groups.filter(pk=2).exists():
            institucion = Institucion.objects.get(usuario=user)
            queryset = DonacionBienes.objects.filter(cod_estado = 1).filter(institucion=institucion)
        return queryset


class InstitucionesListConCBU(generics.ListAPIView):
    """
    Se devuelven todas las instituciones que tienen registrado el CBU bancario
    para elegir uno para la donación monetario a realizar
    """
    serializer_class = InstitucionSerializer
    queryset = Institucion.objects.filter(cbu__isnull=False)
    permission_classes = [IsDonantePermission|IsAdminUser]


class EligeInstitucionConCBU(generics.RetrieveAPIView):
    """
    Se devuelven los datos bancarios necesarios de la institución ingresada como
    parámetro en el GET para que el donante pueda realizar la transferencia
    bancaria a la institución
    """
    serializer_class = DatosBancariosInstitucion
    Institucion.objects.filter(cbu__isnull=False)
    permission_classes = [IsDonantePermission|IsAdminUser]


class DonacionMonetariaCreate(generics.CreateAPIView):
    """
    Genero una nueva donación monetaria con el monto indicado para la
    institución elegida por el donante en la página anterior.
    En el campo 'institucion' se debe indicar el id de la institución seleccionada.
    """
    queryset = DonacionMonetaria.objects.all()
    serializer_class = DonacionMonetariaSerializer
    permission_classes = [IsDonantePermission|IsAdminUser]


class VerDonacionMonetaria(generics.ListAPIView):
    """docstring"""   
    serializer_class = VerTransferenciaSerializer
    def get_queryset(self):
        return DonacionMonetaria.objects.filter(cod_estado = 3) #(Q(cod_estado = 1) | Q(cod_estado = 3))


class AceptarTransferencia(generics.UpdateAPIView):
    """docstring"""
    serializer_class = AceptarTransferenciaSerializer
    def get_queryset(self):
        return DonacionMonetaria.objects.filter(cod_estado = 3)