from django.shortcuts import render
from rest_framework import generics
from login.models import Donante
from login.serializers import DonanteSerializer, UserSerializer
from django.contrib.auth.models import User

# Create your views here.
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