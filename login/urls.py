from django.urls import path, include
from rest_framework import urlpatterns
from login import views
from rest_framework.urlpatterns import format_suffix_patterns
from login.views import DonanteList
from rest_framework import renderers
from rest_framework.routers import DefaultRouter

urlpatterns = [
    path('donantes/', views.DonanteList.as_view(), name='donante-list'),
]

urlpatterns = format_suffix_patterns(urlpatterns)