from rest_framework import serializers
from DonacionesApp.models import DonacionBienes, Bien, DonacionMonetaria
from Recoleccion.models import *
from baseApp.serializers import DonanteSerializer,CadeteSerializer
from baseApp.models import Institucion, Cadete
from datetime import datetime,date
from DonacionesApp.serializers import DonacionBienesSerializer

class RecoleccionesCreateSerializer(serializers.ModelSerializer):
     donacion = DonacionBienesSerializer(many=True)
     cadete = CadeteSerializer()
     class Meta:
         model = Recoleccion
         fields = ['cadete','fecha_recoleccion','hora_recoleccion','donacion']
         #read_only_fields = ['estado_recoleccion']

    #  def create(self,validated_data):
    #     donaciones_data = validated_data.pop('donacion')
    #     recoleccion = Recoleccion.objects.create(
    #          cadete = validated_data['cadete'],
    #          fecha_recoleccion = validated_data['fecha_recoleccion'],
    #          hora_recoleccion = validated_data['hora_recoleccion'],
    #          estado_recoleccion = 1,
    #          donacion = self.validated_data.get('donacion',self.donacion)
    #     )
    #     for donacion_data in donaciones_data:
    #         DonacionBienes.objects.get(recoleccion=recoleccion, **donacion_data)
    #     recoleccion.save()          
    #     return recoleccion