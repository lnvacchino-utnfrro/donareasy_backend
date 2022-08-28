"""Vistas para módulo Noticias"""
from requests import Response

from rest_framework import generics
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, SAFE_METHODS, \
                                        AllowAny, IsAdminUser

from baseApp.models import Institucion
from baseApp.permissions import IsInstitucionPermission

from noticias.models import ComentarioPublicacion, Noticia
from noticias.serializers import NoticiaSerializer, NoticiaConComentariosSerializer, ComentarioPublicacionSerializer, \
                                 CreateNoticiaInstitucionSerializer

# pylint: disable=no-member

class NoticiaGeneralList(generics.ListAPIView):
    """APIView para listar y crear instancias de la clase Noticia"""
    queryset = Noticia.objects.all()
    serializer_class = NoticiaSerializer
    permission_classes = [AllowAny]


class NoticiaGeneralDetail(generics.RetrieveAPIView):
    """APIView para recuperar, actualizar y destruir una instancia de la clase Noticia"""
    queryset = Noticia.objects.all()
    serializer_class = NoticiaConComentariosSerializer
    permission_classes = [AllowAny]


class NoticiaInstitucionList(generics.ListCreateAPIView):
    """docstring"""
    serializer_class = CreateNoticiaInstitucionSerializer
    permission_classes = [IsInstitucionPermission|IsAdminUser]

    def get_queryset(self):
        user = self.request.user
        if user.groups.filter(name='instituciones').exists():
            institucion = Institucion.objects.get(usuario=user)
            queryset = Noticia.objects.filter(institucion=institucion)
        else:
            queryset = Noticia.objects.none()
        return queryset


class NoticiaInstitucionDetail(generics.RetrieveUpdateDestroyAPIView):
    """APIView para recuperar, actualizar y destruir una instancia de la clase Noticia"""
    queryset = Noticia.objects.all()
    serializer_class = NoticiaConComentariosSerializer
    permission_classes = [IsInstitucionPermission]    


class ComentarioPublicacionCreate(generics.CreateAPIView):
    """APIView para crear una instancia de comentario"""
    queryset = ComentarioPublicacion.objects.all()
    serializer_class = ComentarioPublicacionSerializer
    permission_classes = [IsAuthenticated]
