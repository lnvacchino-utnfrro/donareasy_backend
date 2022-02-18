from django.urls import path, include
from rest_framework import urlpatterns
from login import auth, views
from rest_framework.urlpatterns import format_suffix_patterns
from login.views import DonanteList, DonanteDetail, UserCreate, UserDetail, InstitucionList, InstitucionDetail
from login.views import DonanteCreate, InstitucionCreate
from rest_framework import renderers
from rest_framework.routers import DefaultRouter

urlpatterns = [
    #path('donantes/', views.DonanteList.as_view(), name='donantes-list'),
    #path('donantes/<int:pk>/', views.DonanteDetail.as_view(), name='donantes-detail'),
    #path('usuarios/', views.UserList.as_view(), name='usuarios-list'),
    path('usuarios/<int:pk>/', views.UserDetail.as_view(), name='user-detail'),
    path('',auth.Login.as_view(),name='login'),
    path('logout/',auth.Logout.as_view(),name='logout'),
    #path('instituciones/', views.InstitucionList.as_view(), name='instituciones-list'),
    #path('instituciones/<int:pk>/', views.InstitucionDetail.as_view(), name='instituciones-detail'),
    path('logup/', views.UserCreate.as_view(), name='logup'),
    path('logup/donante/', views.DonanteCreate.as_view(), name='donante-create'),
    path('logup/institucion/', views.InstitucionCreate.as_view(), name='institucion-create'),
    path('recuperacion/',auth.RecuperacionContraseña.as_view(), name='recuperacion_contraseña'),
]

urlpatterns = format_suffix_patterns(urlpatterns)