from rest_framework import serializers
from DonacionesApp.models import DonacionBienes, Bien
from baseApp.serializers import DonanteSerializer, InstitucionSerializer
from baseApp.models import Institucion
import datetime

class BienesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bien
        exclude = ['donacion']


class DonacionBienesSerializer(serializers.ModelSerializer):
    # donante = DonanteSerializer(many = True),
    # institucion = InstitucionSerializer()  
    bienes = BienesSerializer(many=True)
    class Meta:
        model = DonacionBienes
        fields = ['donante','institucion','bienes']
        read_only_fields = ['cod_estado','fecha_creacion']

    def create(self,validated_data):
         bienes_data = validated_data.pop('bienes')
         donacion = DonacionBienes.objects.create(
             donante = validated_data['donante'],
             institucion = validated_data['institucion'],
             cod_estado = 1,
             fecha_creacion = datetime.datetime.now()
         )
         for bien_data in bienes_data:
            Bien.objects.create(donacion=donacion, **bien_data)
        #  donacion.save()          
         return donacion

class AceptarDonacionSerializer(serializers.ModelSerializer):
    #bienes = BienesSerializer(many=True)
    class Meta:
        model = DonacionBienes
        fields = ['fecha_retiro']
        #read_only_fields = ['fecha_aceptacion','cod_estado']
    # def update(self,validated_data):
    #     bienes_data = validated_data.pop('bienes')
    #      donacion = DonacionBienes.objects.update(
    #          donante = validated_data['donante'],
    #          institucion = validated_data['institucion'],
    #          cod_estado = 1,
    #          fecha_creacion = datetime.datetime.now()
    #      )
    #      for bien_data in bienes_data:
    #         Bien.objects.create(donacion=donacion, **bien_data)
    #     #  donacion.save()          
    #      return donacion

    