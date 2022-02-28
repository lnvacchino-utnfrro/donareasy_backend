from django.contrib.auth.models import User
from typing_extensions import Required
from rest_framework import serializers
from rest_framework.utils.field_mapping import needs_label
from baseApp.models import Donante, Institucion

class DonanteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Donante
        fields = '__all__'

class InstitucionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Institucion
        fields = '__all__'
