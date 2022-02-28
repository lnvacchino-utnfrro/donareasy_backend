from django.shortcuts import render
from rest_framework import generics
from baseApp.models import Donante, Institucion
from login.serializers import UserSerializer
from baseApp.serializers import DonanteSerializer, InstitucionSerializer
from django.contrib.auth.models import User

class UserCreate(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class DonanteCreate(generics.CreateAPIView):
    queryset = Donante.objects.all()
    serializer_class = DonanteSerializer

class InstitucionCreate(generics.CreateAPIView):
    queryset = Institucion.objects.all()
    serializer_class = InstitucionSerializer
