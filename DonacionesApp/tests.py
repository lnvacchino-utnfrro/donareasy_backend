"""Pruebas de integración"""
from datetime import date, datetime
#from queue import Empty

from django.urls import reverse
from django.contrib.auth.models import User, Group
#from faker import Faker  #--Librería para generar datos fakes, pero no funciona bien
from rest_framework.test import APITestCase, APIClient
from rest_framework import status

from baseApp.models import Donante, Institucion
from DonacionesApp.models import DonacionBienes,Bien
from DonacionesApp.models import DonacionMonetaria

#fake = Faker()
############# nuevo #####################
class ListarInstitucionesParaDonacionTestCase(APITestCase):

    fixtures = ['group.json']# ,'user.json','donante.json','institucion.json']

    def setUp(self):
        """
        Preparo algunas variables utilizadas en las pruebas de la clase.
        Inicio el cliente, creo 3 usuarios (que será el que tenga el rol
        de Donante) y genero la url .../InstitucionConCBU/.
        """
        self.client = APIClient()
        self.user_donante = User.objects.create_user('john',
                                             'lennon@thebeatles.com',
                                             'johnpassword',
                                             first_name='john',
                                             last_name='lennon')
        # self.user2 = User.objects.create_user('Paul',
        #                                      'paul@thebeatles.com',
        #                                      'paulpassword',
        #                                      first_name='Paul',
        #                                      last_name='McCartney')
        # self.user3 = User.objects.create_user('Ringo',
        #                                      'ringostarr@thebeatles.com',
        #                                      'ringopassword',
        #                                      first_name='Ringo',
        #                                      last_name='Starr')
        self.user_donante.groups.set(Group.objects.filter(id=1))
        self.user_donante.save()
        # self.user2.save()
        # self.user3.save()
        self.donante = Donante.objects.create(nombre= self.user_donante.first_name,
                                            apellido= self.user_donante.last_name,
                                            fecha_nacimiento= date(1983,7,19),
                                            dni= '87654321',
                                            domicilio= 'Calle falsa 789',
                                            localidad= 'local',
                                            provincia= 'prov',
                                            pais= 'pais',
                                            telefono= '1675-138745',
                                            estado_civil= 'soltere',
                                            genero= 'masculine',
                                            ocupacion='reportero deportivo',
                                            usuario= self.user_donante)
        # self.institucion1 = Institucion.objects.create(nombre= self.user2.first_name,
        #                                                 director= "Ramón",
        #                                                 fecha_fundacion= date(1980,1,1),
        #                                                 domicilio= "",
        #                                                 localidad= "",
        #                                                 provincia= "",
        #                                                 pais= "",
        #                                                 telefono= "",
        #                                                 cant_empleados=0,
        #                                                 descripcion= "",
        #                                                 cbu= 256000,
        #                                                 cuenta_bancaria= "123-555555/8",
        #                                                 usuario= self.user2)
        # self.institucion2 = Institucion.objects.create(nombre= self.user3.first_name,
        #                                                 director= "Ringo",
        #                                                 fecha_fundacion= date(1999,1,1),
        #                                                 domicilio= "a",
        #                                                 localidad= "b",
        #                                                 provincia= "c",
        #                                                 pais= "d",
        #                                                 telefono= "",
        #                                                 cant_empleados=10,
        #                                                 descripcion= "",
        #                                                 cbu= None,
        #                                                 cuenta_bancaria= None,
        #                                                 usuario= self.user3)
        self.url = reverse('instituciones_list')

    def test_no_listar_sin_instituciones(self):
        """
        Valido que, si no existen instituciones, al realizar un GET devuelva
        una lista vacía
        """
        self.client.force_login(self.user_donante)
        response = self.client.get(self.url)
        cantidad = Institucion.objects.count()
        self.assertEqual(cantidad,0)
        self.assertEqual(response.data['count'], 0)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_listar_una_institucion(self):
        """
        Valido que al realizar un GET se obtengan todas las instituciones
        """
        user_institucion = User.objects.create_user('Leonardo',
                                             'leo@dan.com',
                                             'leodan222',
                                             first_name='Leo',
                                             last_name='Dan')
        user_institucion.groups.set(Group.objects.filter(id=2))
        user_institucion.save()
        institucion1 = Institucion.objects.create(nombre=user_institucion.first_name,
                                                        director= "Leoncito",
                                                        fecha_fundacion= date(1999,8,4),
                                                        domicilio= "aaa123",
                                                        localidad= "stafe",
                                                        provincia= "stafe",
                                                        pais= "arg",
                                                        telefono= "341000000",
                                                        cant_empleados=20,
                                                        descripcion= "leo dan",
                                                        cbu= 88888888,
                                                        cuenta_bancaria= "",
                                                        usuario= user_institucion)
        self.client.force_login(self.user_donante)
        response = self.client.get(self.url)
        cantidad = Institucion.objects.count()
        self.assertEqual(cantidad,1)
        self.assertEqual(response.data['count'],1)
        
        institucion_response = response.data['results'][0]
        self.assertEqual(institucion.id,institucion_response['id'])
        self.assertEqual(institucion.nombre,institucion_response['nombre'])
        #* Se puede seguir validando los demas campos, no le veo mucho sentido

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_listar_muchas_instituciones(self):
        """
        Valido que al realizar un GET se obtengan todas las instituciones
        """
        user_institucion1 = User.objects.create_user('Leonardo',
                                             'leo@dan.com',
                                             'leodan222',
                                             first_name='Leo',
                                             last_name='Dan')
        user_institucion1.groups.set(Group.objects.filter(id=2))
        user_institucion1.save()
        institucion1 = Institucion.objects.create(nombre=user_institucion1.first_name,
                                                        director= "Leoncito",
                                                        fecha_fundacion= date(1999,8,4),
                                                        domicilio= "aaa123",
                                                        localidad= "stafe",
                                                        provincia= "stafe",
                                                        pais= "arg",
                                                        telefono= "341000000",
                                                        cant_empleados=20,
                                                        descripcion= "leo dan",
                                                        cbu= 88888888,
                                                        cuenta_bancaria= "",
                                                        usuario= user_institucion1)
        self.user_institucion2 = User.objects.create_user('Paul',
                                             'paul@thebeatles.com',
                                             'paulpassword',
                                             first_name='Paul',
                                             last_name='McCartney')
        user_institucion2.groups.set(Group.objects.filter(id=2))
        user_institucion2.save()
        self.institucion2 = Institucion.objects.create(nombre= user_institucion2.first_name,
                                                        director= "Ramón",
                                                        fecha_fundacion= date(1980,1,1),
                                                        domicilio= "",
                                                        localidad= "",
                                                        provincia= "",
                                                        pais= "",
                                                        telefono= "",
                                                        cant_empleados=0,
                                                        descripcion= "",
                                                        cbu= 256000,
                                                        cuenta_bancaria= "123-555555/8",
                                                        usuario= user_institucion2)        
        self.client.force_login(self.user_donante)
        response = self.client.get(self.url)
        cantidad = Institucion.objects.count()
        self.assertEqual(cantidad,2)
        self.assertEqual(response.data['count'],2)
        
        institucion1_response = response.data['results'][1]
        institucion2_response = response.data['results'][0]
        self.assertEqual(institucion1.id,institucion1_response['id'])
        self.assertEqual(institucion1.nombre,institucion1_response['nombre'])
        self.assertEqual(institucion2.id,institucion2_response['id'])
        self.assertEqual(institucion2.nombre,institucion2_response['nombre'])
        #* Se puede seguir validando los demas campos, no le veo mucho sentido

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_no_listar_para_no_donante(self):
        """
        Valido que devuelva error si el usuario que ingresa no es un donante
        """
        self.client.force_login(self.user_donante)
        reponse = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class CreaDonacionBienesTestCase(APITestCase):
    """Caso de Prueba para crear donaciones de bienes"""
    def setUp(self):
        """docstring"""
        self.client = APIClient()
        self.user_donante = User.objects.create_user('john',
                                             'lennon@thebeatles.com',
                                             'johnpassword',
                                             first_name='john',
                                             last_name='lennon')
        self.user_donante.groups.set(Group.objects.filter(id=1))
        self.user_donante.save()
        self.donante = Donante.objects.create(nombre= self.user_donante.first_name,
                                            apellido= self.user_donante.last_name,
                                            fecha_nacimiento= date(1983,7,19),
                                            dni= '87654321',
                                            domicilio= 'Calle falsa 789',
                                            localidad= 'local',
                                            provincia= 'prov',
                                            pais= 'pais',
                                            telefono= '1675-138745',
                                            estado_civil= 'soltere',
                                            genero= 'masculine',
                                            ocupacion='reportero deportivo',
                                            usuario= self.user_donante)
        self.user_institucion = User.objects.create_user('Leonardo',
                                             'leo@dan.com',
                                             'leodan222',
                                             first_name='Leo',
                                             last_name='Dan')
        self.user_institucion.groups.set(Group.objects.filter(id=2))
        self.user_institucion.save()
        self.institucion = Institucion.objects.create(nombre=self.user_institucion.first_name,
                                                        director= "Leoncito",
                                                        fecha_fundacion= date(1999,8,4),
                                                        domicilio= "aaa123",
                                                        localidad= "stafe",
                                                        provincia= "stafe",
                                                        pais= "arg",
                                                        telefono= "341000000",
                                                        cant_empleados=20,
                                                        descripcion= "leo dan",
                                                        cbu= 88888888,
                                                        cuenta_bancaria= "",
                                                        usuario= self.user_institucion)
        self.url = reverse('donacion_bienes')

    def test_crear_donacion_un_bien(self):
        """
        Valido que al realizar un POST con todos los datos de una donacion,
        se genere una instancia Donacion de bienes en la Base de Datos.
        """
        tipo_bien = 1
        nombre_bien = 'hrd'
        descripcion_bien = 'fsdg'
        cantidad_bien = 8
        data = {
            'institucion': self.institucion.id,
            'bienes': 
            [{
                'tipo': tipo_bien,
                'nombre': nombre_bien,
                'descripcion': descripcion_bien,
                'cantidad': cantidad_bien
                }]
        }
        self.client.force_login(self.user_donante)
        response = self.client.post(self.url, data, format='json') #No funcionaba porque no tenía puesto el format
        cantidad_donacion = DonacionBienes.objects.count()
        self.assertEqual(cantidad_donacion, 1)
        cantidad_bienes = Bien.objects.count()
        self.assertEqual(cantidad_bienes,1)
        donacion = DonacionBienes.objects.first()
        bien = Bien.objects.first()
        self.assertEqual(donacion.donante, self.donante)
        self.assertEqual(donacion.institucion.id, response.data['institucion'])
        self.assertEqual(bien.tipo, tipo_bien)
        self.assertEqual(bien.nombre, nombre_bien)
        self.assertEqual(bien.descripcion, descripcion_bien)
        self.assertEqual(bien.cantidad, cantidad_bien)
        self.assertEqual(bien.donacion, donacion)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_crear_donacion_muchos_bienes(self):
        """
        Valido que al realizar un POST con todos los datos de una donacion,
        se genere una instancia Donacion de bienes en la Base de Datos.
        """
        tipo_bien1 = 1
        nombre_bien1 = 'hrd'
        descripcion_bien1 = 'fsdg'
        cantidad_bien1 = 8
        tipo_bien2 = 2
        nombre_bien2 = 'aoe'
        descripcion_bien2 = 'drtn'
        cantidad_bien2 = 13
        data = {
            'institucion': self.institucion.id,
            'bienes': 
            [{
                'tipo': tipo_bien1,
                'nombre': nombre_bien1,
                'descripcion': descripcion_bien1,
                'cantidad': cantidad_bien1
                },
            {
                'tipo': tipo_bien2,
                'nombre': nombre_bien2,
                'descripcion': descripcion_bien2,
                'cantidad': cantidad_bien2
                }]
        }
        self.client.force_login(self.user_donante)
        response = self.client.post(self.url, data, format='json') #No funcionaba porque no tenía puesto el format
        cantidad_donacion = DonacionBienes.objects.count()
        self.assertEqual(cantidad_donacion, 1)
        cantidad_bienes = Bien.objects.count()
        self.assertEqual(cantidad_bienes,2)
        donacion = DonacionBienes.objects.first()
        bien1 = Bien.objects.get(nombre=nombre_bien1)
        bien2 = Bien.objects.get(nombre=nombre_bien2)
        self.assertEqual(donacion.donante, self.donante)
        self.assertEqual(donacion.institucion.id, response.data['institucion'])
        self.assertEqual(bien1.tipo, tipo_bien1)
        self.assertEqual(bien1.nombre, nombre_bien1)
        self.assertEqual(bien1.descripcion, descripcion_bien1)
        self.assertEqual(bien1.cantidad, cantidad_bien1)
        self.assertEqual(bien1.donacion, donacion1)
        self.assertEqual(bien2.tipo, tipo_bien2)
        self.assertEqual(bien2.nombre, nombre_bien2)
        self.assertEqual(bien2.descripcion, descripcion_bien2)
        self.assertEqual(bien2.cantidad, cantidad_bien2)
        self.assertEqual(bien2.donacion, donacion2)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


    def test_no_crear_donacion_bienes_todos_nulos(self):
        """
        Valido que al realizar un POST sin ningún dato, devuelva un mensaje
        HTTP_400 sin generar una instancia Donacion_bienes en la Base de Datos.
        """
        data = {
            "institucion": None,
            "bienes": None
        }
        self.client.force_login(self.user_donante)
        response = self.client.post(self.url, data, format='json')
        cantidad_donaciones = DonacionBienes.objects.count()
        cantidad_bienes = Bien.objects.count()
        self.assertEqual(cantidad_donaciones, 0)
        self.assertEqual(cantidad_bienes,0)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_no_crear_donacion_bienes_todos_enblanco(self):
        """
        Valido que al realizar un POST sin ningún dato, devuelva un mensaje
        HTTP_400 sin generar una instancia Donacion_bienes en la Base de Datos.
        """
        data = {
            "institucion": '',
            "bienes":''       
        }
        self.client.force_login(self.user_donante)
        response = self.client.post(self.url, data, format='json')
        cantidad_donaciones = DonacionBienes.objects.count()
        cantidad_bienes = Bien.objects.count()
        self.assertEqual(cantidad_donaciones, 0)
        self.assertEqual(cantidad_bienes,0)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_no_crear_donacion_bienes_sin_institucion(self):
        """
        Valido que al realizar un POST sin a institucion, devuelva un mensaje
        HTTP_400 sin generar una instancia Donacion_bienes en la Base de Datos.
        """
        tipo_bien = 1
        nombre_bien = 'hrd'
        descripcion_bien = 'fsdg'
        cantidad_bien = 8
        data = {
            "institucion": None,
            "bienes":
            [{
                'tipo': tipo_bien,
                'nombre': nombre_bien,
                'descripcion': descripcion_bien,
                'cantidad': cantidad_bien
                }]
        }
        self.client.force_login(self.user_donante)
        response = self.client.post(self.url, data, format='json')
        cantidad_donaciones = DonacionBienes.objects.count()
        cantidad_bienes = Bien.objects.count()
        self.assertEqual(cantidad_donaciones, 0)
        self.assertEqual(cantidad_bienes,0)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_no_crear_donacion_bienes_con_institucion_inexistente(self):
        """
        Valido que al realizar un POST con una institucion inexistente, devuelva un mensaje
        HTTP_400 sin generar una instancia Donacion_bienes en la Base de Datos.
        """
        tipo_bien = 1
        nombre_bien = 'hrd'
        descripcion_bien = 'fsdg'
        cantidad_bien = 8
        data = {
            "institucion": 12,
            "bienes":
            [{
                'tipo': tipo_bien,
                'nombre': nombre_bien,
                'descripcion': descripcion_bien,
                'cantidad': cantidad_bien
                }]
        }
        self.client.force_login(self.user_donante)
        response = self.client.post(self.url, data, format='json')
        cantidad_donaciones = DonacionBienes.objects.count()
        cantidad_bienes = Bien.objects.count()
        self.assertEqual(cantidad_donaciones, 0)
        self.assertEqual(cantidad_bienes,0)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_no_crear_donacion_bienes_sin_bienes(self):
        """
        Valido que al realizar un POST sin por lo menos un bien, devuelva un mensaje
        HTTP_400 sin generar una instancia Donacion_bienes en la Base de Datos.
        """
        data = {
            "institucion": self.institucion.id,
            "bienes":
            []
        }
        self.client.force_login(self.user_donante)
        response = self.client.post(self.url, data, format='json')
        cantidad_donaciones = DonacionBienes.objects.count()
        cantidad_bienes = Bien.objects.count()
        self.assertEqual(cantidad_donaciones, 0)
        self.assertEqual(cantidad_bienes,0)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_no_crear_donacion_bienes_con_bien_sin_valores(self):
        """
        Valido que al realizar un POST sin por lo menos un bien, devuelva un mensaje
        HTTP_400 sin generar una instancia Donacion_bienes en la Base de Datos.
        """
        data = {
            "institucion": self.institucion.id,
            "bienes":
            [{
                'tipo': None,
                'nombre': None,
                'descripcion': None,
                'cantidad': None
                }]
        }
        self.client.force_login(self.user_donante)
        response = self.client.post(self.url, data, format='json')
        cantidad_donaciones = DonacionBienes.objects.count()
        cantidad_bienes = Bien.objects.count()
        self.assertEqual(cantidad_donaciones, 0)
        self.assertEqual(cantidad_bienes,0)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_no_crear_donacion_bienes_con_bien_sin_valores(self):
        """
        Valido que al realizar un POST sin por lo menos un bien, devuelva un mensaje
        HTTP_400 sin generar una instancia Donacion_bienes en la Base de Datos.
        """
        data = {
            "institucion": self.institucion.id,
            "bienes":
            [{
                'tipo': None,
                'nombre': None,
                'descripcion': None,
                'cantidad': None
                }]
        }
        self.client.force_login(self.user_donante)
        response = self.client.post(self.url, data, format='json')
        cantidad_donaciones = DonacionBienes.objects.count()
        cantidad_bienes = Bien.objects.count()
        self.assertEqual(cantidad_donaciones, 0)
        self.assertEqual(cantidad_bienes,0)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_no_crear_donacion_bienes_con_bien_mal_cargado_1(self):
        """
        Valido que al realizar un POST sin por lo menos un bien, devuelva un mensaje
        HTTP_400 sin generar una instancia Donacion_bienes en la Base de Datos.
        """
        tipo_bien = 1
        nombre_bien = 'hrd'
        descripcion_bien = 'fsdg'
        cantidad_bien = 8
        data = {
            "institucion": self.institucion.id,
            "bienes":
            [{
                'tipo': tipo_bien,
                'nombre': nombre_bien,
                'descripcion': descripcion_bien,
                'cantidad': -1
                }]
        }
        self.client.force_login(self.user_donante)
        response = self.client.post(self.url, data, format='json')
        cantidad_donaciones = DonacionBienes.objects.count()
        cantidad_bienes = Bien.objects.count()
        self.assertEqual(cantidad_donaciones, 0)
        self.assertEqual(cantidad_bienes,0)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_no_crear_donacion_bienes_con_usuario_anonimo(self):
        """
        Valido que al realizar un POST sin por lo menos un bien, devuelva un mensaje
        HTTP_400 sin generar una instancia Donacion_bienes en la Base de Datos.
        """
        tipo_bien = 1
        nombre_bien = 'hrd'
        descripcion_bien = 'fsdg'
        cantidad_bien = 8
        data = {
            "institucion": self.institucion.id,
            "bienes":
            [{
                'tipo': tipo_bien,
                'nombre': nombre_bien,
                'descripcion': descripcion_bien,
                'cantidad': cantidad_bien
                }]
        }
        response = self.client.post(self.url, data, format='json')
        cantidad_donaciones = DonacionBienes.objects.count()
        cantidad_bienes = Bien.objects.count()
        self.assertEqual(cantidad_donaciones, 0)
        self.assertEqual(cantidad_bienes,0)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_no_crear_donacion_bienes_con_usuario_no_donante(self):
        """
        Valido que al realizar un POST sin por lo menos un bien, devuelva un mensaje
        HTTP_400 sin generar una instancia Donacion_bienes en la Base de Datos.
        """
        tipo_bien = 1
        nombre_bien = 'hrd'
        descripcion_bien = 'fsdg'
        cantidad_bien = 8
        data = {
            "institucion": self.institucion.id,
            "bienes":
            [{
                'tipo': tipo_bien,
                'nombre': nombre_bien,
                'descripcion': descripcion_bien,
                'cantidad': cantidad_bien
                }]
        }
        self.client.force_login(self.user_institucion)
        response = self.client.post(self.url, data, format='json')
        cantidad_donaciones = DonacionBienes.objects.count()
        cantidad_bienes = Bien.objects.count()
        self.assertEqual(cantidad_donaciones, 0)
        self.assertEqual(cantidad_bienes,0)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class ListarInstitucionesConCBUParaDonacionTestCase(APITestCase):

    fixtures = ['group.json']# ,'user.json','donante.json','institucion.json']

    def setUp(self):
        """
        Preparo algunas variables utilizadas en las pruebas de la clase.
        Inicio el cliente, creo 3 usuarios (que será el que tenga el rol
        de Donante) y genero la url .../InstitucionConCBU/.
        """
        self.client = APIClient()
        self.user_donante = User.objects.create_user('john',
                                             'lennon@thebeatles.com',
                                             'johnpassword',
                                             first_name='john',
                                             last_name='lennon')
        # self.user2 = User.objects.create_user('Paul',
        #                                      'paul@thebeatles.com',
        #                                      'paulpassword',
        #                                      first_name='Paul',
        #                                      last_name='McCartney')
        # self.user3 = User.objects.create_user('Ringo',
        #                                      'ringostarr@thebeatles.com',
        #                                      'ringopassword',
        #                                      first_name='Ringo',
        #                                      last_name='Starr')
        self.user_donante.groups.set(Group.objects.filter(id=1))
        self.user_donante.save()
        # self.user2.save()
        # self.user3.save()
        self.donante = Donante.objects.create(nombre= self.user_donante.first_name,
                                            apellido= self.user_donante.last_name,
                                            fecha_nacimiento= date(1983,7,19),
                                            dni= '87654321',
                                            domicilio= 'Calle falsa 789',
                                            localidad= 'local',
                                            provincia= 'prov',
                                            pais= 'pais',
                                            telefono= '1675-138745',
                                            estado_civil= 'soltere',
                                            genero= 'masculine',
                                            ocupacion='reportero deportivo',
                                            usuario= self.user_donante)
        # self.institucion1 = Institucion.objects.create(nombre= self.user2.first_name,
        #                                                 director= "Ramón",
        #                                                 fecha_fundacion= date(1980,1,1),
        #                                                 domicilio= "",
        #                                                 localidad= "",
        #                                                 provincia= "",
        #                                                 pais= "",
        #                                                 telefono= "",
        #                                                 cant_empleados=0,
        #                                                 descripcion= "",
        #                                                 cbu= 256000,
        #                                                 cuenta_bancaria= "123-555555/8",
        #                                                 usuario= self.user2)
        # self.institucion2 = Institucion.objects.create(nombre= self.user3.first_name,
        #                                                 director= "Ringo",
        #                                                 fecha_fundacion= date(1999,1,1),
        #                                                 domicilio= "a",
        #                                                 localidad= "b",
        #                                                 provincia= "c",
        #                                                 pais= "d",
        #                                                 telefono= "",
        #                                                 cant_empleados=10,
        #                                                 descripcion= "",
        #                                                 cbu= None,
        #                                                 cuenta_bancaria= None,
        #                                                 usuario= self.user3)
        self.url = reverse('instituciones_list_cbu')

    def test_no_listar_sin_instituciones(self):
        """
        Valido que, si no existen instituciones, al realizar un GET devuelva
        una lista vacía
        """
        self.client.force_login(self.user_donante)
        response = self.client.get(self.url)
        cantidad = Institucion.objects.count()
        self.assertEqual(cantidad,0)
        self.assertEqual(response.data['count'], 0)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_no_listar_una_institucion_sin_CBU(self):
        """
        Valido que al realizar un GET se obtengan todas las instituciones
        """
        user_institucion = User.objects.create_user('Leonardo',
                                             'leo@dan.com',
                                             'leodan222',
                                             first_name='Leo',
                                             last_name='Dan')
        user_institucion.groups.set(Group.objects.filter(id=2))
        user_institucion.save()
        institucion1 = Institucion.objects.create(nombre=user_institucion.first_name,
                                                        director= "Leoncito",
                                                        fecha_fundacion= date(1999,8,4),
                                                        domicilio= "aaa123",
                                                        localidad= "stafe",
                                                        provincia= "stafe",
                                                        pais= "arg",
                                                        telefono= "341000000",
                                                        cant_empleados=20,
                                                        descripcion= "leo dan",
                                                        cuenta_bancaria= "",
                                                        usuario= user_institucion)
        self.client.force_login(self.user_donante)
        response = self.client.get(self.url)
        cantidad = Institucion.objects.count()
        self.assertEqual(cantidad,1)
        self.assertEqual(response.data['count'],0)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_listar_una_institucion_con_CBU(self):
        """
        Valido que al realizar un GET se obtengan todas las instituciones
        """
        user_institucion = User.objects.create_user('Leonardo',
                                             'leo@dan.com',
                                             'leodan222',
                                             first_name='Leo',
                                             last_name='Dan')
        user_institucion.groups.set(Group.objects.filter(id=2))
        user_institucion.save()
        institucion1 = Institucion.objects.create(nombre=user_institucion.first_name,
                                                        director= "Leoncito",
                                                        fecha_fundacion= date(1999,8,4),
                                                        domicilio= "aaa123",
                                                        localidad= "stafe",
                                                        provincia= "stafe",
                                                        pais= "arg",
                                                        telefono= "341000000",
                                                        cant_empleados=20,
                                                        descripcion= "leo dan",
                                                        cbu= 88888888,
                                                        cuenta_bancaria= "",
                                                        usuario= user_institucion)
        self.client.force_login(self.user_donante)
        response = self.client.get(self.url)
        cantidad = Institucion.objects.count()
        self.assertEqual(cantidad,1)
        self.assertEqual(response.data['count'],1)
        
        institucion_response = response.data['results'][0]
        self.assertEqual(institucion.id,institucion_response['id'])
        self.assertEqual(institucion.nombre,institucion_response['nombre'])
        #* Se puede seguir validando los demas campos, no le veo mucho sentido

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_listar_muchas_instituciones(self):
        """
        Valido que al realizar un GET se obtengan todas las instituciones
        """
        user_institucion1 = User.objects.create_user('Leonardo',
                                             'leo@dan.com',
                                             'leodan222',
                                             first_name='Leo',
                                             last_name='Dan')
        user_institucion1.groups.set(Group.objects.filter(id=2))
        user_institucion1.save()
        institucion1 = Institucion.objects.create(nombre=user_institucion1.first_name,
                                                        director= "Leoncito",
                                                        fecha_fundacion= date(1999,8,4),
                                                        domicilio= "aaa123",
                                                        localidad= "stafe",
                                                        provincia= "stafe",
                                                        pais= "arg",
                                                        telefono= "341000000",
                                                        cant_empleados=20,
                                                        descripcion= "leo dan",
                                                        cbu= 88888888,
                                                        cuenta_bancaria= "",
                                                        usuario= user_institucion1)
        self.user_institucion2 = User.objects.create_user('Paul',
                                             'paul@thebeatles.com',
                                             'paulpassword',
                                             first_name='Paul',
                                             last_name='McCartney')
        user_institucion2.groups.set(Group.objects.filter(id=2))
        user_institucion2.save()
        self.institucion2 = Institucion.objects.create(nombre= user_institucion2.first_name,
                                                        director= "Ramón",
                                                        fecha_fundacion= date(1980,1,1),
                                                        domicilio= "",
                                                        localidad= "",
                                                        provincia= "",
                                                        pais= "",
                                                        telefono= "",
                                                        cant_empleados=0,
                                                        descripcion= "",
                                                        cbu= 256000,
                                                        cuenta_bancaria= "123-555555/8",
                                                        usuario= user_institucion2)        
        self.client.force_login(self.user_donante)
        response = self.client.get(self.url)
        cantidad = Institucion.objects.count()
        self.assertEqual(cantidad,2)
        self.assertEqual(response.data['count'],2)
        
        institucion1_response = response.data['results'][1]
        institucion2_response = response.data['results'][0]
        self.assertEqual(institucion1.id,institucion1_response['id'])
        self.assertEqual(institucion1.nombre,institucion1_response['nombre'])
        self.assertEqual(institucion2.id,institucion2_response['id'])
        self.assertEqual(institucion2.nombre,institucion2_response['nombre'])
        #* Se puede seguir validando los demas campos, no le veo mucho sentido

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_no_listar_para_no_donante(self):
        """
        Valido que devuelva error si el usuario que ingresa no es un donante
        """
        self.client.force_login(self.user_donante)
        reponse = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class CrearDonacionMonetariaTestCase(APITestCase):
    """Caso de Prueba para crear donaciones monetarias"""
    fixtures = ['group.json']# ,'user.json','donante.json','institucion.json']

    def setUp(self):
        """docstring"""
        self.client = APIClient()
        self.user_donante = User.objects.create_user('john',
                                             'lennon@thebeatles.com',
                                             'johnpassword',
                                             first_name='john',
                                             last_name='lennon')
        self.user_donante.groups.set(Group.objects.filter(id=1))
        self.user_donante.save()
        self.donante = Donante.objects.create(nombre= self.user_donante.first_name,
                                            apellido= self.user_donante.last_name,
                                            fecha_nacimiento= date(1983,7,19),
                                            dni= '87654321',
                                            domicilio= 'Calle falsa 789',
                                            localidad= 'local',
                                            provincia= 'prov',
                                            pais= 'pais',
                                            telefono= '1675-138745',
                                            estado_civil= 'soltere',
                                            genero= 'masculine',
                                            ocupacion='reportero deportivo',
                                            usuario= self.user_donante)
        self.user_institucion = User.objects.create_user('Leonardo',
                                             'leo@dan.com',
                                             'leodan222',
                                             first_name='Leo',
                                             last_name='Dan')
        self.user_institucion.groups.set(Group.objects.filter(id=2))
        self.user_institucion.save()
        self.institucion = Institucion.objects.create(nombre=self.user_institucion.first_name,
                                                        director= "Leoncito",
                                                        fecha_fundacion= date(1999,8,4),
                                                        domicilio= "aaa123",
                                                        localidad= "stafe",
                                                        provincia= "stafe",
                                                        pais= "arg",
                                                        telefono= "341000000",
                                                        cant_empleados=20,
                                                        descripcion= "leo dan",
                                                        cbu= 88888888,
                                                        cuenta_bancaria= "",
                                                        usuario= self.user_institucion)
        self.url = reverse('donacion_monetaria')

    def test_crear_donacion_monetaria(self):
        """
        Valido que al realizar un POST con todos los datos de una donacion,
        se genere una instancia Donacion de bienes en la Base de Datos.
        """
        monto = 19375
        data = {
            'institucion': self.institucion.id,
            'monto': monto
        }
        self.client.force_login(self.user_donante)
        response = self.client.post(self.url, data, format='json') #No funcionaba porque no tenía puesto el format
        cantidad_donacion = DonacionMonetaria.objects.count()
        self.assertEqual(cantidad_donacion, 1)
        donacion = DonacionMonetaria.objects.first()

        self.assertEqual(donacion.donante, self.donante)
        self.assertEqual(donacion.institucion.id, response.data['institucion'])
        self.assertEqual(donacion.monto, monto)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_no_crear_donacion_monetaria_institucion_incorrecto(self):
        """
        Valido que al realizar un POST con todos los datos de una donacion,
        se genere una instancia Donacion de bienes en la Base de Datos.
        """
        monto = 19375
        data = {
            'institucion': 7,
            'monto': monto
        }
        self.client.force_login(self.user_donante)
        response = self.client.post(self.url, data, format='json')
        cantidad_donaciones = DonacionBienes.objects.count()
        self.assertEqual(cantidad_donaciones, 0)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_no_crear_donacion_monetaria_sin_monto(self):
        """
        Valido que al realizar un POST con todos los datos de una donacion,
        se genere una instancia Donacion de bienes en la Base de Datos.
        """
        data = {
            'institucion': self.institucion.id,
            'monto': 0
        }
        self.client.force_login(self.user_donante)
        response = self.client.post(self.url, data, format='json')
        cantidad_donaciones = DonacionBienes.objects.count()
        self.assertEqual(cantidad_donaciones, 0)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_no_crear_donacion_monetaria_todos_nulos(self):
        """
        Valido que al realizar un POST sin ningún dato, devuelva un mensaje
        HTTP_400 sin generar una instancia Donacion_bienes en la Base de Datos.
        """
        data = {
            "institucion": None,
            "monto": None
        }
        self.client.force_login(self.user_donante)
        response = self.client.post(self.url, data, format='json')
        cantidad_donaciones = DonacionBienes.objects.count()
        self.assertEqual(cantidad_donaciones, 0)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_no_crear_donacion_monetaria_todos_enblanco(self):
        """
        Valido que al realizar un POST sin ningún dato, devuelva un mensaje
        HTTP_400 sin generar una instancia Donacion_bienes en la Base de Datos.
        """
        data = {
            "institucion": '',
            "monto":0       
        }
        self.client.force_login(self.user_donante)
        response = self.client.post(self.url, data, format='json')
        cantidad_donaciones = DonacionBienes.objects.count()
        cantidad_bienes = Bien.objects.count()
        self.assertEqual(cantidad_donaciones, 0)
        self.assertEqual(cantidad_bienes,0)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_no_crear_donacion_bienes_sin_institucion(self):
        """
        Valido que al realizar un POST sin a institucion, devuelva un mensaje
        HTTP_400 sin generar una instancia Donacion_bienes en la Base de Datos.
        """
        tipo_bien = 1
        nombre_bien = 'hrd'
        descripcion_bien = 'fsdg'
        cantidad_bien = 8
        data = {
            "institucion": None,
            "bienes":
            [{
                'tipo': tipo_bien,
                'nombre': nombre_bien,
                'descripcion': descripcion_bien,
                'cantidad': cantidad_bien
                }]
        }
        self.client.force_login(self.user_donante)
        response = self.client.post(self.url, data, format='json')
        cantidad_donaciones = DonacionBienes.objects.count()
        cantidad_bienes = Bien.objects.count()
        self.assertEqual(cantidad_donaciones, 0)
        self.assertEqual(cantidad_bienes,0)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


