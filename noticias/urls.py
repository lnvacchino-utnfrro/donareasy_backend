"""Lista de rutas (path) del módulo Noticias"""
from django.urls import path

from noticias import views

urlpatterns = [
     path('',
          views.NoticiaGeneralList.as_view(),
          name='lista-noticias-generales'),
     path('<int:pk>/',
          views.NoticiaGeneralDetail.as_view(),
          name='detalle-noticia'),
     path('institucion/',
          views.NoticiaInstitucionList.as_view(),
          name='lista-noticia-institucion'),
     path('institucion/<int:pk>/',
          views.NoticiaInstitucionDetail.as_view(),
          name='detalle-noticia-institucion'),
     path('comentario/',
          views.ComentarioPublicacionCreate.as_view(),
          name='crear-comentario'),
]
