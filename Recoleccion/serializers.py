from rest_framework import serializers
from DonacionesApp.models import DonacionBienes, Bien, DonacionMonetaria
from Recoleccion.models import *
from baseApp.serializers import DonanteSerializer,CadeteSerializer
from baseApp.models import Institucion, Cadete
from datetime import datetime,date
from DonacionesApp.serializers import DonacionBienesSerializer, IdDonacionSerializer

class RecoleccionesCreateSerializer(serializers.ModelSerializer):
     #donacion = DonacionBienesSerializer(many=True)
     donaciones = serializers.ListField( #IdDonacionSerializer(many=True)
            child= IdDonacionSerializer(many=True))
     #cadete = CadeteSerializer
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
        for donacion_data in donaciones_data:
            #donacion = DonacionBienes.objects.get(pk=donacion_data, **donacion_data)
            print(donacion_data)
            donacion = DonacionBienes.objects.get(id=donacion_data, **donacion_data) #si donacion_data es un numero
                                                                   #sino, ver como conseguir el número ingresado en la lista
            # https://docs.djangoproject.com/en/4.0/topics/db/queries/
            donacion.recoleccion = recoleccion
            donacion.save()

        return recoleccion
