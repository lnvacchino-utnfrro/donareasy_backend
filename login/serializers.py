from django.contrib.auth.models import User
from typing_extensions import Required
from rest_framework import serializers
from rest_framework.utils.field_mapping import needs_label
from login.models import Donante

class DonanteSerializer(serializers.Serializer):
    class Meta:
        model = Donante
        fields = [] #campos

    