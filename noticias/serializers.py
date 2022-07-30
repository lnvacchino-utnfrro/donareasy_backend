"""Archivo para generar Serializadores para el módulo Noticias"""
from rest_framework import serializers
from rest_framework_recursive.fields import RecursiveField

from baseApp.serializers import InstitucionSerializer
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
        fields = ['texto_comentario','fecha_publicacion','usuario','noticia','comentario_comentario','reacciones']
