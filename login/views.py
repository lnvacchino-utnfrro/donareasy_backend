"""docstring"""
from django.contrib.auth.models import User, Group

from rest_framework import generics,status
from rest_framework.views import APIView
from rest_framework.response import Response

from drf_yasg.utils import swagger_auto_schema

from login.serializers import UserSerializer, DonanteUserSerializer, InstitucionUserSerializer, \
                              GroupSerializer, CadeteUserSerializer

from baseApp.models import Cadete, Donante, Institucion
from baseApp.serializers import DonanteSerializer, InstitucionSerializer

# pylint: disable=no-member

class UserCreate(generics.CreateAPIView):
    """docstring"""
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    """docstring"""
    queryset = User.objects.all()
    serializer_class = UserSerializer


class DonanteCreate(generics.CreateAPIView):
    """docstring"""
    queryset = Donante.objects.all()
    serializer_class = DonanteSerializer


class InstitucionCreate(generics.CreateAPIView):
    """docstring"""
    queryset = Institucion.objects.all()
    serializer_class = InstitucionSerializer


class DonanteUserCreate(generics.CreateAPIView):
    """docstring"""
    queryset = Donante.objects.all()
    serializer_class = DonanteUserSerializer


class InstitucionUserCreate(generics.CreateAPIView):
    """docstring"""
    queryset = Institucion.objects.all()
    serializer_class = InstitucionUserSerializer


class CadeteUserCreate(generics.CreateAPIView):
    """docstring"""
    queryset = Cadete.objects.all()
    serializer_class = CadeteUserSerializer


class groupLinkList(APIView):
    """docstring"""
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
