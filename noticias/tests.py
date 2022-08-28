"""Pruebas de integración"""
from datetime import date, datetime

from django.urls import reverse
from django.contrib.auth.models import User, Group

from rest_framework.test import APITestCase, APIClient
from rest_framework import status

from baseApp.models import Cadete, Donante, Institucion
from login.serializers import CadeteUserSerializer

from noticias.models import Noticia, Etiqueta, ComentarioPublicacion

# pylint: disable=no-member

class NoticiaGeneralListTestCase(APITestCase):
    """
    Pruebas realizadas sobre el listado de la clase Noticia.
    """
    fixtures = ['group.json']

    def setUp(self):
        """
        Preparo algunas variables utilizadas en las pruebas de la clase.
        Inicio el cliente, creo el usuario john (que será el que tenga el rol
        de Donante) y genero la url.
        """
        self.client = APIClient()
        # self.user = User.objects.create_user('john',
        #                                      'lennon@thebeatles.com',
        #                                      'johnpassword',
        #                                      first_name='john',
        #                                      last_name='lennon')
        self.user_institucion = User.objects.create_user(
            'unainstitucion',
            'institucion@gmail.com',
            'password',
            first_name='Steve',
            last_name='Caprinne'
        )
        self.user_institucion.groups.set(Group.objects.filter(id=2))
        self.institucion = Institucion.objects.create(
            nombre='UnaInstitucion',
            director='Steve Caprinne',
            usuario=self.user_institucion
        )
        self.etiqueta1 = Etiqueta.objects.create(nombre='etiqueta1')
        self.etiqueta2 = Etiqueta.objects.create(nombre='etiqueta2')
        self.url = reverse('lista-noticias-generales')

    def test_no_listar_noticias_generales_vacias(self):
        """
        Valido que, cuando no existen noticias creadas, al realizar un GET me
        devuelva una lista vacía.
        """
        response = self.client.get(self.url)
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
        noticia = Noticia.objects.create(
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
        self.assertEqual(noticia_response['titulo'], noticia.titulo)
        self.assertEqual(noticia_response['descripcion'], noticia.descripcion)
        self.assertEqual(datetime.strptime(noticia_response['fecha_publicacion'],'%Y-%m-%dT%H:%M:%S.%f'), noticia.fecha_publicacion)
        self.assertEqual(noticia_response['autores'], noticia.autores)
        self.assertEqual(noticia_response['institucion'], noticia.institucion.id)
        self.assertEqual(noticia_response['usuario'], noticia.usuario.id)
        # self.assertEqual(noticia_response['etiquetas'], noticia.etiquetas)


    def test_listar_noticias_generales(self):
        """
        Valido que, cuando existan varias noticia creada, al realizar un GET se
        muestre esas noticias
        """
        noticia1 = Noticia.objects.create(
            titulo='Titulo',
            descripcion='Descripcion',
            fecha_publicacion=datetime.now(),
            autores='Autores',
            institucion=self.institucion,
            usuario=self.user_institucion
        )
        noticia1.etiquetas.set([Etiqueta.objects.first()])
        noticia1.save()
        noticia2 = Noticia.objects.create(
            titulo='Titulo',
            descripcion='Descripcion',
            fecha_publicacion=datetime.now(),
            autores='Autores',
            institucion=self.institucion,
            usuario=self.user_institucion
        )
        noticia2.etiquetas.set([Etiqueta.objects.first()])
        noticia2.save()
        noticia3 = Noticia.objects.create(
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
        self.user_institucion.groups.set(Group.objects.filter(id=2))
        self.institucion = Institucion.objects.create(
            nombre='UnaInstitucion',
            director='Steve Caprinne',
            usuario=self.user_institucion
        )
        self.noticia = Noticia.objects.create(
            titulo='Titulo',
            descripcion='Descripcion',
            fecha_publicacion=datetime.now(),
            autores='Autores',
            institucion=self.institucion,
            usuario=self.user_institucion
        )
        self.etiqueta1 = Etiqueta.objects.create(nombre='etiqueta1')
        self.etiqueta2 = Etiqueta.objects.create(nombre='etiqueta2')
        self.noticia.etiquetas.set([self.etiqueta1,self.etiqueta2])
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
        url_erroneo = reverse('detalle-noticia', args=[99])
        response = self.client.get(url_erroneo)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)        


class CreateComentarioPublicacionTestCase(APITestCase):
    """
    Pruebas realizadas sobre la creaciónde un comentario realizado sobre una
    noticia o un comentario de un noticia 
    """
    def setUp(self):
        """
        docstring
        """
        self.client = APIClient()
        self.user = User.objects.create_user('john',
                                             'lennon@thebeatles.com',
                                             'johnpassword',
                                             first_name='john',
                                             last_name='lennon')
        self.user.groups.set(Group.objects.filter(name='donante'))
        self.user_institucion = User.objects.create_user(
            'unainstitucion',
            'institucion@gmail.com',
            'password',
            first_name='Steve',
            last_name='Caprinne'
        )
        self.user_institucion.groups.set(Group.objects.filter(id=2))
        self.institucion = Institucion.objects.create(
            nombre='UnaInstitucion',
            director='Steve Caprinne',
            usuario=self.user_institucion
        )
        self.noticia = Noticia.objects.create(
            titulo='Titulo',
            descripcion='Descripcion',
            fecha_publicacion=datetime.now(),
            autores='Autores',
            institucion=self.institucion,
            usuario=self.user_institucion
        )
        self.etiqueta1 = Etiqueta.objects.create(nombre='etiqueta1')
        self.etiqueta2 = Etiqueta.objects.create(nombre='etiqueta2')
        self.noticia.etiquetas.set([self.etiqueta1,self.etiqueta2])
        self.noticia.save()
        self.url = reverse('crear-comentario')

    def test_no_crear_comentario_sin_autenticacion(self):
        """
        Valido que al realizar un POST cuando el usuario no se autentico,
        me devuelva un error de usuario no autenticado
        """
        data = {
            'texto_comentario':'Esto es un texto',
            'noticia':self.noticia.id
        }
        response = self.client.post(self.url,data)
        cantidad = ComentarioPublicacion.objects.count()
        self.assertEqual(cantidad,0)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_crear_comentario_noticia(self):
        """
        Valido que al realizar un POST con todos los datos se genere una
        instancia de la clase ComentarioPublicacion
        """
        self.client.force_login(self.user)
        data = {
            'texto_comentario':'Esto es un texto',
            'noticia':self.noticia.id
        }
        response = self.client.post(self.url,data)
        cantidad = ComentarioPublicacion.objects.count()
        if cantidad > 0:
            comentario = ComentarioPublicacion.objects.get(id=response.data['id'])
        self.assertEqual(cantidad,1)
        self.assertEqual(comentario.texto_comentario, data['texto_comentario'])
        self.assertEqual(comentario.fecha_publicacion.date(), datetime.now().date())
        self.assertEqual(comentario.usuario.id, self.user.id)
        self.assertEqual(comentario.noticia.id, data['noticia'])
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


# class NoticiaInstitucionListTestCase(APITestCase):
#     """
#     Pruebas realizadas sobre el listado de las noticias publicadas por la
#     institución que se encuentra logueada.
#     """
#     def setUp(self):
#         """
#         docstring
#         """
#         self.client = APIClient()
#         self.user_donante = User.objects.create_user('john',
#                                              'lennon@thebeatles.com',
#                                              'johnpassword',
#                                              first_name='john',
#                                              last_name='lennon')
#         self.user_donante.groups.set(Group.objects.filter(name='donante'))
#         self.donante = Donante.objects.create(

#         )
#         self.user_institucion = User.objects.create_user(
#             'unainstitucion',
#             'institucion@gmail.com',
#             'password',
#             first_name='Steve',
#             last_name='Caprinne'
#         )
#         self.user_institucion.groups.set(Group.objects.filter(id=2))
#         self.institucion = Institucion.objects.create(
#             nombre='UnaInstitucion',
#             director='Steve Caprinne',
#             usuario=self.user_institucion
#         )
#         self.noticia = Noticia.objects.create(
#             titulo='Titulo',
#             descripcion='Descripcion',
#             fecha_publicacion=datetime.now(),
#             autores='Autores',
#             institucion=self.institucion,
#             usuario=self.user_institucion
#         )
#         self.etiqueta1 = Etiqueta.objects.create(nombre='etiqueta1')
#         self.etiqueta2 = Etiqueta.objects.create(nombre='etiqueta2')
#         self.noticia.etiquetas.set([self.etiqueta1,self.etiqueta2])
#         self.noticia.save()
#         self.url = reverse('crear-comentario')

#     def test_no_crear_comentario_sin_autenticacion(self):
#         """
#         Valido que al realizar un POST cuando el usuario no se autentico,
#         me devuelva un error de usuario no autenticado
#         """
#         data = {
#             'texto_comentario':'Esto es un texto',
#             'noticia':self.noticia.id
#         }
#         response = self.client.post(self.url,data)
#         cantidad = ComentarioPublicacion.objects.count()
#         self.assertEqual(cantidad,0)
#         self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)