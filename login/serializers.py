from django.contrib.auth.models import User
from typing_extensions import Required
from rest_framework import serializers
from rest_framework.utils.field_mapping import needs_label
from login.models import Donante, Institucion, CodigoRecuperacion

class DonanteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Donante
        fields = '__all__'

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
        fields = '__all__'

class EmailSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=255)

class CodigoRecuperacionSerializer(serializers.ModelSerializer):
    class Meta:
        model = CodigoRecuperacion
        fields = ['email','usuario']

    def create(self, validated_data):
        print('METODO CREATE DE SERIALIZER')
        print(validated_data)
        print('fin de metodo')
        codigo_recuperacion = self.Meta.model(
            email=validated_data['email'],
            usuario=validated_data['usuario'],
        )
        codigo_recuperacion.save()
        return codigo_recuperacion
