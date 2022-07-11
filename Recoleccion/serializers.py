"""Archivo para generar Serializadores"""
from django.forms import IntegerField
from rest_framework import serializers
from DonacionesApp.models import DonacionBienes, Bien, DonacionMonetaria
from baseApp.serializers import DonanteSerializer,CadeteSerializer
from baseApp.models import Institucion, Cadete
from datetime import datetime,date
from DonacionesApp.serializers import DonacionBienesSerializer, BienesSerializer
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

class RecoleccionesDetailSerializer (serializers.ModelSerializer):
    class Meta:
        model = Recoleccion
        fields = ['id','cadete','fecha_recoleccion','hora_recoleccion']
        
class RecoleccionDonacionDetailSerializer(serializers.ModelSerializer):
    bienes = BienesSerializer(many=True)
    donante = DonanteSerializer()
    recoleccion = RecoleccionesDetailSerializer()
    class Meta:
        model = DonacionBienes
        fields = ['id','donante','recoleccion','bienes']

class RecoleccionListSerializer(serializers.ModelSerializer):
    cadete = CadeteSerializer()
    donaciones = DonacionBienesSerializer(many=True)
    class Meta:
        model = Recoleccion
        fields = ['id','cadete','fecha_recoleccion','hora_recoleccion','estado_recoleccion','donaciones']

class CambiaEstadoRecoleccionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recoleccion
        fields = ['id','estado_recoleccion','motivo_cancelacion']
        read_only_fields = ['fecha_cancelacion','fecha_finalizacion']

    #! Ver si acá mismo se actualiza el estado a "No Finalizado" (estado_recoleccion = 4) 
    def update(self,recoleccion,validated_data):
        if (validated_data['estado_recoleccion'] == 3):
            recoleccion.estado_recoleccion = validated_data.get('estado_recoleccion',recoleccion.estado_recoleccion)
            recoleccion.motivo_cancelacion = None
            recoleccion.fecha_cancelacion = None
            recoleccion.fecha_finalizacion = datetime.now()
            recoleccion.save()
        elif (validated_data['estado_recoleccion'] == 0):
            recoleccion.estado_recoleccion = validated_data.get('estado_recoleccion',recoleccion.estado_recoleccion)
            recoleccion.motivo_cancelacion = validated_data.get('motivo_cancelacion',recoleccion.motivo_cancelacion)
            recoleccion.fecha_cancelacion = datetime.now()
            recoleccion.fecha_finalizacion = None
            recoleccion.save()
        else:
            recoleccion.estado_recoleccion = 2
            recoleccion.motivo_cancelacion = None
            recoleccion.fecha_cancelacion = None
            recoleccion.fecha_finalizacion = None
            recoleccion.save()
        return recoleccion
