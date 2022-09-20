from rest_framework import serializers
from DonacionesApp.models import DonacionBienes, Bien, DonacionMonetaria
from baseApp.serializers import DonanteSerializer, InstitucionSerializer
from baseApp.models import Donante, Institucion
from datetime import datetime,date

class BienesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bien
        exclude = ['donacion']


class DonacionBienesSerializer(serializers.ModelSerializer):
    # donante = DonanteSerializer()
    # institucion = InstitucionSerializer(read_only=True)
    institucion = serializers.PrimaryKeyRelatedField(queryset=Institucion.objects.all(),read_only=False)
    bienes = BienesSerializer(many=True)

    class Meta:
        model = DonacionBienes
        fields = ['institucion','bienes']
        read_only_fields = ['cod_estado','fecha_creacion']

    def create(self,validated_data):
        user = self.context['request'].user
        donante = Donante.objects.get(usuario=user)
        bienes_data = validated_data.pop('bienes')
        donacion = DonacionBienes.objects.create(
            donante = donante,
            institucion = validated_data['institucion'],
            cod_estado = 1,
            fecha_creacion = datetime.now()
        )
        for bien_data in bienes_data:
            Bien.objects.create(donacion=donacion, **bien_data)

        return donacion


class AceptarDonacionSerializer(serializers.ModelSerializer):
    class Meta:
        model = DonacionBienes
        fields = []

    def update(self,donacion,validated_data):
        donacion.cod_estado = 2
        donacion.fecha_aceptacion = datetime.now()
        donacion.fecha_cancelacion = None
        donacion.motivo_cancelacion = None          
        donacion.save()
        return donacion           


class RechazarDonacionSerializer(serializers.ModelSerializer):
    class Meta:
        model = DonacionBienes
        fields = ['motivo_cancelacion']

    def update(self,donacion,validated_data):
        donacion.cod_estado = 0
        donacion.fecha_aceptacion = None 
        donacion.fecha_cancelacion = datetime.now()
        donacion.motivo_cancelacion = validated_data.get('motivo_cancelacion',donacion.motivo_cancelacion)
        donacion.save()
        return donacion           


class ActualizarEstadoDonacionSerializer(serializers.ModelSerializer):
    bienes = BienesSerializer(many=True,read_only=True)
    donante = DonanteSerializer(read_only=True)
    
    class Meta:
        model = DonacionBienes
        fields = ['donante','bienes','cod_estado','motivo_cancelacion']
        read_only_fields = ['id','fecha_aceptacion','fecha_cancelacion']
        
    def update(self,donacion,validated_data):
        if validated_data['cod_estado'] == 2:
            donacion.cod_estado = validated_data.get('cod_estado',donacion.cod_estado)
            donacion.fecha_aceptacion = datetime.now()
            donacion.fecha_cancelacion = None
            donacion.motivo_cancelacion = None          
            donacion.save()           
        elif validated_data['cod_estado'] == 0:
            donacion.cod_estado = validated_data.get('cod_estado',donacion.cod_estado)
            donacion.fecha_aceptacion = None 
            donacion.fecha_cancelacion = datetime.now()
            donacion.motivo_cancelacion = validated_data.get('motivo_cancelacion',donacion.motivo_cancelacion)
            donacion.save()
        elif validated_data['cod_estado'] == 5:
            donacion.cod_estado = validated_data.get('cod_estado',donacion.cod_estado)
            donacion.fecha_aceptacion = None 
            donacion.fecha_cancelacion = datetime.now()
            donacion.motivo_cancelacion = "La donación no fue entregada al cadete"
            donacion.save()
        else:
            donacion.cod_estado = 1
            donacion.fecha_aceptacion = None 
            donacion.fecha_cancelacion = None
            donacion.motivo_cancelacion = None
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
        fields = ['institucion','monto']
        read_only_fields = ['cod_estado','fecha_transferencia','fecha_creacion']
    
    def validate_monto(self,value):
        """
        Valida que el monto sea mayor a 0.
        """
        if value <= 0:
            raise serializers.ValidationError("El monto debe ser un valor mayor a 0")
        return value

    def validate_institucion(self,value):
        if value is None:
            raise serializers.ValidationError("El campo institución no puede ser nulo")
        if value.cbu is None or value.cbu <= 0:
            raise serializers.ValidationError("La institución ingresada no posee CBU")
        if value.cuenta_bancaria is None or value.cuenta_bancaria == '':
            raise serializers.ValidationError("La institución ingresada no posee cuenta bancaria")
        return value

    def create(self,validated_data):
        user = self.context['request'].user
        donante = Donante.objects.get(usuario=user)
        if (validated_data['monto'] > 0):
            donacion = DonacionMonetaria.objects.create(
             donante = donante,
             institucion = validated_data['institucion'],
             monto = validated_data['monto'],
             cod_estado = 3,
             fecha_transferencia = date.today(),
             fecha_creacion = datetime.now()
            )
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
    class Meta:
        model = DonacionMonetaria
        fields = []
    
    def update(self,donacion,validated_data):
        donacion.cod_estado = 4
        donacion.fecha_aceptacion = datetime.now()
        donacion.fecha_cancelacion = None
        donacion.motivo_cancelacion = None          
        donacion.save()                  
        return donacion
        

class RechazarTransferenciaSerializer(serializers.ModelSerializer):
    class Meta:
        model = DonacionMonetaria
        fields = ['motivo_cancelacion']

    def update(self,donacion,validated_data):
        donacion.cod_estado = 0
        donacion.fecha_aceptacion = None 
        donacion.fecha_cancelacion = datetime.now()
        donacion.motivo_cancelacion = validated_data.get('motivo_cancelacion',donacion.motivo_cancelacion)
        donacion.save()
        return donacion
