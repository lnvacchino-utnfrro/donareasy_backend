"""docstring"""
from django.contrib.auth.models import User, Group

from rest_framework.authentication import BasicAuthentication 
from rest_framework import generics,status
from rest_framework.views import APIView
from rest_framework.response import Response

from drf_yasg.utils import swagger_auto_schema

from donareasy.utils import CsrfExemptSessionAuthentication

from login.serializers import UserSerializer, DonanteUserSerializer, InstitucionUserSerializer, \
                              GroupSerializer, CadeteUserSerializer, LogupDonanteUserSerializer, \
                              LogupInstitucionUserSerializer, LogupCadeteUserSerializer

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
