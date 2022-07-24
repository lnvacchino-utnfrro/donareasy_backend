"""docstring"""
from django.contrib.auth.models import User, UserManager, Group
from django.contrib.auth.password_validation import validate_password

from rest_framework import serializers

from baseApp.models import Cadete, Donante, Institucion
from baseApp.serializers import DonanteSinForeingKeySerializer

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


class CodigoSerializer(serializers.Serializer):
    """docstring"""
    codigo = serializers.CharField(max_length=255)


class CodigoRecuperacionSerializer(serializers.ModelSerializer):
    """docstring"""
    class Meta:
        # pylint: disable=missing-class-docstring
        model = CodigoRecuperacion
        fields = ['email','usuario']

    def create(self, validated_data):
        """parámetro validated_data es un dato tipo diccionario. Ya está validado"""
        codigo_recuperacion = self.Meta.model(
            email=validated_data['email'],
            usuario=validated_data['usuario'],
        )
        codigo_recuperacion.save()
        return codigo_recuperacion.codigo


class RecuperacionContraseniaSerializer(serializers.Serializer):
    """docstring"""
    password = serializers.CharField(max_length=255)
    id_user = serializers.IntegerField()

    def save(self):
        """docstring"""
        user = User.objects.get(id=self.validated_data['id_user'])
        user.set_password(self.validated_data['password'])
        CodigoRecuperacion.objects.filter(usuario=user).filter(activo=1).delete()
        user.save()
        return user

    def validate_password(self,value):
        """docstring"""
        validate_password(value)
        return value


class CambioContraseniaSerializer(serializers.Serializer):
    old_password = serializers.CharField(max_length=128, write_only=True, required=True)
    new_password = serializers.CharField(max_length=128, write_only=True, required=True)

    def validate_new_password(self,value):
        """docstring"""
        validate_password(value)
        return value


class DonanteUserSerializer(serializers.ModelSerializer):
    usuario = UserSerializer()

    class Meta:
        model = Donante
        fields = ['usuario','nombre','apellido','fecha_nacimiento','dni','domicilio','localidad','provincia',
        'pais','telefono','estado_civil','genero','ocupacion']

    def create(self, validated_data):
        usuario_data = validated_data.pop('usuario', None)
        usuario = User.objects.create_user(
            username=usuario_data['username'],
            email=usuario_data['email'],
            password=usuario_data['password'],
            first_name=usuario_data['first_name'],
            last_name=usuario_data['last_name']
        )
        usuario.groups.set(usuario_data['groups'])
        donante = Donante.objects.create(
            usuario=usuario,
            **validated_data
        )
        return donante


class InstitucionUserSerializer(serializers.ModelSerializer):
    usuario = UserSerializer()

    class Meta:
        model = Institucion
        fields = ['usuario','nombre','director','fecha_fundacion','domicilio',
                    'localidad','provincia','pais','telefono','cant_empleados',
                    'descripcion','cbu','cuenta_bancaria']

    def create(self, validated_data):
        usuario_data = validated_data.pop('usuario', None)
        usuario = User.objects.create_user(
            username=usuario_data['username'],
            email=usuario_data['email'],
            password=usuario_data['password'],
            first_name=usuario_data['first_name'],
            last_name=usuario_data['last_name']
        )
        usuario.groups.set(usuario_data['groups'])
        institucion = Institucion.objects.create(
            usuario=usuario,
            **validated_data
        ) 
        return institucion


class CadeteUserSerializer(serializers.ModelSerializer):
    usuario = UserSerializer()

    class Meta:
        model = Cadete
        fields = ['usuario','nombre','apellido','fecha_nacimiento','dni','domicilio','localidad','provincia',
        'pais','telefono','estado_civil','genero','ocupacion','medio_transporte']

    def create(self, validated_data):
        usuario_data = validated_data.pop('usuario', None)
        usuario = User.objects.create_user(
            username=usuario_data['username'],
            email=usuario_data['email'],
            password=usuario_data['password'],
            first_name=usuario_data['first_name'],
            last_name=usuario_data['last_name']
        )
        usuario.groups.set(usuario_data['groups'])
        cadete = Cadete.objects.create(
            usuario=usuario,
            **validated_data
        )
        return cadete


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ['id','name']


class TokenSerializer(serializers.Serializer):
    """docstring"""
    token = serializers.CharField(max_length=255)


class PublicUserSerializer(serializers.ModelSerializer):
    """docstring""" 
    class Meta:
        # pylint: disable=missing-class-docstring
        model = User
        fields = ['id','username','first_name','last_name']
