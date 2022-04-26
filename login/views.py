"""docstring"""
from django.contrib.auth.models import User

from rest_framework import generics

from login.serializers import UserSerializer, UsuarioSistemaSerializer, UsuarioDonanteSerializer

from baseApp.models import Donante, Institucion
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


# Prueba 1
class DonanteUserCreate(generics.CreateAPIView):
    """docstring"""
    queryset = Donante.objects.all()
    serializer_class = UsuarioDonanteSerializer

# PEBA 2
class UserSystemCreate(generics.CreateAPIView):
    """docstring"""

    def get_serializer_class(self):
        if self.request.user.is_staff:
            return FullAccountSerializer
        return BasicAccountSerializer

    def create(self, request):
        print(request.data)
        return