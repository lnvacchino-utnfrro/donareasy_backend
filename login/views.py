from django.shortcuts import render
from rest_framework import generics
from login.models import Donante, Institucion
from login.serializers import DonanteSerializer, UserSerializer, InstitucionSerializer
from django.contrib.auth.models import User

class DonanteList(generics.ListCreateAPIView):
    queryset = Donante.objects.all()
    serializer_class = DonanteSerializer

class DonanteDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Donante.objects.all()
    serializer_class = DonanteSerializer

class UserCreate(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class InstitucionList(generics.ListCreateAPIView):
    queryset = Institucion.objects.all()
    serializer_class = InstitucionSerializer

class InstitucionDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Institucion.objects.all()
    serializer_class = InstitucionSerializer

# class UserCreate(generics.CreateAPIView):
#     #queryset = User.objects.all()
#     serializer_class = UserSerializer

#     def post(self,request):
#         serializer = self.serializer_class(data = request.data)

#* Lo que sigue son las vistas sólo para la creación de instituciones/donantes
class DonanteCreate(generics.CreateAPIView):
    queryset = Donante.objects.all()
    serializer_class = DonanteSerializer

class InstitucionCreate(generics.CreateAPIView):
    queryset = Institucion.objects.all()
    serializer_class = InstitucionSerializer
#* Fin ----



