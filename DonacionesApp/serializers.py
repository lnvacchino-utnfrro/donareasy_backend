from rest_framework import serializers
from DonacionesApp.models import DonacionBienes, Bien, DonacionMonetaria, Donacion, Necesidad
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
    institucion = serializers.PrimaryKeyRelatedField(queryset=Institucion.instituciones_habilitadas(),read_only=False)
    bienes = BienesSerializer(many=True)

    class Meta:
        model = DonacionBienes
        fields = ['institucion','bienes','observacion','tipo']
        read_only_fields = ['cod_estado','fecha_creacion']

    def create(self,validated_data):
        user = self.context['request'].user
        donante = Donante.objects.get(usuario=user)
        bienes_data = validated_data.pop('bienes')
        donacion = DonacionBienes.objects.create(
            donante = donante,
            institucion = validated_data['institucion'],
            cod_estado = 1,
            fecha_creacion = datetime.now(),
            observacion = validated_data['observacion'],
            tipo = validated_data['tipo']
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

class RecogerDonacionSerializer(serializers.ModelSerializer):
    class Meta:
        model = DonacionBienes
        fields = []

    def update(self,donacion,validated_data):
        donacion.cod_estado = 6
        donacion.fecha_retiro = datetime.now()         
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
        fields = ['id','donante','cod_estado','bienes','observacion','tipo']
    
class DonacionMonetariaSerializer(serializers.ModelSerializer):
    class Meta:
        model = DonacionMonetaria
        fields = ['institucion','monto','observacion','comprobante_transaccion']
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
        if value.cbu is None or value.cbu == '':
            raise serializers.ValidationError("La institución ingresada no posee CBU")
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
             fecha_creacion = datetime.now(),
             observacion = validated_data['observacion'],
             comprobante_transaccion = validated_data['comprobante_transaccion'],
            )
        return donacion

class DatosBancariosInstitucion(serializers.ModelSerializer):
    #mensaje = serializers.CharField(max_length=100)
    
    class Meta:
        model = Institucion
        fields = ['id','nombre','cbu']

class VerTransferenciaSerializer(serializers.ModelSerializer):
    donante = DonanteSerializer()
    institucion = InstitucionSerializer()
    
    class Meta:
        model = DonacionMonetaria
        fields = ['id','donante','institucion','cod_estado','monto','fecha_transferencia','observacion','comprobante_transaccion']


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


class DonacionesGeneralesDonanteSeralizer(serializers.ModelSerializer):
    institucion = InstitucionSerializer()
    bienes = BienesSerializer(many=True)
    donante = DonanteSerializer()

    class Meta:
        model = DonacionBienes #Donacion
        #exclude = ['donante']
        fields = '__all__'


class CancelarDonacionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Donacion
        fields = []

    def update(self,donacion,validated_data):
        donacion.cod_estado = 0
        donacion.fecha_cancelacion = datetime.now()
        donacion.fecha_aceptacion = None
        donacion.motivo_cancelacion = 'Cancelación por parte del usuario'          
        donacion.save()
        return donacion


class NecesidadSerializer(serializers.ModelSerializer):

    #institucion = InstitucionSerializer()
    #institucion = serializers.PrimaryKeyRelatedField(queryset=Institucion.objects.all(),read_only=False)

    class Meta:
        model = Necesidad
        exclude = ['institucion','fecha_baja','fecha_alta','isDelete','cantidad']

    def create(self,validated_data):
        usuario = self.context['request'].user
        necesidad = Necesidad.objects.create(
            tipo = validated_data['tipo'],
            titulo = validated_data['titulo'],
            descripcion = validated_data['descripcion'],
            fecha_baja = None,
            fecha_vigencia = validated_data['fecha_vigencia'],
            institucion = Institucion.objects.get(usuario = usuario),
            fecha_alta = datetime.now()
        )
        return necesidad

class ModificarNecesidadSerializer(serializers.ModelSerializer):

    class Meta:
        model = Necesidad
        fields = ['descripcion','fecha_vigencia']

class ListaNecesidadSerializer(serializers.ModelSerializer):

    #institucion = InstitucionSerializer()
    #institucion = serializers.PrimaryKeyRelatedField(queryset=Institucion.objects.all(),read_only=False)

    class Meta:
        model = Necesidad
        exclude = ['cantidad']

    # def validate_fecha_vigencia(self,value):
    #     if value >= datetime.now():
    #         raise serializers.ValidationError("El monto debe ser un valor mayor a 0")
    #     return value
    

class EntregarDonacionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Donacion
        fields = []

    def update(self,donacion,validated_data):
        donacion.cod_estado = 4
        donacion.fecha_entrega_real = datetime.now()    
        donacion.save()
        return donacion
