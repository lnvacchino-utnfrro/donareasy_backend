"""docstring"""
from django.core.exceptions import ObjectDoesNotExist

from django.contrib.auth.models import User, Group

from rest_framework.authentication import BasicAuthentication 
from rest_framework import generics,status
from rest_framework.views import APIView
from rest_framework.response import Response

from drf_yasg.utils import swagger_auto_schema

from donareasy.utils import CsrfExemptSessionAuthentication

from login.serializers import UserSerializer, DonanteUserSerializer, InstitucionUserSerializer, \
                              GroupSerializer, CadeteUserSerializer, LogupDonanteUserSerializer, \
                              LogupInstitucionUserSerializer, LogupCadeteUserSerializer, \
                              InstitucionNoHabilitadaSerializer

from baseApp.models import Cadete, Donante, Institucion
from baseApp.serializers import DonanteSerializer, InstitucionSerializer

# pylint: disable=no-member

class UserCreate(generics.CreateAPIView):
    """docstring"""
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    """docstring"""
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)
    queryset = User.objects.all()
    serializer_class = UserSerializer


class DonanteCreate(generics.CreateAPIView):
    """docstring"""
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)
    queryset = Donante.objects.all()
    serializer_class = DonanteSerializer


class InstitucionCreate(generics.CreateAPIView):
    """docstring"""
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)
    queryset = Institucion.instituciones_habilitadas()
    serializer_class = InstitucionSerializer


class DonanteUserCreate(generics.CreateAPIView):
    """docstring"""
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)
    queryset = Donante.objects.all()
    serializer_class = LogupDonanteUserSerializer


class InstitucionUserCreate(generics.CreateAPIView):
    """docstring"""
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)
    queryset = Institucion.instituciones_habilitadas()
    serializer_class = LogupInstitucionUserSerializer


class CadeteUserCreate(generics.CreateAPIView):
    """docstring"""
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)
    queryset = Cadete.objects.all()
    serializer_class = LogupCadeteUserSerializer


class groupLinkList(APIView):
    """docstring"""
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)
    serializer_class = GroupSerializer

    def get(*args, **kwargs):
        """docstring"""
        grupos_data = []
        grupos = Group.objects.all()
        for grupo in grupos:
            grupo_data = {
                'id': grupo.id,
                'url': '127.0.0.1:8000/login/logup/'+grupo.name+'/'
            }
            grupos_data.append(grupo_data)
        return Response({'data':grupos_data},
                        status=status.HTTP_200_OK)


# class InstitucionesNoHabilitadasList(generics.ListAPIView):
#     authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)
#     queryset = Institucion.objects.filter(habilitado=False)
#     serializer_class = InstitucionNoHabilitadaSerializer


class InstitucionNoHabilitadaUpdate(APIView):
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)
    #queryset = Institucion.objects.filter(habilitado=False)
    serializer_class = InstitucionNoHabilitadaSerializer

    def post(self,request,*args,**kwargs):
        """"""
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            codigo_habilitacion = serializer.validated_data['codigo_habilitacion']
            try:
                institucion = Institucion.objects.get(codigo_habilitacion=codigo_habilitacion)
            except ObjectDoesNotExist:
                return Response({"Mensaje": "Codigo de habilitacion incorrecto"},
                                    status=status.HTTP_400_BAD_REQUEST)
            
            if not institucion.habilitado:
                institucion.habilitado = True
                institucion.save()
                return Response({"Mensaje": "Su institucion ya fue habilitada con EXITO"},
                                    status=status.HTTP_200_OK)
            else:
                return Response({"Mensaje": "La institucion ya se encuentra habilitada"},
                                    status=status.HTTP_400_BAD_REQUEST)
