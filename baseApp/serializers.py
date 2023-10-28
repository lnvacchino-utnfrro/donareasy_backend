"""Archivo para generar Serializadores"""
from django.contrib.auth.models import User

from rest_framework import serializers

from baseApp.models import Cadete, Donante, Institucion

# pylint: disable=too-few-public-methods
class UserEmailSerializer(serializers.ModelSerializer):
    """Correo electrónico de un usuario"""
    class Meta:
            model = User
            fields = ['email']

class DonanteSerializer(serializers.ModelSerializer):
    """Serializador para el modelo Donante"""
    usuario = UserEmailSerializer()

    class Meta:
        # pylint: disable=missing-class-docstring
        model = Donante
        fields = '__all__'


class InstitucionSerializer(serializers.ModelSerializer):
    """Serializador para el modelo Institucion"""
    usuario = UserEmailSerializer()

    class Meta:
        # pylint: disable=missing-class-docstring
        model = Institucion
        exclude = ('codigo_habilitacion',)


class CadeteSerializer(serializers.ModelSerializer):
    """Serializador para el modelo Cadete"""
    class Meta:
        # pylint: disable=missing-class-docstring
        model = Cadete
        fields = '__all__'


class DonanteSinForeingKeySerializer(serializers.ModelSerializer):
    """
    Serializador para el modelo Donante sin incluir la Clave Foránea
    que lo relaciona con la clase User
    """
    class Meta:
        # pylint: disable=missing-class-docstring
        model = Donante
        exclude = ('usuario',)


class InstitucionSinForeingKeySerializer(serializers.ModelSerializer):
    """
    Serializador para el modelo institución sin incluir la Clave Foránea
    que lo relaciona con la clase User
    """
    class Meta:
        # pylint: disable=missing-class-docstring
        model = Institucion
        exclude = ('usuario','codigo_habilitacion')


class CadeteSinForeingKeySerializer(serializers.ModelSerializer):
    """
    Serializador para el modelo Cadete sin incluir la Clave Foránea
    que lo relaciona con la clase User
    """
    class Meta:
        # pylint: disable=missing-class-docstring
        model = Cadete
        exclude = ('usuario',)
