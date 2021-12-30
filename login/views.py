from django.shortcuts import render
from rest_framework import generics
from login.models import Donante
from login.serializers import DonanteSerializer

# Create your views here.
class DonanteList(generics.ListCreateAPIView):
    queryset = Donante.objects.all()
    serializer_class = DonanteSerializer

class DonanteDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Donante.objects.all()
    serializer_class = DonanteSerializer
