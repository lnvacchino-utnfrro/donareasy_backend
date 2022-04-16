"""Archivo para generar Serializadores"""
from rest_framework import serializers

from baseApp.models import Donante, Institucion

# pylint: disable=too-few-public-methods

class DonanteSerializer(serializers.ModelSerializer):
    """Serializador para el modelo Donante"""
    class Meta:
        # pylint: disable=missing-class-docstring
        model = Donante
        fields = '__all__'


class InstitucionSerializer(serializers.ModelSerializer):
    """Serializador para el modelo Institucion"""
    class Meta:
        # pylint: disable=missing-class-docstring
        model = Institucion
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
        exclude = ('usuario',)