######################################################


class DonanacionBienesListCreateTestCase(APITestCase):
    """
    Pruebas realizadas sobre el listado y la creación de instancias de la
    clase DonacionBienes.
    """
    fixtures = ['group.json']

    def setUp(self):
        """
        Preparo algunas variables utilizadas en las pruebas de la clase.
        Inicio el cliente, creo el usuario john (que será el que tenga el rol
        de Donante) y genero la url .../eligeInstitucion/donarBienes/.
        """
        self.client = APIClient()
        self.user1 = User.objects.create_user('john',
                                             'lennon@thebeatles.com',
                                             'johnpassword',
                                             first_name='john',
                                             last_name='lennon')
        self.user2 = User.objects.create_user('Paul',
                                             'paul@thebeatles.com',
                                             'paulpassword',
                                             first_name='Paul',
                                             last_name='McCartney')
        self.user1.groups.set(Group.objects.filter(id=1))
        self.user2.groups.set(Group.objects.filter(id=2))
        self.user1.save()
        self.user2.save()
        self.donante = Donante.objects.create(nombre= self.user1.first_name,
                                            apellido= self.user1.last_name,
                                            fecha_nacimiento= date(1983,7,19),
                                            dni= '87654321',
                                            domicilio= 'Calle falsa 789',
                                            localidad= 'local',
                                            provincia= 'prov',
                                            pais= 'pais',
                                            telefono= '1675-138745',
                                            estado_civil= 'soltere',
                                            genero= 'masculine',
                                            ocupacion='reportero deportivo',
                                            usuario= self.user1)
        self.institucion = Institucion.objects.create(nombre= self.user2.first_name,
                                                        director= "Ramón",
                                                        fecha_fundacion= date(1980,1,1),
                                                        domicilio= "",
                                                        localidad= "",
                                                        provincia= "",
                                                        pais= "",
                                                        telefono= "",
                                                        cant_empleados=0,
                                                        descripcion= "",
                                                        cbu= 256000,
                                                        cuenta_bancaria= "",
                                                        usuario= self.user2)
        self.url = reverse('donacion_bienes')
        self.client.force_login(self.user1)

    def test_crear_donacion_bienes(self):
        """
        Valido que al realizar un POST con todos los datos de una donacion,
        se genere una instancia Donacion de bienes en la Base de Datos.
        """
        data = {
            'institucion': self.institucion.id,
            # 'cod_estado': 1,
            # 'fecha_creacion': datetime.now(),
            # 'fecha_retiro': 'null',
            # 'fecha_cancelacion': 'null',
            # 'fecha_aceptacion': 'null',
            # 'motivo_cancelacion':'',
            # 'fecha_entrega_real':'null',
            'bienes': 
            [{
                'tipo': 1,
                'nombre': 'hrd',
                'descripcion': 'fsdg',
                'cantidad': 8
                }]           
        }
        response = self.client.post(self.url, data, format='json') #No funcionaba porque no tenía puesto el format
        cantidad_donacion = DonacionBienes.objects.count()
        self.assertEqual(cantidad_donacion, 1)
        cantidad_bienes = Bien.objects.count()
        self.assertEqual(cantidad_bienes,1)
        donacion = DonacionBienes.objects.get(donante=response.data['donante']) 
        bien = Bien.objects.first()
        self.assertEqual(donacion.donante, self.donante)
        self.assertEqual(donacion.institucion.id, response.data['institucion'])
        self.assertEqual(bien.tipo, 1)
        self.assertEqual(bien.nombre, 'hrd')
        self.assertEqual(bien.descripcion, 'fsdg')
        self.assertEqual(bien.cantidad, 8)
        self.assertEqual(bien.donacion, donacion)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_no_crear_donacion_bienes_todos_nulos(self): #Funciona
        """
        Valido que al realizar un POST sin ningún dato, devuelva un mensaje
        HTTP_400 sin generar una instancia Donacion_bienes en la Base de Datos.
        """
        data = {
            "institucion": 'null',
            # "cod_estado": 'null',
            # "fecha_creacion": 'null',
            # "fecha_retiro":'null',
            # "fecha_creacion":'null',
            # "fecha_cancelacion":'null',
            # "fecha_aceptacion":'null',
            # "motivo_cancelacion":'null',
            # "fecha_entrega_real":'null',
            "bienes":'null'       
        }
        response = self.client.post(self.url, data, format='json')
        cantidad_donaciones = DonacionBienes.objects.count()
        cantidad_bienes = Bien.objects.count()
        self.assertEqual(cantidad_donaciones, 0)
        self.assertEqual(cantidad_bienes,0)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_no_crear_donacion_bienes_todos_enblanco(self): #Funciona
        """
        Valido que al realizar un POST sin ningún dato, devuelva un mensaje
        HTTP_400 sin generar una instancia Donacion_bienes en la Base de Datos.
        """
        data = {
            "institucion": '',
            # "cod_estado": '',
            # "fecha_creacion": '',
            # "fecha_retiro":'',
            # "fecha_creacion":'',
            # "fecha_cancelacion":'',
            # "fecha_aceptacion":'',
            # "motivo_cancelacion":'',
            # "fecha_entrega_real":'',
            "bienes":''       
        }
        response = self.client.post(self.url, data, format='json')
        cantidad_donaciones = DonacionBienes.objects.count()
        cantidad_bienes = Bien.objects.count()
        self.assertEqual(cantidad_donaciones, 0)
        self.assertEqual(cantidad_bienes,0)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


    def test_listar_donaciones(self):
        self.url = reverse('ver_donacion')
        self.user3 = User.objects.create_user('Leonardo',
                                             'leo@dan.com',
                                             'leodan222',
                                             first_name='Leo',
                                             last_name='Dan')
        self.user3.groups.set(Group.objects.filter(id=2))
        self.user3.save()
        self.institucion2 = Institucion.objects.create(nombre= self.user3.first_name,
                                                        director= "Leoncito",
                                                        fecha_fundacion= date(1999,8,4),
                                                        domicilio= "aaa123",
                                                        localidad= "stafe",
                                                        provincia= "stafe",
                                                        pais= "arg",
                                                        telefono= "341000000",
                                                        cant_empleados=20,
                                                        descripcion= "leo dan",
                                                        cbu= 88888888,
                                                        cuenta_bancaria= "",
                                                        usuario= self.user3)
        self.institucion2.save()
        self.donacion1 = DonacionBienes.objects.create(   
            donante = self.donante,
            institucion = self.institucion,
            cod_estado = 1,
            fecha_creacion = datetime.now()  
        )
        self.donacion2 = DonacionBienes.objects.create(   
            donante = self.donante,
            institucion = self.institucion2,
            cod_estado = 1,
            fecha_creacion = datetime.now()       
        )
        self.donacion1.save()
        self.donacion2.save()
        self.bien1 = Bien.objects.create(
                tipo = 1,
                nombre = 'hrd',
                descripcion = 'fsdg',
                cantidad = 8,
                donacion = self.donacion1      
        )
        self.bien2 = Bien.objects.create(
                tipo = 3,
                nombre = 'asd',
                descripcion = 'gt',
                cantidad = 11,
                donacion = self.donacion2      
        )
        self.bien3 = Bien.objects.create(
                tipo = 2,
                nombre = 'fdhfdf',
                descripcion = 'aaaa',
                cantidad = 7,
                donacion = self.donacion2     
        )
        self.bien1.save()
        self.bien2.save()
        self.bien3.save()
        self.client.force_login(self.institucion)
        response = self.client.get(self.url)
        #print(response.data)
        cantidad = len(response.data['results'])
        donacion_response = response.data['results'][0]
        donacion2_response = response.data['results'][1]
        cantidad_bienes = Bien.objects.count()
        self.assertEqual(cantidad,2)
        self.assertEqual(self.donacion1.id,donacion_response['id'])
        self.assertEqual(self.donacion2.id,donacion2_response['id'])
        self.assertEqual(cantidad_bienes,3)

    def test_aceptar_donaciones(self):
        ''' Valido que se acepte la donacion elegida de manera correcta '''
        self.donacion1 = DonacionBienes.objects.create(   
            donante = self.donante,
            institucion = self.institucion,
            cod_estado = 1,
            fecha_creacion = datetime.now(),
            fecha_aceptacion = None,
            fecha_cancelacion = None,
            motivo_cancelacion = None  
        )
        
        self.donacion1.save()
        self.bien1 = Bien.objects.create(
                tipo = 1,
                nombre = 'hrd',
                descripcion = 'fsdg',
                cantidad = 8,
                donacion = self.donacion1      
        )
        self.bien2 = Bien.objects.create(
                tipo = 3,
                nombre = 'asd',
                descripcion = 'gt',
                cantidad = 11,
                donacion = self.donacion1      
        )
        self.bien3 = Bien.objects.create(
                tipo = 2,
                nombre = 'fdhfdf',
                descripcion = 'aaaa',
                cantidad = 7,
                donacion = self.donacion1     
        )
        self.bien1.save()
        self.bien2.save()
        self.bien3.save()
        self.url = reverse('aceptar_donacion', args=[self.donacion1.id])
        data = {
            "cod_estado": 2,
            #"motivo_cancelacion": None,
            "fecha_aceptacion": datetime.now()
            #"fecha_cancelacion": None
        }
        data2 = {
            "cod_estado": 0,
            "motivo_cancelacion": "Cancelado",
            #"fecha_aceptacion": None,
            "fecha_cancelacion": datetime.now()
        }
        #print(self.url)
        response = self.client.put(self.url,data) #Acepta donacion
        response2 = self.client.put(self.url,data2) #Cancela donacion
        """Valido que el response sea correcto tanto para la aceptacion como para la cancelacion"""
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response2.status_code, status.HTTP_200_OK)

        """Valido datos al aceptar donacion"""
        self.assertEqual(response.data['cod_estado'],2)
        #Fecha de aceptación no se puede validar porque es un campo read_only
        #print(response)
        """Valido datos al cancelar donacion"""
        self.assertEqual(response2.data['cod_estado'],0)
        self.assertEqual(response2.data['motivo_cancelacion'],"Cancelado")
        #Fecha de cancelacion no se puede validar porque es un campo read_only

