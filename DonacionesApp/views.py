
from rest_framework.authentication import BasicAuthentication 
from rest_framework import generics
from rest_framework.permissions import IsAdminUser

from DonacionesApp.serializers import *
from DonacionesApp.models import Donacion, DonacionBienes, DonacionMonetaria, Bien
from donareasy.utils import CsrfExemptSessionAuthentication

from baseApp.models import Donante, Institucion
from baseApp.serializers import InstitucionSerializer
from baseApp.permissions import IsInstitucionPermission, IsDonantePermission

# Create your views here.

class InstitucionesList(generics.ListAPIView):
    """
    Se devuelven todas las instituciones que existen para elegir uno para la
    donación a realizar
    """
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)
    queryset = Institucion.objects.all()
    serializer_class = InstitucionSerializer
    # # permission_classes = [IsDonantePermission|IsAdminUser]


class DonacionBienesCreate(generics.CreateAPIView):
    """
    Carga de todos los bienes a donar por el donante para la institución elegida
    por el donante en la página anterior.
    En el campo 'institucion' se debe indicar el id de la institución seleccionada.
    """
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)
    queryset = DonacionBienes.objects.all()
    serializer_class = DonacionBienesSerializer
    # permission_classes = [IsDonantePermission|IsAdminUser]


class DonacionBienesDetail(generics.RetrieveUpdateDestroyAPIView):
    """docstring"""
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)
    queryset = DonacionBienes.objects.all()
    serializer_class = DonacionBienesSerializer


class BienesList(generics.RetrieveAPIView):
    """docstring"""
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)
    queryset = Bien.objects.all()
    serializer_class = BienesSerializer


class DonacionDetail(generics.RetrieveAPIView):
    """docstring"""
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)
    # serializer_class = ActualizarEstadoDonacionSerializer
    serializer_class = DonacionesSerializer
    # permission_classes = [IsInstitucionPermission|IsAdminUser]
    # def retrieve(self,request):
    #     queryset = self.get_object()
    #     serializer = DonacionBienesSerializer(queryset)
    #     return Response(serializer.data)

    def get_queryset(self):
        user = self.request.user
        if user.groups.filter(pk=2).exists():
            institucion = Institucion.objects.get(usuario=user)
            queryset = DonacionBienes.objects.filter(cod_estado = 1).filter(institucion=institucion)
        return queryset


class AceptarDonacion(generics.UpdateAPIView):
    """Actualizar el estado de la donación como aceptado"""
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)
    serializer_class = AceptarDonacionSerializer
    permission_classes = [IsInstitucionPermission|IsAdminUser]

    def get_queryset(self):
        user = self.request.user
        if user.groups.filter(pk=2).exists():
            return DonacionBienes.objects.filter(cod_estado=1).filter(institucion=user.usuario_institucion)



class RechazarDonacion(generics.UpdateAPIView):
    """Actualizar el estado de la donación como aceptado"""
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)
    serializer_class = RechazarDonacionSerializer
    # permission_classes = [IsInstitucionPermission|IsAdminUser]

    def get_queryset(self):
        user = self.request.user
        if user.groups.filter(pk=2).exists():
            institucion = Institucion.objects.get(usuario=user)
            queryset = DonacionBienes.objects.filter(cod_estado = 1).filter(institucion=institucion)
        return queryset


class TodasDonacionesList(generics.ListAPIView):
    """Me traigo las donaciones que tienen estado 'creadas' o 'aceptadas'"""
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)
    serializer_class = DonacionesSerializer
    # queryset = DonacionBienes.objects.filter(cod_estado = 1) #or DonacionBienes.objects.filter(cod_estado = 2)
    # permission_classes = [IsInstitucionPermission|IsAdminUser]

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
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)
    serializer_class = InstitucionSerializer
    queryset = Institucion.objects.filter(cbu__isnull=False)
    # permission_classes = [IsDonantePermission|IsAdminUser]


class EligeInstitucionConCBU(generics.RetrieveAPIView):
    """
    Se devuelven los datos bancarios necesarios de la institución ingresada como
    parámetro en el GET para que el donante pueda realizar la transferencia
    bancaria a la institución
    """
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)
    serializer_class = DatosBancariosInstitucion
    queryset = Institucion.objects.filter(cbu__isnull=False)
    # permission_classes = [IsDonantePermission|IsAdminUser]


class DonacionMonetariaCreate(generics.CreateAPIView):
    """
    Genero una nueva donación monetaria con el monto indicado para la
    institución elegida por el donante en la página anterior.
    En el campo 'institucion' se debe indicar el id de la institución seleccionada.
    """
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)
    queryset = DonacionMonetaria.objects.all()
    serializer_class = DonacionMonetariaSerializer
    # permission_classes = [IsDonantePermission|IsAdminUser]


