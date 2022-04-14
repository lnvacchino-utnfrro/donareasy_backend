from rest_framework import serializers
from DonacionesApp.models import DonacionBienes, Bien
from baseApp.serializers import DonanteSerializer, InstitucionSerializer

class DonacionBienesSerializer(serializers.ModelSerializer):
    donante = DonanteSerializer(many=True),
    institucion = InstitucionSerializer(many=True)
    class Meta:
        model = DonacionBienes
        fields = ['donante','institucion']

class DonacionIdSerializer(serializers.ModelSerializer):
    class Meta:
        model = DonacionBienes
        fields = ['id']
        
class BienesSerializer(serializers.ModelSerializer):
    donaciones = DonacionBienesSerializer(many=True)
    class Meta:
        model = Bien
        fields = '__all__'

    def create(self,validated_data):
        donaciones_data = validated_data.pop('donaciones')
        bien = Bien.objects.create(**validated_data)
        for donacion_data in donaciones_data:
            DonacionBienes.objects.create(bien=bien, **donacion_data)
        return bien



    