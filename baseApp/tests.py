"""Pruebas de integración"""
from datetime import date

from django.urls import reverse
from django.contrib.auth.models import User

from rest_framework.test import APITestCase, APIClient
from rest_framework import status

from baseApp.models import Donante

# pylint: disable=no-member

class DonantesListCreateTestCase(APITestCase):
    """
    Pruebas realizadas sobre el listado y la creación de instancias de la
    clase Donante.
    """
    def setUp(self):
        """
        Preparo algunas variables utilizadas en las pruebas de la clase.
        Inicio el cliente, creo el usuario john (que será el que tenga el rol
        de Donante) y genero la url .../donantes/.
        """
        self.client = APIClient()
        self.user = User.objects.create_user('john',
                                             'lennon@thebeatles.com',
                                             'johnpassword',
                                             first_name='john',
                                             last_name='lennon')
        self.user.save()
        self.url = reverse('donantes-list')

    def test_crear_donante(self):
        """
        Valido que al realizar un POST con todos los datos de un Donante,
        se genere una instancia Donante en la Base de Datos.
        """
        data = {
            'nombre': self.user.first_name,
            'apellido': self.user.last_name,
            'fecha_nacimiento': date(1983,7,19),
            'dni': '87654321',
            'domicilio': 'Calle falsa 789',
            'localidad': 'local',
            'provincia': 'prov',
            'pais': 'pais',
            'telefono': '1675-138745',
            'estado_civil': 'soltere',
            'genero': 'masculine',
            'ocupacion': 'reportero deportivo',
            'usuario': self.user.id
        }
        response = self.client.post(self.url, data)
        cantidad = Donante.objects.count()
        if cantidad > 0:
            donante = Donante.objects.get(id=response.data['id'])
        self.assertEqual(cantidad, 1)
        self.assertEqual(donante.nombre, self.user.first_name)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_no_crear_donante_con_todos_nulos(self):
        """
        Valido que al realizar un POST sin ningún dato, devuelva un mensaje
        HTTP_400 sin generar una instancia Donante en la Base de Datos.
        """
        data = {
            'nombre': 'null',
            'apellido': 'null',
            'fecha_nacimiento': 'null',  #date(1900,1,1),
            'dni': 'null',
            'domicilio': 'null',
            'localidad': 'null',
            'provincia': 'null',
            'pais': 'null',
            'telefono': 'null',
            'estado_civil': 'null',
            'genero': 'null',
            'ocupacion': 'null',
            'usuario': 'null' #0
        }
        response = self.client.post(self.url, data)
        cantidad = Donante.objects.count()
        self.assertEqual(cantidad, 0)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_no_crear_donante_con_todos_blancos(self):
        """
        Valido que al realizar un POST con todos los datos blancos, devuelva
        un mensaje HTTP_400 sin generar una instancia Donante en la Base de
        Datos.
        """
        data = {
            'nombre': '',
            'apellido': '',
            'fecha_nacimiento': '',  #El blanco no existe para valores date
            'dni': '',
            'domicilio': '',
            'localidad': '',
            'provincia': '',
            'pais': '',
            'telefono': '',
            'estado_civil': '',
            'genero': '',
            'ocupacion': '',
            'usuario': '' #El blanco no existe para claves foraneas
        }
        response = self.client.post(self.url,data)
        cantidad = Donante.objects.count()
        self.assertEqual(cantidad,0)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_crear_donante_con_datos_minimos(self):
        """
        Valido que al realizar un POST con los datos mínimos necesarios para
        registrar un Donante, se genere una instancia Donante en la Base de
        Datos.
        """

        #? Esto se debe definir según nuetro criterio
        data = {
            'nombre': self.user.first_name,
            'apellido': self.user.last_name,
            'fecha_nacimiento': '',
            'dni': '',
            'domicilio': '',
            'localidad': '',
            'provincia': '',
            'pais': '',
            'telefono': '',
            'estado_civil': '',
            'genero': '',
            'ocupacion': '',
            'usuario': self.user.id
        }
        response = self.client.post(self.url,data)
        cantidad = Donante.objects.count()
        if cantidad > 0:
            donante = Donante.objects.get(id=response.data['id'])
        self.assertEqual(cantidad,1)
        self.assertIsNone(response.data['fecha_nacimiento'])
        self.assertEqual(donante.nombre, self.user.first_name)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_nombre_apellido_usuario_donante(self):
        """
        Valido que al realizar un POST con los datos mínimos necesarios para
        registrar un Donante, se genere una instancia Donante en la Base de
        Datos vinculado a un usuario ya registrado (campo usuario) y que tenga
        el mismo nombre y apellido que los registrados para el usuario
        asociado.
        """
        data = {
            'nombre': self.user.first_name,
            'apellido': self.user.last_name,
            'fecha_nacimiento': '',
            'dni': '',
            'domicilio': '',
            'localidad': '',
            'provincia': '',
            'pais': '',
            'telefono': '',
            'estado_civil': '',
            'genero': '',
            'ocupacion': '',
            'usuario': self.user.id
        }
        response = self.client.post(self.url,data)
        cantidad = Donante.objects.count()
        if cantidad > 0:
            donante = Donante.objects.get(id=response.data['id'])
        self.assertEqual(cantidad,1)
        self.assertEqual(donante.nombre, self.user.first_name)
        self.assertEqual(donante.apellido, self.user.last_name)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_listar_donante(self):
        """
        Valido que al realizar un GET después de registrar un solo Donante en
        la Base de Datos, devuelva sólo los datos del Donante registrado.
        """
        donante = Donante.objects.create(
            nombre=self.user.first_name,
            apellido=self.user.last_name,
            fecha_nacimiento=date(1998,2,5),
            dni='12345678',
            domicilio='Calle falsa 123',
            localidad='localidad',
            provincia='provincia',
            pais='pais',
            telefono='3471622222',
            estado_civil='soltara',
            ocupacion='mecanico dental',
            usuario=self.user
        )
        donante.save()
        response = self.client.get(self.url)
        cantidad = len(response.data['results'])
        self.assertEqual(cantidad,1)
        donante_response = response.data['results'][0]
        self.assertEqual(donante.nombre,donante_response['nombre'])
        self.assertEqual(donante.apellido,donante_response['apellido'])
        self.assertEqual(donante.fecha_nacimiento,
                    date.fromisoformat(donante_response['fecha_nacimiento']))
        self.assertEqual(donante.dni,donante_response['dni'])
        self.assertEqual(donante.domicilio,donante_response['domicilio'])
        self.assertEqual(donante.localidad,donante_response['localidad'])
        self.assertEqual(donante.provincia,donante_response['provincia'])
        self.assertEqual(donante.pais,donante_response['pais'])
        self.assertEqual(donante.telefono,donante_response['telefono'])
        self.assertEqual(donante.estado_civil,
                    donante_response['estado_civil'])
        self.assertEqual(donante.ocupacion,donante_response['ocupacion'])
        self.assertEqual(donante.usuario.id,donante_response['usuario'])

    def test_listar_varios_donantes(self):
        """
        Valido que al realizar un GET después de registrar dos Donantes en la
        Base de Datos, devuelva los datos de los donantes registrados.
        """
        donante1 = Donante.objects.create(
            nombre=self.user.first_name,
            apellido=self.user.last_name,
            fecha_nacimiento=date(1998,2,5),
            dni='12345678',
            domicilio='Calle falsa 123',
            localidad='localidad',
            provincia='provincia',
            pais='pais',
            telefono='3471622222',
            estado_civil='soltara',
            ocupacion='mecanico dental',
            usuario=self.user
        )
        user2 = User.objects.create_user('paul',
                                         'paul@thebeatles.com',
                                         'paulpassword',
                                         first_name='paul',
                                         last_name='mccarny')
        donante2 = Donante.objects.create(
            nombre=user2.first_name,
            apellido=user2.last_name,
            fecha_nacimiento=date(1998,2,5),
            dni='12345678',
            domicilio='Calle falsa 123',
            localidad='localidad',
            provincia='provincia',
            pais='pais',
            telefono='3471622222',
            estado_civil='soltara',
            ocupacion='mecanico dental',
            usuario=user2
        )
        response = self.client.get(self.url)
        cantidad = len(response.data['results'])
        self.assertEqual(cantidad,2)
        donante1_response = response.data['results'][0]
        donante2_response = response.data['results'][1]
        self.assertEqual(donante1.nombre,donante1_response['nombre'])
        self.assertEqual(donante1.apellido,donante1_response['apellido'])
        self.assertEqual(donante2.nombre,donante2_response['nombre'])
        self.assertEqual(donante2.apellido,donante2_response['apellido'])

    def test_lista_donantes_vacia(self):
        """
        Valido que al realizar un GET cuando no existen donantes en la Base de
        Datos, no devuelva nada.
        """
        response = self.client.get(self.url)
        cantidad = len(response.data['results'])
        self.assertEqual(cantidad,0)
