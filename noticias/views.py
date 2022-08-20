"""Vistas para módulo Noticias"""

from requests import Response

from rest_framework import generics
from rest_framework import status

from baseApp.models import Institucion

from noticias.models import ComentarioPublicacion, Noticia
from noticias.serializers import NoticiaSerializer, NoticiaConComentariosSerializer, ComentarioPublicacionSerializer, \
                                 CreateNoticiaInstitucionSerializer

# pylint: disable=no-member

class NoticiaGeneralList(generics.ListAPIView):
    """APIView para listar y crear instancias de la clase Noticia"""
    queryset = Noticia.objects.all()
    serializer_class = NoticiaSerializer


class NoticiaGeneralDetail(generics.RetrieveAPIView):
    """APIView para recuperar, actualizar y destruir una instancia de la clase Noticia"""
    queryset = Noticia.objects.all()
    serializer_class = NoticiaConComentariosSerializer


class NoticiaInstitucionList(generics.ListCreateAPIView):
    """docstring"""
    serializer_class = CreateNoticiaInstitucionSerializer

    def get_queryset(self):
        user = self.request.user
        print(user)
        if user.groups.filter(name='instituciones').exists():
            print('camino 1')
            institucion = Institucion.objects.get(usuario=user)
            queryset = Noticia.objects.filter(institucion=institucion)
        else:
            print('camino 2')
            # queryset = []
            queryset = Noticia.objects.none()
        # return Noticia.objects.all()
        return queryset


class NoticiaInstitucionDetail(generics.RetrieveUpdateDestroyAPIView):
    """APIView para recuperar, actualizar y destruir una instancia de la clase Noticia"""
    queryset = Noticia.objects.all()
    serializer_class = NoticiaConComentariosSerializer


class ComentarioPublicacionCreate(generics.CreateAPIView):
    """APIView para crear una instancia de comentario"""
    queryset = ComentarioPublicacion.objects.all()
    serializer_class = ComentarioPublicacionSerializer