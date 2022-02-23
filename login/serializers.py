from multiprocessing.sharedctypes import Value
from re import M
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from typing_extensions import Required
from rest_framework import serializers
from rest_framework.utils.field_mapping import needs_label
from login.models import CodigoRecuperacion

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','username','first_name','last_name','email','password','groups']

class UserAuthSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username','email','first_name','last_name']

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

class UserPasswordSerializer(serializers.Serializer):
    password1 = serializers.CharField(max_length=255)
    password2 = serializers.CharField(max_length=255)
    username = serializers.CharField(max_length=255)
    
    def save(self, **kwargs):
        print('CREATE')
        print('validated_data')
        user = User.objects.get(username=self.validated_data['username'])
        user.set_password(self.validated_data['password1'])
        CodigoRecuperacion.objects.filter(usuario=user).filter(activo=1).delete()
        user.save()
        return user
    
    def validate_password1(self,value):
        print('VALIDATE_PASSWORD')
        validate_password(value)
        return value
    
    def validate_password2(self,value):
        print('VALIDATE_PASSWORD_VALIDATE - ',value)
        validate_password(value)
        return value

    def validate(self, attrs):
        print('attrs-password - ',attrs)
        print(attrs['password1'])
        print('UPS... ALGO PASÓ ACÁ')
        if attrs['password1']!=attrs['password2']:
            raise serializers.ValidationError('Las contraseñas ingresadas no son iguales')
        return super().validate(attrs)

# class PasswordSerializer(serializers.ModelSerializer):
#     password = serializers.CharField(max_length=255)
#     password_validate = serializers.CharField(max_length=255)

#     class Meta:
#         fields = ['password','password_validate']

# class RecuperarContraseñaSerializer(serializers.Serializer):
#     new_password1 = serializers.CharField(max_length=128, write_only=True, required=True)
#     new_password2 = serializers.CharField(max_length=128, write_only=True, required=True)

#     def validate(self, data):
#         if data['new_password1'] != data['new_password2']:
#             raise serializers.ValidationError({'new_password2': "The two password fields didn't match."})
#         password_validation.validate_password(data['new_password1'], self.context['request'].user)
#         return data

#     def save(self, **kwargs):
#         password = self.validated_data['new_password1']
#         user = self.context['request'].user
#         user.set_password(password)
#         user.save()
#         return user