#! Comienzo a validar las donaciones monetarias!

class DonanacionMonetariaCreateTestCase(APITestCase):
    """
    Pruebas realizadas sobre el listado de Instituciones con CBU y la creación de instancias de la
    clase DonacionMonetaria.
    """
    def setUp(self):
        """
        Preparo algunas variables utilizadas en las pruebas de la clase.
        Inicio el cliente, creo 3 usuarios (que será el que tenga el rol
        de Donante) y genero la url .../InstitucionConCBU/.
        """
        self.client = APIClient()
        self.user1 = User.objects.create_user('john',
                                             'lennon@thebeatles.com',
                                             'johnpassword',
                                             first_name='john',
                                             last_name='lennon')
        self.user2 = User.objects.create_user('Paul',
                                             'paul@thebeatles.com',
                                             'paulpassword',
                                             first_name='Paul',
                                             last_name='McCartney')
        self.user3 = User.objects.create_user('Ringo',
                                             'ringostarr@thebeatles.com',
                                             'ringopassword',
                                             first_name='Ringo',
                                             last_name='Starr')
        self.user1.save()
        self.user2.save()
        self.user3.save()
        self.donante = Donante.objects.create(nombre= self.user1.first_name,
                                            apellido= self.user1.last_name,
                                            fecha_nacimiento= date(1983,7,19),
                                            dni= '87654321',
                                            domicilio= 'Calle falsa 789',
                                            localidad= 'local',
                                            provincia= 'prov',
                                            pais= 'pais',
                                            telefono= '1675-138745',
                                            estado_civil= 'soltere',
                                            genero= 'masculine',
                                            ocupacion='reportero deportivo',
                                            usuario= self.user1)
        self.institucion1 = Institucion.objects.create(nombre= self.user2.first_name,
                                                        director= "Ramón",
                                                        fecha_fundacion= date(1980,1,1),
                                                        domicilio= "",
                                                        localidad= "",
                                                        provincia= "",
                                                        pais= "",
                                                        telefono= "",
                                                        cant_empleados=0,
                                                        descripcion= "",
                                                        cbu= 256000,
                                                        cuenta_bancaria= "123-555555/8",
                                                        usuario= self.user2)
        self.institucion2 = Institucion.objects.create(nombre= self.user3.first_name,
                                                        director= "Ringo",
                                                        fecha_fundacion= date(1999,1,1),
                                                        domicilio= "a",
                                                        localidad= "b",
                                                        provincia= "c",
                                                        pais= "d",
                                                        telefono= "",
                                                        cant_empleados=10,
                                                        descripcion= "",
                                                        cbu= None,
                                                        cuenta_bancaria= None,
                                                        usuario= self.user3)
        self.url = reverse('instituciones_list_cbu')

    def test_listar_instituciones_con_cbu(self):
        """
        Valido que al realizar un GET se obtengan todas las instituciones que esten bancarizadas
        """
        response = self.client.get(self.url)
        #print(response.data)
        cantidad = len(response.data['results'])
        institucion_response = response.data['results'][0]
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(cantidad,1)
        self.assertEqual(self.institucion1.nombre,institucion_response['nombre']) #valido nombre institucion1
        #* Se puede seguir validando los demas campos, no le veo mucho sentido

    def test_transferencia_institucion_elegida(self):
        """
        Valido que al realizar un GET se obtenga la información de la institucion bancarizada elegida
        """
        self.url = reverse('institucion_elegida_cbu', args=[self.institucion1.id])
        data = {
            "nombre": self.institucion1.nombre,
            "cbu": self.institucion1.cbu,
            "cuenta_bancaria": "1425-5869/0"
        }
        response = self.client.get(self.url,data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.institucion1.nombre,response.data['nombre'])
        self.assertEqual(response.data['cbu'],self.institucion1.cbu)

    def test_transferencia_institucion_sin_cbu(self):
        """
        Valido que al realizar un GET se obtenga la información de la institucion bancarizada elegida
        """
        self.url = reverse('institucion_elegida_cbu', args=[self.institucion2.id])
        data = {
            'nombre': self.institucion2.nombre,
            'cbu': 'null',
            'cuenta_bancaria': 'null'
        }      
        response = self.client.get(self.url,data,format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        #self.assertEqual(self.institucion2.nombre,response.data['results'][0]['nombre'])
        self.assertIsNone(self.institucion2.cbu)

#############################################################
    def test_crear_donacion_monetaria(self):
        """
        Valido que al ingresar los datos requeridos se cree una donacion monetaria
        """
        self.url = reverse('donacion_monetaria')
        data = {
            'donante': self.donante.id,
            'institucion': self.institucion1.id,
            'monto': 500
        }      
        response = self.client.post(self.url,data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        cantidad = DonacionMonetaria.objects.count()
        self.assertEqual(cantidad,1)
        #self.assertEqual(self.institucion2.nombre,response.data['results'][0]['nombre'])
        #self.assertIsNone(self.institucion2.cbu)

    def test_NO_crear_donacion_monetaria_monto_menorigual_a_0(self):
        """
        Valido que al ingresar un monto <= 0 no se cree la donación
        """
        #self.url = reverse('donacion_monetaria')
        data = {
            'donante': self.donante.id,
            'institucion': self.institucion1.id,
            'monto': 0
        }      
        response = self.client.post(self.url,data)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        cantidad = DonacionMonetaria.objects.count()
        self.assertEqual(cantidad,0)
        """El error 405 No Permitido ocurre cuando el servidor web está configurado de una forma que no permita 
        que usted pueda llevar a cabo una acción para un URL en particular.
        Es un código de respuesta de estado HTTP que indica que el método requerido es conocido por el servidor, 
        pero no es soportado por la fuente objetivo."""

    def test_NO_crear_donacion_monetaria_institucion_sin_CBU(self):
        """
        Valido que al ingresar una institución sin cbu no se cree la donación
        """
        #Nose como está funcionando este test, pero funciona, no tocar.
        data = {
            'donante': self.donante.id,
            'institucion': self.institucion2.id,
            'monto': 10
        }      
        response = self.client.post(self.url,data)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        cantidad = DonacionMonetaria.objects.count()
        self.assertEqual(cantidad,0)

    def test_listar_transferencias(self):
        """
        Valido que al realizar un GET obtenga la lista de las transferencias
        """
        self.transf1 = DonacionMonetaria.objects.create(
            donante = self.donante,
            institucion = self.institucion1,
            monto = 5000,
            cod_estado = 3,
            fecha_transferencia = date.today(),
            fecha_creacion = datetime.now()
        )
        self.transf2 = DonacionMonetaria.objects.create(
            donante = self.donante,
            institucion = self.institucion1,
            monto = 2000,
            cod_estado = 3,
            fecha_transferencia = date.today(),
            fecha_creacion = datetime.now()
        )
        self.transf2.save()
        self.transf1.save()
        self.url = reverse('ver_transferencia')
        response = self.client.get(self.url)
        cantidad = len(response.data['results'])
        transferencia_response = response.data['results'][0]
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(cantidad,2)
        #print(response.data['institucion'])
        #self.assertEqual(self.institucion1.id,transferencia_response['institucion'])

    def test_aceptar_transferencia(self):
        """
        Valido que al realizar un PUT se actualice el codigo de estado a 4 (Recibida)
        """
        self.transf3 = DonacionMonetaria.objects.create(
            donante = self.donante,
            institucion = self.institucion1,
            monto = 5000,
            cod_estado = 3,
            fecha_transferencia = date.today(),
            fecha_creacion = datetime.now()
        )
        self.transf3.save()
        data = {
            'cod_estado': 4,
            'motivo_cancelacion': None,
            'fecha_aceptacion': datetime.now(),
            'fecha_cancelacion': None
        }     
        self.url = reverse('aceptar_transferencia',args=[self.transf3.id])
        response = self.client.put(self.url,data,format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['cod_estado'],4)
        #self.assertIsNone(self.institucion2.cbu)

    def test_rechazar_transferencia(self):
        """
        Valido que al realizar un PUT se actualice el codigo de estado a 0 (Cancelada)
        """
        self.transf3 = DonacionMonetaria.objects.create(
            donante = self.donante,
            institucion = self.institucion1,
            monto = 5000,
            cod_estado = 3,
            fecha_transferencia = date.today(),
            fecha_creacion = datetime.now()
        )
        self.transf3.save()
        data = {
            'cod_estado': 0,
            'motivo_cancelacion': "No llego",
            'fecha_aceptacion': None,
            'fecha_cancelacion': datetime.now()
        }     
        self.url = reverse('aceptar_transferencia',args=[self.transf3.id])
        response = self.client.put(self.url,data,format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['cod_estado'],0)
        self.assertEqual(response.data['motivo_cancelacion'],"No llego")
        #self.assertIsNone(self.institucion2.cbu)

    def test_no_aceptacion_de_transferencia_sin_enviar_transferencia(self):
        """
        Valido que al realizar un PUT a una donación que fue creada pero no enviada falle
        """
        self.transf3 = DonacionMonetaria.objects.create(
            donante = self.donante,
            institucion = self.institucion1,
            monto = 5000,
            cod_estado = 1,
            fecha_transferencia = date.today(),
            fecha_creacion = datetime.now()
        )
        self.transf3.save()
        data = {
            'cod_estado': 4,
            'motivo_cancelacion': None,
            'fecha_aceptacion': datetime.now(),
            'fecha_cancelacion': None
        }     
        self.url = reverse('aceptar_transferencia',args=[self.transf3.id])
        response = self.client.put(self.url,data,format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
