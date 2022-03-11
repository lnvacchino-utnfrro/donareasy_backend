"""docstring"""
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password

from rest_framework import serializers

from login.models import CodigoRecuperacion

# pylint: disable=no-member

class UserSerializer(serializers.ModelSerializer):
    """docstring"""
    class Meta:
        # pylint: disable=missing-class-docstring
        model = User
        fields = ['id','username','first_name','last_name','email','password','groups']


class UserAuthSerializer(serializers.ModelSerializer):
    """docstring"""
    class Meta:
        # pylint: disable=missing-class-docstring
        model = User
        fields = ['username','email','first_name','last_name']


class EmailSerializer(serializers.Serializer):
    """docstring"""
    email = serializers.EmailField(max_length=255)


class CodigoRecuperacionSerializer(serializers.ModelSerializer):
    """docstring"""
    class Meta:
        # pylint: disable=missing-class-docstring
        model = CodigoRecuperacion
        fields = ['email','usuario']

    def create(self, validated_data):
        """docstring"""
        codigo_recuperacion = self.Meta.model(
            email=validated_data['email'],
            usuario=validated_data['usuario'],
        )
        codigo_recuperacion.save()
        return codigo_recuperacion.codigo


class UserPasswordSerializer(serializers.Serializer):
    """docstring"""
    password1 = serializers.CharField(max_length=255)
    password2 = serializers.CharField(max_length=255)
    username = serializers.CharField(max_length=255)

    def save(self):
        """docstring"""
        user = User.objects.get(username=self.validated_data['username'])
        user.set_password(self.validated_data['password1'])
        CodigoRecuperacion.objects.filter(usuario=user).filter(activo=1).delete()
        user.save()
        return user

    def validate_password1(self,value):
        """docstring"""
        validate_password(value)
        return value

    def validate_password2(self,value):
        """docstring"""
        validate_password(value)
        return value

    def validate(self,attrs):
        """docstring"""
        if attrs['password1']!=attrs['password2']:
            raise serializers.ValidationError('Las contraseñas ingresadas no son iguales')
        return super().validate(attrs)

# class PasswordSerializer(serializers.ModelSerializer):
#     password = serializers.CharField(max_length=255)
#     password_validate = serializers.CharField(max_length=255)

#     class Meta:
#         fields = ['password','password_validate']

class CambioContraseniaSerializer(serializers.Serializer):
    old_password = serializers.CharField(max_length=128, write_only=True, required=True)
    new_password1 = serializers.CharField(max_length=128, write_only=True, required=True)
    new_password2 = serializers.CharField(max_length=128, write_only=True, required=True)

    def validate(self, data):
        password1 = data['new_password1']
        password2 = data['new_password2']
        if password1 != password2:
            raise serializers.ValidationError({
                                          'new_password2': "Las dos contraseñas ingresadas no coinciden."
                                      })
        validate_password(password1)
        validate_password(password2)
        return data

    def save(self, **kwargs):
        password = self.validated_data['new_password1']
        user = self.context['request'].user
        user.set_password(password)
        user.save()
        return user
