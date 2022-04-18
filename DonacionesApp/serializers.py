from rest_framework import serializers
from DonacionesApp.models import DonacionBienes, Bien
from baseApp.serializers import DonanteSerializer, InstitucionSerializer
from baseApp.models import Institucion
import datetime

class BienesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bien
        fields = '__all__'


class DonacionBienesSerializer(serializers.ModelSerializer):
    # donante = DonanteSerializer(many = True),
    # institucion = InstitucionSerializer()  
    #bienes = BienesSerializer(many=True)
    class Meta:
        model = DonacionBienes
        fields = ['donante','institucion']
        read_only_fields = ['cod_estado','fecha_creacion']

    def create(self,validated_data):
    #     donante_data = validated_data.pop('donante'),
    #     institucion_data = validated_data.pop('institucion'),
         donacion = DonacionBienes.objects.create(
             donante = validated_data['donante'],
             institucion = validated_data['institucion'],
             cod_estado = 1,
             fecha_creacion = datetime.datetime.now()
         )
        # bienes_data = validated_data.pop('donaciones')
        # bien = Bien.objects.create(**validated_data)
        # for donacion_data in donaciones_data:
        #     DonacionBienes.objects.create(bien=bien, **donacion_data)       
         donacion.save()
         return donacion

# class DonacionIdSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = DonacionBienes
#         fields = ['id']
        
# class BienesSerializer(serializers.ModelSerializer):
#     #donaciones = DonacionBienesSerializer(many=True)
#     class Meta:
#         model = Bien
#         fields = '__all__'

#     def create(self,validated_data):
#         donaciones_data = validated_data.pop('donaciones')
#         bien = Bien.objects.create(**validated_data)
#         for donacion_data in donaciones_data:
#             DonacionBienes.objects.create(bien=bien, **donacion_data)
#         return bien

class AceptarDonacionSerializer(serializers.ModelSerializer):
    class Meta:
        model = DonacionBienes
        fields = '__all__'


    