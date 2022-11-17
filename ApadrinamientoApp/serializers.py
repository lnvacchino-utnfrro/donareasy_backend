from django.forms import ValidationError
from rest_framework import serializers
from ApadrinamientoApp.models import *
from baseApp.serializers import DonanteSerializer, InstitucionSerializer
from baseApp.models import Institucion
from datetime import datetime,date

class ChicosSerializer (serializers.ModelSerializer):
    class Meta:
        model = Chicos
        fields = '__all__'

class ChicosCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chicos
        exclude = ['institucion']
    def create(self, validated_data):
        usuario = self.context['request'].user
        if (validated_data['edad'] < 18 and validated_data['edad'] >= 0):
            chico = Chicos.objects.create(
                nombre = validated_data['nombre'],
                apellido = validated_data['apellido'],
                edad = validated_data['edad'],
                fotografia = validated_data['fotografia'],
                descripcion = validated_data['descripcion'],
                institucion = Institucion.objects.get(usuario = usuario)
            )
            return chico
        else:
            raise serializers.ValidationError({'name': "El niño/a debe ser menor de edad."})

#!Editar luego el create a gusto
class SolicitudCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = SolicitudApadrinamiento
        exclude = ['fecha_aceptacion','fecha_cancelacion','motivo_cancelacion']
        read_only_fields = ['cod_estado','fecha_creacion']
    def create(self, validated_data):
        solicitud = SolicitudApadrinamiento.objects.create(
            cod_estado = 1,
            fecha_creacion = datetime.now(),
            dni_frente = validated_data['dni_frente'],
            dni_dorso = validated_data['dni_dorso'],
            recibo_sueldo = validated_data['recibo_sueldo'],
            acta_matrimonio = validated_data['acta_matrimonio'],
            visita = validated_data['visita'],
            fecha_visita = validated_data['fecha_visita'],
            chico_apadrinado = validated_data['chico_apadrinado']
        )
        return solicitud

class SolicitudListSerializer(serializers.ModelSerializer):
    chico_apadrinado = ChicosSerializer()
    class Meta:
        model = SolicitudApadrinamiento
        fields = ['id','motivo_FS','fecha_creacion','visita','fecha_visita','chico_apadrinado']

class EligeSolicitudSerializer(serializers.ModelSerializer):
    chico_apadrinado = ChicosSerializer()
    class Meta:
        model = SolicitudApadrinamiento
        exclude = ['cod_estado','fecha_aceptacion','fecha_cancelacion','motivo_cancelacion']

class AceptaSolicitudSerializer(serializers.ModelSerializer):
    class Meta:
        model = SolicitudApadrinamiento
        fields = ['cod_estado','motivo_cancelacion']
        read_only_fields = ['fecha_cancelacion','fecha_aceptacion']
    def update(self, solicitud, validated_data):
            if validated_data['cod_estado'] == 2:
                solicitud.cod_estado = validated_data.get('cod_estado',solicitud.cod_estado)
                solicitud.fecha_aceptacion = datetime.now()
                solicitud.fecha_cancelacion = None
                solicitud.motivo_cancelacion = None          
                solicitud.save()           
            elif validated_data['cod_estado'] == 0:
                solicitud.cod_estado = validated_data.get('cod_estado',solicitud.cod_estado)
                solicitud.fecha_aceptacion = None 
                solicitud.fecha_cancelacion = datetime.now()
                solicitud.motivo_cancelacion = validated_data.get('motivo_cancelacion',solicitud.motivo_cancelacion)
                solicitud.save()
            else:
                solicitud.cod_estado = 1
                solicitud.fecha_aceptacion = None 
                solicitud.fecha_cancelacion = None
                solicitud.motivo_cancelacion = None
                solicitud.save()       
            return solicitud