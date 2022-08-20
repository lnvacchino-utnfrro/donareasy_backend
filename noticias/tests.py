"""Pruebas de integración"""
from datetime import date, datetime

from django.urls import reverse
from django.contrib.auth.models import User

from rest_framework.test import APITestCase, APIClient
from rest_framework import status

from baseApp.models import Cadete, Donante, Institucion
from login.serializers import CadeteUserSerializer

from noticias.models import Noticia, Etiqueta

# pylint: disable=no-member

class NoticiaGeneralListTestCase(APITestCase):
    """
    Pruebas realizadas sobre el listado de la clase Noticia.
    """
    def setUp(self):
        """
        Preparo algunas variables utilizadas en las pruebas de la clase.
        Inicio el cliente, creo el usuario john (que será el que tenga el rol
        de Donante) y genero la url.
        """
        self.client = APIClient()
        self.user = User.objects.create_user('john',
                                             'lennon@thebeatles.com',
                                             'johnpassword',
                                             first_name='john',
                                             last_name='lennon')
        self.user_institucion = User.objects.create_user(
            'unainstitucion',
            'institucion@gmail.com',
            'password',
            first_name='Steve',
            last_name='Caprinne'
        )
        self.institucion = Institucion.objects.create(
            nombre='UnaInstitucion',
            director='Steve Caprinne',
            usuario=self.user_institucion
        )
        self.url = reverse('lista-noticias-generales')

    def test_no_listar_noticias_generales(self):
        """
        Valido que, cuando no existen noticias creadas, al realizar un GET me
        devuelva una lista vacía.
        """
        response = self.client.get(self.ur)
        cantidad = Noticia.objects.count()
        self.assertEqual(cantidad, 0)
        self.assertEqual(response.data['count'], 0)
        self.assertEqual(len(response.data['results']), 0)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_listar_una_noticia_general(self):
        """
        Valido que, cuando exista una noticia creada, al realizar un GET se 
        muestre esa noticia
        """
        noticia = Noticia(
            titulo='Titulo',
            descripcion='Descripcion',
            fecha_publicacion=datetime.now(),
            autores='Autores',
            institucion=self.institucion,
            usuario=self.user_institucion
        )
        noticia.etiquetas.set([Etiqueta.objects.first()])
        noticia.save()
        response = self.client.get(self.url)
        cantidad = Noticia.objects.count()
        self.assertEqual(cantidad,1)
        self.assertEqual(response.data['count'],1)
        self.assertEqual(len(response.data['results']),1)
        noticia_response = response.data['results'][0]
        self.assertEqual(noticia_response.titulo, noticia.titulo)
        self.assertEqual(noticia_response.descripcion, noticia.descripcion)
        self.assertEqual(noticia_response.fecha_publicacion, noticia.fecha_publicacion)
        self.assertEqual(noticia_response.autores, noticia.autores)
        self.assertEqual(noticia_response.institucion, noticia.institucion)
        self.assertEqual(noticia_response.usuario, noticia.usuario)
        self.assertEqual(noticia_response.etiquetas, noticia.etiquetas)

    def test_listar_noticias_generales(self):
        """
        Valido que, cuando existan varias noticia creada, al realizar un GET se
        muestre esas noticias
        """
        noticia1 = Noticia(
            titulo='Titulo',
            descripcion='Descripcion',
            fecha_publicacion=datetime.now(),
            autores='Autores',
            institucion=self.institucion,
            usuario=self.user_institucion
        )
        noticia1.etiquetas.set([Etiqueta.objects.first()])
        noticia1.save()
        noticia2 = Noticia(
            titulo='Titulo',
            descripcion='Descripcion',
            fecha_publicacion=datetime.now(),
            autores='Autores',
            institucion=self.institucion,
            usuario=self.user_institucion
        )
        noticia2.etiquetas.set([Etiqueta.objects.all()])
        noticia2.save()
        noticia3 = Noticia(
            titulo='Titulo',
            descripcion='Descripcion',
            fecha_publicacion=datetime.now(),
            autores='Autores',
            institucion=self.institucion,
            usuario=self.user_institucion
        )
        noticia3.etiquetas.set([Etiqueta.objects.first()])
        noticia3.save()
        response = self.client.get(self.url)
        cantidad = Noticia.objects.count()
        self.assertEqual(cantidad,3)
        self.assertEqual(response.data['count'],3)
        self.assertEqual(len(response.data['results']),3)
   

class NoticiaDetailTestCase(APITestCase):
    """
    Pruebas realizadas sobre la visualización de los detalles de una noticia
    """
    def setUp(self):
        """
        Preparo algunas variables utilizadas en las pruebas de la clase.
        Inicio el cliente, creo el usuario john (que será el que tenga el rol
        de Donante) y genero la url.
        """
        self.client = APIClient()
        self.user = User.objects.create_user('john',
                                             'lennon@thebeatles.com',
                                             'johnpassword',
                                             first_name='john',
                                             last_name='lennon')
        self.user_institucion = User.objects.create_user(
            'unainstitucion',
            'institucion@gmail.com',
            'password',
            first_name='Steve',
            last_name='Caprinne'
        )
        self.institucion = Institucion.objects.create(
            nombre='UnaInstitucion',
            director='Steve Caprinne',
            usuario=self.user_institucion
        )
        self.noticia = Noticia(
            titulo='Titulo',
            descripcion='Descripcion',
            fecha_publicacion=datetime.now(),
            autores='Autores',
            institucion=self.institucion,
            usuario=self.user_institucion
        )
        self.noticia.etiquetas.set([Etiqueta.objects.first()])
        self.noticia.save()
        self.url = reverse('detalle-noticia', args=[self.noticia.id])

    def test_mostrar_detalle_noticia(self):
        """
        Valido que, al realizar un GET me devuelva el detalle de la noticia
        """
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_error_noticia_no_existente(self):
        """
        Valido que el GET me devuelva un error si la noticia no existe
        """
        self.url = reverse('detalle-noticia', args=[99])
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)        
