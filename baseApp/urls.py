"""Lista de rutas (path) del módulo baseApp"""
from django.urls import path

from rest_framework import urlpatterns
from rest_framework.urlpatterns import format_suffix_patterns

from baseApp import views

urlpatterns = [
    path('donantes/',
         views.DonanteList.as_view(),
         name='donantes-list'),
    path('donantes/<int:pk>/',
         views.DonanteDetail.as_view(),
         name='donantes-detail'),
    # path('usuarios/',
    #      views.UserList.as_view(),
    #      name='usuarios-list'),
    # path('usuarios/<int:pk>/',
    #      views.UserDetail.as_view(),
    #      name='user-detail'),
    path('instituciones/',
         views.InstitucionList.as_view(),
         name='instituciones-list'),
    path('instituciones/<int:pk>/',
         views.InstitucionDetail.as_view(),
         name='instituciones-detail'),
]

# urlpatterns = format_suffix_patterns(urlpatterns)
