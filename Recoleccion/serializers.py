"""Archivo para generar Serializadores"""
from django.forms import IntegerField
from rest_framework import serializers
from DonacionesApp.models import DonacionBienes, Bien, DonacionMonetaria
from baseApp.serializers import DonanteSerializer,CadeteSerializer
from baseApp.models import Institucion, Cadete
from datetime import datetime,date
from DonacionesApp.serializers import DonacionBienesSerializer, BienesSerializer
from Recoleccion.models import Recoleccion #, Location

# from rest_framework_gis.serializers import GeoFeatureModelSerializer

# class LocationSerializer(GeoFeatureModelSerializer):
#     """ A class to serialize locations as GeoJSON compatible data """

#     class Meta:
#         model = Location
#         geo_field = "point"

#         # you can also explicitly declare which fields you want to include
#         # as with a ModelSerializer.
#         fields = ('id', 'address', 'city', 'state')

class RecoleccionesCreateSerializer(serializers.ModelSerializer):
    donaciones = serializers.PrimaryKeyRelatedField(many=True, queryset=DonacionBienes.objects.filter(cod_estado=2))

    class Meta:
        model = Recoleccion
        fields = ['fecha_recoleccion','hora_recoleccion','donaciones']
        read_only_fields = ['estado_recoleccion']

    def validate_donaciones(self,value):
        """ Valido que el listado de donaciones pertenezcan a la institución del cadete que esté logueado """
        usuario = self.context['request'].user
        cadete = Cadete.objects.get(usuario = usuario)
        institucion = Institucion.objects.get(cadete=cadete)
        for donacion in value:
            if donacion.institucion != institucion:
                raise serializers.ValidationError("No existen donaciones para esa institucion")
        return value
    

    def create(self,validated_data):
        usuario = self.context['request'].user
        donaciones_data = validated_data.pop('donaciones')
         
        if len(donaciones_data)==0:
            raise serializers.ValidationError("No se agregó ninguna donación a la recolección")

        else:
            recoleccion = Recoleccion.objects.create(
            cadete = Cadete.objects.get(usuario = usuario),
            fecha_recoleccion = validated_data['fecha_recoleccion'],
            hora_recoleccion = validated_data['hora_recoleccion'],
            estado_recoleccion = 1     
            )
            for donacion in donaciones_data:
                donacion.recoleccion = recoleccion
                donacion.fecha_retiro = recoleccion.fecha_recoleccion
                donacion.cod_estado = 5
                donacion.save()
            recoleccion.save()            
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

class RecoleccionComenzarSerializer (serializers.ModelSerializer):
    class Meta:
        model = Recoleccion
        fields = []

    def update(self,recoleccion,validated_data):
        recoleccion.estado_recoleccion = 2
        recoleccion.fecha_inicio_recoleccion = datetime.now()
        recoleccion.save()

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

class FinalizaRecoleccionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recoleccion
        fields = []

    def update(self,recoleccion,validated_data):
        recoleccion.estado_recoleccion = 3
        recoleccion.fecha_finalizacion = datetime.now()
        recoleccion.save()


class NoFinalizaRecoleccionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recoleccion
        fields = ['motivo_cancelacion']

    def update(self,recoleccion,validated_data):
        recoleccion.estado_recoleccion = 4
        recoleccion.motivo_cancelacion = validated_data.get('motivo_cancelacion',recoleccion.motivo_cancelacion)
        recoleccion.fecha_cancelacion = datetime.now()
        recoleccion.save()




# class CambiaEstadoRecoleccionSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Recoleccion
#         fields = ['id','estado_recoleccion','motivo_cancelacion']
#         read_only_fields = ['fecha_cancelacion','fecha_finalizacion']

#     #! Ver si acá mismo se actualiza el estado a "No Finalizado" (estado_recoleccion = 4) 
#     def update(self,recoleccion,validated_data):
#         if (validated_data['estado_recoleccion'] == 3):
#             recoleccion.estado_recoleccion = validated_data.get('estado_recoleccion',recoleccion.estado_recoleccion)
#             recoleccion.motivo_cancelacion = None
#             recoleccion.fecha_cancelacion = None
#             recoleccion.fecha_finalizacion = datetime.now()
#             recoleccion.save()
#         elif (validated_data['estado_recoleccion'] == 0):
#             recoleccion.estado_recoleccion = validated_data.get('estado_recoleccion',recoleccion.estado_recoleccion)
#             recoleccion.motivo_cancelacion = validated_data.get('motivo_cancelacion',recoleccion.motivo_cancelacion)
#             recoleccion.fecha_cancelacion = datetime.now()
#             recoleccion.fecha_finalizacion = None
#             recoleccion.save()
#         else:
#             recoleccion.estado_recoleccion = 2
#             recoleccion.motivo_cancelacion = None
#             recoleccion.fecha_cancelacion = None
#             recoleccion.fecha_finalizacion = None
#             recoleccion.save()
#         return recoleccion
