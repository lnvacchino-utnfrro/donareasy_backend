"""Archivo para generar Serializadores"""
from rest_framework import serializers

from DonacionesApp.serializers import DonacionBienesSerializer

from Recoleccion.models import Recoleccion

# pylint: disable=too-few-public-methods

class RecoleccionSerializer(serializers.ModelSerializer):
    # donante = DonanteSerializer(many = True),
    # institucion = InstitucionSerializer()  
    donaciones = DonacionBienesSerializer(many=True)
    class Meta:
        model = Recoleccion
        fields = '__all__'
        # read_only_fields = ['cod_estado','fecha_creacion']