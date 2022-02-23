from django.shortcuts import render
from rest_framework import generics
from baseApp.models import Donante, Institucion
from baseApp.serializers import DonanteSerializer, InstitucionSerializer

class DonanteList(generics.ListCreateAPIView):
    queryset = Donante.objects.all()
    serializer_class = DonanteSerializer

class DonanteDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Donante.objects.all()
    serializer_class = DonanteSerializer

class InstitucionList(generics.ListCreateAPIView):
    queryset = Institucion.objects.all()
    serializer_class = InstitucionSerializer

class InstitucionDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Institucion.objects.all()
    serializer_class = InstitucionSerializer
