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

class UserList(generics.ListCreateAPIView):
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