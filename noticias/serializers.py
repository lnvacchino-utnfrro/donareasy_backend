"""Archivo para generar Serializadores para el módulo Noticias"""
from datetime import datetime

from django.contrib.auth.models import User

from rest_framework import serializers
# from rest_framework_recursive.fields import RecursiveField

from baseApp.serializers import InstitucionSerializer
from baseApp.models import Institucion

from login.serializers import PublicUserSerializer

from noticias.models import ComentarioPublicacion, Etiqueta, Noticia, Reaccion

# pylint: disable=too-few-public-methods
    
class EtiquetaSerializer(serializers.ModelSerializer):
    """docstring"""
    class Meta:
        # pylint: disable=missing-class-docstring
        model = Etiqueta
        fields = '__all__'


class ReaccionSerializer(serializers.ModelSerializer):
    """docstring"""
    class Meta:
        # pylint: disable=missing-class-docstring
        model = Reaccion
        fields = '__all__'


class NoticiaSerializer(serializers.ModelSerializer):
    """Serializador para el modelo Noticia"""
    # institucion = InstitucionSerializer()
    # usuario = PublicUserSerializer()
    # etiquetas = EtiquetaSerializer(many=True)
    # reacciones = ReaccionSerializer(many=True)

    class Meta:
        # pylint: disable=missing-class-docstring
        model = Noticia
        fields = '__all__'


class CreateNoticiaInstitucionSerializer(serializers.ModelSerializer):
    """Serializador para el modelo Noticia"""
    # institucion = InstitucionSerializer()
    # usuario = PublicUserSerializer()
    # etiquetas = EtiquetaSerializer(many=True)
    # reacciones = ReaccionSerializer(many=True)

    class Meta:
        # pylint: disable=missing-class-docstring
        model = Noticia
        fields = ['id','etiquetas','titulo','descripcion','autores']

    def create(self,validated_data):
        institucion = Institucion.objects.get(pk=1)
        user = User.objects.get(pk=1)
        noticia = Noticia.objects.create(
            titulo = validated_data['titulo'],
            descripcion = validated_data['descripcion'],
            fecha_publicacion = datetime.now(),
            autores = validated_data['autores'],
            institucion = institucion,
            usuario = user
        )
        noticia.etiquetas.set(validated_data['etiquetas'])
        noticia.save()
            
        return noticia


class ComentarioSerializer(serializers.ModelSerializer):
    """docstring"""
    usuario = PublicUserSerializer()
    reacciones = ReaccionSerializer(many=True)

    class Meta:
        # pylint: disable=missing-class-docstring
        model = ComentarioPublicacion
        fields = ['texto_comentario','fecha_publicacion','usuario','reacciones']


class NoticiaConComentariosSerializer(serializers.ModelSerializer):
    """
    Serializador para mostrar una instancia del modelo Noticia y el detalle 
    de todos los comentarios asociados a esta noticia
    """
    noticia_comentario = ComentarioSerializer(many=True)
    institucion = InstitucionSerializer()
    usuario = PublicUserSerializer()
    etiquetas = EtiquetaSerializer(many=True)
    reacciones = ReaccionSerializer(many=True)

    class Meta:
        # pylint: disable=missing-class-docstring
        model = Noticia
        fields = ['id','institucion','usuario','etiquetas','reacciones','titulo',
                  'descripcion','fecha_publicacion','autores','noticia_comentario']


class ComentarioPublicacionSerializer(serializers.ModelSerializer):
    """
    Serializador para crear una instancia de la clase ComentarioPublicacion
    """    
    class Meta:
        # pylint: disable=missing-class-docstring
        model = ComentarioPublicacion
        fields = ['texto_comentario','noticia','comentario_comentario']

    def create(self,validated_data):
        user = User.objects.get(pk=1)
        comentario = ComentarioPublicacion.objects.create(
            texto_comentario = validated_data['texto_comentario'],
            noticia = validated_data['noticia'],
            fecha_publicacion = datetime.now(),
            usuario = user
        )
        comentario.comentario_comentario.set(validated_data['comentario_comentario'])
        comentario.save()
            
        return comentario