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

# PRUEBA 2
class UserSystemCreate(generics.CreateAPIView):
    """docstring"""
    group = 0

    def get_serializer_class(self):
        print('SERIALIZADOR')
        if self.group == 1:
            return UsuarioDonanteSerializer
        elif self.group == 2:
            return UsuarioDonanteSerializer

    def get_queryset(self):
        print('queryset')
        if self.group == 1:
            obj = Donante
        elif self.group == 2:
            obj = Institucion
        return obj.objects.all()

    def create(self, request):
        # print(request.data['groups'][0])
        self.group = request.data['groups'][0]
        self.serializer_class = self.get_serializer_class(self)
        print('SERIALIZADOR: ',self.serializer_class)
        self.queryset = self.get_queryset(self)
        return self.create(request)

