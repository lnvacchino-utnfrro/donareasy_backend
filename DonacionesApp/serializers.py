from rest_framework import serializers
from DonacionesApp.models import DonacionBienes, Bien, DonacionMonetaria
from baseApp.serializers import DonanteSerializer, InstitucionSerializer
from baseApp.models import Institucion
from datetime import datetime,date

class BienesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bien
        exclude = ['donacion']


class DonacionBienesSerializer(serializers.ModelSerializer):
    donante = DonanteSerializer()
    institucion = InstitucionSerializer()  
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
             fecha_creacion = datetime.now()
         )
         for bien_data in bienes_data:
            Bien.objects.create(donacion=donacion, **bien_data)
        #  donacion.save()          
         return donacion


class ActualizarEstadoDonacionSerializer(serializers.ModelSerializer):
    #bienes = BienesSerializer(many=True)
    class Meta:
        model = DonacionBienes
        fields = ['cod_estado','motivo_cancelacion']
        read_only_fields = ['fecha_aceptacion','fecha_cancelacion']
    def update(self,donacion,validated_data):
        if validated_data['cod_estado'] == 2:
            donacion.cod_estado = validated_data.get('cod_estado',donacion.cod_estado)
            donacion.fecha_aceptacion = datetime.now()
            donacion.fecha_cancelacion = None
            donacion.motivo_cancelacion = None          
            donacion.save()           
        else:
            donacion.cod_estado = validated_data.get('cod_estado',donacion.cod_estado)
            donacion.fecha_aceptacion = None 
            donacion.fecha_cancelacion = datetime.now()
            donacion.motivo_cancelacion = validated_data.get('motivo_cancelacion',donacion.motivo_cancelacion)
            donacion.save()         
        return donacion

class DonacionesSerializer(serializers.ModelSerializer):
    bienes = BienesSerializer(many=True)
    donante = DonanteSerializer()
    class Meta:
        model = DonacionBienes
        fields = ['id','donante','cod_estado','bienes']
    
class DonacionMonetariaSerializer(serializers.ModelSerializer):
    class Meta:
        model = DonacionMonetaria
        fields = ['donante','institucion','monto']
        read_only_fields = ['cod_estado','fecha_transferencia','fecha_creacion']
    def create(self,validated_data):
        #if validated_data['institucion']['cbu'] is not None: 
        #! Ver como hacer para no permitir que elija instituciones no bancarizadas, #Lo hace frontend?
        if (validated_data['monto'] > 0):
            donacion = DonacionMonetaria.objects.create(
             donante = validated_data['donante'],
             institucion = validated_data['institucion'],
             monto = validated_data['monto'],
             cod_estado = 3,
             fecha_transferencia = date.today(),
             fecha_creacion = datetime.now()
            )
        #else:
        #    print("La institución no posee CBU")
        return donacion

class DatosBancariosInstitucion(serializers.ModelSerializer):
    #mensaje = serializers.CharField(max_length=100)
    class Meta:
        model = Institucion
        fields = ['id','nombre','cbu','cuenta_bancaria']

class VerTransferenciaSerializer(serializers.ModelSerializer):
    donante = DonanteSerializer()
    class Meta:
        model = DonacionMonetaria
        fields = ['id','donante','cod_estado','monto','fecha_transferencia']

class AceptarTransferenciaSerializer(serializers.ModelSerializer):
    #bienes = BienesSerializer(many=True)
    class Meta:
        model = DonacionMonetaria
        fields = ['cod_estado','motivo_cancelacion']
        read_only_fields = ['fecha_aceptacion','fecha_cancelacion']
    def update(self,donacion,validated_data):
        if validated_data['cod_estado'] == 4:
            donacion.cod_estado = validated_data.get('cod_estado',donacion.cod_estado)
            donacion.fecha_aceptacion = datetime.now()
            donacion.fecha_cancelacion = None
            donacion.motivo_cancelacion = None          
            donacion.save()           
        else:
            donacion.cod_estado = validated_data.get('cod_estado',donacion.cod_estado)
            donacion.fecha_aceptacion = None 
            donacion.fecha_cancelacion = datetime.now()
            donacion.motivo_cancelacion = validated_data.get('motivo_cancelacion',donacion.motivo_cancelacion)
            donacion.save()         
        return donacion