from django.contrib.auth.models import User
from typing_extensions import Required
from rest_framework import serializers
from rest_framework.utils.field_mapping import needs_label
from login.models import Donante, Institucion

class DonanteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Donante
<<<<<<< HEAD
        fields = ['id', 'nombre', 'apellido','usuario']

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','username','first_name','last_name','email','password','groups']

class UserAuthSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username','email','first_name','last_name']

class InstitucionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Institucion
        fields = ['id', 'nombre', 'usuario']
=======
        fields = ['id', 'nombre', 'apellido', 'email', 'edad'] 
>>>>>>> e1dfdaf (Se completaron los demás métodos para el ABM de Donantes)