class VerDonacionMonetaria(generics.ListAPIView):
    """Lista de todas las donaciones monetarias"""   
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)
    serializer_class = VerTransferenciaSerializer
    # permission_classes = [IsInstitucionPermission|IsAdminUser]
    
    def get_queryset(self):
        user = self.request.user
        if user.groups.filter(pk=1).exists(): #institucion = Institucion.objects.get(usuario=user)
            return DonacionMonetaria.objects.filter(donante=user.usuario_donante)#.filter(cod_estado = 3)
        if user.groups.filter(pk=2).exists(): #institucion = Institucion.objects.get(usuario=user)
            return DonacionMonetaria.objects.filter(institucion=user.usuario_institucion)#.filter(cod_estado = 3)
        #return queryset


class TransferenciaDetail(generics.RetrieveAPIView):
    """Detalle de una donación moetaria"""
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)
    serializer_class = VerTransferenciaSerializer
    # permission_classes = [IsInstitucionPermission|IsAdminUser]

    def get_queryset(self):
        user = self.request.user
        if user.groups.filter(pk=2).exists(): #institucion = Institucion.objects.get(usuario=user)
            return DonacionMonetaria.objects.filter(cod_estado = 3).filter(institucion=user.usuario_institucion)
            

class AceptarTransferencia(generics.UpdateAPIView):
    """Actualizar el estado de la donación como aceptado"""
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)
    serializer_class = AceptarTransferenciaSerializer
    # permission_classes = [IsInstitucionPermission|IsAdminUser]

    def get_queryset(self):
        user = self.request.user
        if user.groups.filter(pk=2).exists(): #institucion = Institucion.objects.get(usuario=user)
            return DonacionMonetaria.objects.filter(cod_estado = 3).filter(institucion=user.usuario_institucion)
            
    
class RechazarTransferencia(generics.UpdateAPIView):
    """Actualizar el estado de la donación como rechazada"""
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)
    serializer_class = RechazarTransferenciaSerializer
    # permission_classes = [IsInstitucionPermission|IsAdminUser]

    def get_queryset(self):
        user = self.request.user
        if user.groups.filter(pk=2).exists():
            institucion = Institucion.objects.get(usuario=user)
            queryset = DonacionMonetaria.objects.filter(cod_estado = 3).filter(institucion=institucion)
        return queryset


class DonacionesDonanteList(generics.ListAPIView):
    """Lista todas las donaciones realizadas por un Donante"""
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)
    serializer_class = DonacionesGeneralesDonanteSeralizer
    # permission_classes = [IsDonantePermission|IsAdminUser]

    def get_queryset(self):
        user = self.request.user
        if user.groups.filter(pk=1).exists():
            queryset = DonacionBienes.objects.filter(donante=user.usuario_donante)
        elif user.groups.filter(pk=2).exists():
            queryset = DonacionBienes.objects.filter(institucion=user.usuario_institucion)
        return queryset

class CancelarDonacion(generics.UpdateAPIView):
    """Actualizar el estado de la donación como cancelada"""
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)
    serializer_class = CancelarDonacionSerializer
    # permission_classes = [IsInstitucionPermission|IsAdminUser]

    def get_queryset(self):
        user = self.request.user
        if user.groups.filter(pk=1).exists():
            donante = Donante.objects.get(usuario=user)
            queryset = Donacion.objects.filter(cod_estado=1).filter(donante=donante)
        return queryset

class CancelarTransferencia(generics.UpdateAPIView):
    """Actualizar el estado de la donación como cancelada"""
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)
    serializer_class = CancelarDonacionSerializer
    # permission_classes = [IsInstitucionPermission|IsAdminUser]

    def get_queryset(self):
        user = self.request.user
        if user.groups.filter(pk=1).exists():
            donante = Donante.objects.get(usuario=user)
            queryset = Donacion.objects.filter(cod_estado=3).filter(donante=donante)
        return queryset

#? Necesidades en desarrollo

class NecesidadCreate(generics.CreateAPIView):
    """
    Creacion de necesidades para la institucion
    """
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)
    queryset = Necesidad.objects.all()
    serializer_class = NecesidadSerializer
    # permission_classes = [IsDonantePermission|IsAdminUser]

class NecesidadUpdate(generics.UpdateAPIView):
    """
    Actualizacion de necesidades para la institucion
    """
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)
    queryset = Necesidad.objects.all()
    serializer_class = ModificarNecesidadSerializer

    def get_queryset(self):
        user = self.request.user
        if user.groups.filter(pk=2).exists():
            return Necesidad.objects.filter(institucion=user.usuario_institucion)
        
class NecesidadesList(generics.ListAPIView):
    """Lista todas las donaciones realizadas por un Donante"""
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)
    serializer_class = NecesidadSerializer
    # permission_classes = [IsDonantePermission|IsAdminUser]

    def get_queryset(self):
        user = self.request.user
        if user.groups.filter(pk=1).exists():
            queryset = Necesidad.objects.filter(donante=user.usuario_donante)
        elif user.groups.filter(pk=2).exists():
            queryset = Necesidad.objects.filter(institucion=user.usuario_institucion)
        return queryset