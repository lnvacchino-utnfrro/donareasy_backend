"""Archivo para generar Serializadores"""
from django.forms import IntegerField
from rest_framework import serializers
from DonacionesApp.models import DonacionBienes, Bien, DonacionMonetaria
from baseApp.serializers import DonanteSerializer,CadeteSerializer
from baseApp.models import Institucion, Cadete
from datetime import datetime,date
from DonacionesApp.serializers import DonacionBienesSerializer
from Recoleccion.models import Recoleccion

# pylint: disable=too-few-public-methods

class RecoleccionesCreateSerializer(serializers.ModelSerializer):
    serializers.PrimaryKeyRelatedField(many=True, queryset=DonacionBienes.objects.all())

    class Meta:
        model = Recoleccion
        fields = ['cadete','fecha_recoleccion','hora_recoleccion','donaciones']
        read_only_fields = ['estado_recoleccion']

    def create(self,validated_data):
        donaciones_data = validated_data.pop('donaciones')
        recoleccion = Recoleccion.objects.create(
            cadete = validated_data['cadete'],
            fecha_recoleccion = validated_data['fecha_recoleccion'],
            hora_recoleccion = validated_data['hora_recoleccion'],
            estado_recoleccion = 1     
        )
        recoleccion.save() 
        for donacion in donaciones_data:
            donacion.recoleccion = recoleccion
            donacion.fecha_retiro = recoleccion.fecha_recoleccion
            donacion.save()
            
        return recoleccion

class RecoleccionSerializer(serializers.ModelSerializer):
    donaciones = DonacionBienesSerializer(many=True, read_only=True)
    class Meta:
        model = Recoleccion
        fields = '__all__'
