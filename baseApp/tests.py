"""Pruebas de integración"""
from datetime import date

from django.urls import reverse
from django.contrib.auth.models import User

from rest_framework.test import APITestCase, APIClient
from rest_framework import status

from baseApp.models import Cadete, Donante, Institucion
from login.serializers import CadeteUserSerializer

# pylint: disable=no-member

class DonanteListCreateTestCase(APITestCase):
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


class InstitucionListCreateTestCase(APITestCase):
    """
    Pruebas realizadas sobre el listado y la creación de instancias de la
    clase Institucion.
    """
    def setUp(self):
        """
        Preparo algunas variables utilizadas en las pruebas de la clase.
        Inicio el cliente, creo el usuario Dar Vida (que será el que tenga el rol
        de Institucion) y genero la url .../institucion/.
        """
        self.client = APIClient()
        self.user = User.objects.create_user('darvida',
                                             'darvida@correo.com',
                                             'darvida',
                                             first_name='dar',
                                             last_name='vida')
        self.user.save()
        self.url = reverse('instituciones-list')

    def test_crear_institucion(self):
        """
        Valido que al realizar un POST con todos los datos de una Institución,
        se genere una instancia Institucion en la Base de Datos.
        """
        data = {
            'nombre': self.user.first_name,
            'director': 'Juan Carlos',
            'fecha_fundacion': date(1983,7,19),
            'domicilio': 'Calle falsa 789',
            'localidad': 'local',
            'provincia': 'prov',
            'pais': 'pais',
            'telefono': '1675-138745',
            'cant_empleados': 10,
            'descripcion': 'Esto es una descripcion',
            'cbu': 123456789012,
            'cuenta_bancaria': '123-456789/0',
            'usuario': self.user.id
        }
        response = self.client.post(self.url, data)
        cantidad = Institucion.objects.count()
        if cantidad > 0:
            institucion = Institucion.objects.get(id=response.data['id'])
        self.assertEqual(cantidad, 1)
        self.assertEqual(institucion.nombre, self.user.first_name)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_no_crear_institucion_con_todos_nulos(self):
        """
        Valido que al realizar un POST sin ningún dato, devuelva un mensaje
        HTTP_400 sin generar una instancia Institucion en la Base de Datos.
        """
        data = {
            'nombre': 'null',
            'director': 'null',
            'fecha_fundacion': 'null',
            'domicilio': 'null',
            'localidad': 'null',
            'provincia': 'null',
            'pais': 'null',
            'telefono': 'null',
            'cant_empleados': None,
            'descripcion': 'null',
            'cbu': 123456789012,
            'cuenta_bancaria': 'null',
            'usuario': 'null'
        }
        response = self.client.post(self.url, data, content_type="application/json")
        cantidad = Institucion.objects.count()
        self.assertEqual(cantidad, 0)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_no_crear_institucion_con_todos_blancos(self):
        """
        Valido que al realizar un POST con todos los datos blancos, devuelva
        un mensaje HTTP_400 sin generar una instancia Institucion en la Base de
        Datos.
        """
        data = {
            'nombre': '',
            'director': '',
            'fecha_fundacion': '',
            'domicilio': '',
            'localidad': '',
            'provincia': '',
            'pais': '',
            'telefono': '',
            'cant_empleados': '',
            'descripcion': '',
            'cbu': None,
            'cuenta_bancaria': '',
            'usuario': ''
        }
        response = self.client.post(self.url,data,content_type='application/json')
        cantidad = Institucion.objects.count()
        self.assertEqual(cantidad,0)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_crear_institucion_con_datos_minimos(self):
        """
        Valido que al realizar un POST con los datos mínimos necesarios para
        registrar un Insitucion, se genere una instancia Institucion en la Base de
        Datos.
        """

        #? Esto se debe definir según nuetro criterio
        data = {
            'nombre': self.user.first_name,
            'director': '',
            'fecha_fundacion': '',
            'domicilio': '',
            'localidad': '',
            'provincia': '',
            'pais': '',
            'telefono': '',
            'cant_empleados': '',
            'descripcion': '',
            'cbu': 123456789012,
            'cuenta_bancaria': '',
            'usuario': self.user.id
        }
        response = self.client.post(self.url,data)
        cantidad = Institucion.objects.count()
        if cantidad > 0:
            institucion = Institucion.objects.get(id=response.data['id'])
        self.assertEqual(cantidad,1)
        self.assertIsNone(response.data['fecha_fundacion'])
        self.assertEqual(institucion.nombre, self.user.first_name)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_listar_institucion(self):
        """
        Valido que al realizar un GET después de registrar una sola Institución en
        la Base de Datos, devuelva sólo los datos de la Institucion registrada.
        """
        institucion = Institucion.objects.create(
            nombre=self.user.first_name,
            director='Juan Carlos',
            fecha_fundacion=date(1983,7,19),
            domicilio='Calle falsa 789',
            localidad='local',
            provincia='prov',
            pais='pais',
            telefono='1675-138745',
            cant_empleados=10,
            descripcion='Esto es una descripcion',
            cbu=123456789012,
            cuenta_bancaria='123-456789/0',
            usuario=self.user
        )
        institucion.save()
        response = self.client.get(self.url)
        cantidad = len(response.data['results'])
        self.assertEqual(cantidad,1)
        institucion_response = response.data['results'][0]
        self.assertEqual(institucion.nombre,institucion_response['nombre'])
        self.assertEqual(institucion.director,institucion_response['director'])
        self.assertEqual(institucion.fecha_fundacion,
                    date.fromisoformat(institucion_response['fecha_fundacion']))
        self.assertEqual(institucion.domicilio,institucion_response['domicilio'])
        self.assertEqual(institucion.localidad,institucion_response['localidad'])
        self.assertEqual(institucion.provincia,institucion_response['provincia'])
        self.assertEqual(institucion.pais,institucion_response['pais'])
        self.assertEqual(institucion.telefono,institucion_response['telefono'])
        self.assertEqual(institucion.cant_empleados,
                    institucion_response['cant_empleados'])
        self.assertEqual(institucion.descripcion,institucion_response['descripcion'])
        self.assertEqual(institucion.cbu,institucion_response['cbu'])
        self.assertEqual(institucion.cuenta_bancaria,institucion_response['cuenta_bancaria'])
        self.assertEqual(institucion.usuario.id,institucion_response['usuario'])

    def test_listar_varias_instituciones(self):
        """
        Valido que al realizar un GET después de registrar dos Instituciones en la
        Base de Datos, devuelva los datos de las instituciones registradas.
        """
        institucion1 = Institucion.objects.create(
            nombre=self.user.first_name,
            director='Juan Carlos',
            fecha_fundacion=date(1983,7,19),
            domicilio='Calle falsa 789',
            localidad='local',
            provincia='prov',
            pais='pais',
            telefono='1675-138745',
            cant_empleados=10,
            descripcion='Esto es una descripcion',
            cbu=123456789012,
            cuenta_bancaria='123-456789/0',
            usuario=self.user
        )
        user2 = User.objects.create_user('paul',
                                         'paul@thebeatles.com',
                                         'paulpassword',
                                         first_name='paul',
                                         last_name='mccarny')
        institucion2 = Institucion.objects.create(
            nombre=user2.first_name,
            director='paul The Beatle',
            fecha_fundacion=date(1983,7,19),
            domicilio='Calle falsa 123',
            localidad='local',
            provincia='prov',
            pais='pais',
            telefono='',
            cant_empleados=5,
            descripcion='Esto es una descripcion',
            cbu=123456789012,
            cuenta_bancaria='',
            usuario=user2
        )
        response = self.client.get(self.url)
        cantidad = len(response.data['results'])
        self.assertEqual(cantidad,2)
        institucion1_response = response.data['results'][0]
        institucion2_response = response.data['results'][1]
        self.assertEqual(institucion1.nombre,institucion1_response['nombre'])
        self.assertEqual(institucion1.director,institucion1_response['director'])
        self.assertEqual(institucion2.nombre,institucion2_response['nombre'])
        self.assertEqual(institucion2.director,institucion2_response['director'])

    def test_lista_institucion_vacia(self):
        """
        Valido que al realizar un GET cuando no existen instituciones en la Base de
        Datos, no devuelva nada.
        """
        response = self.client.get(self.url)
        cantidad = len(response.data['results'])
        self.assertEqual(cantidad,0)


class CadeteListCreateTestCase(APITestCase):
    """
    Pruebas realizadas sobre el listado y la creación de instancias de la
    clase Cadete.
    """
    def setUp(self):
        """
        Preparo algunas variables utilizadas en las pruebas de la clase.
        Inicio el cliente, creo el usuario john (que será el que tenga el rol
        de Donante) y genero la url .../cadete/.
        """
        self.client = APIClient()
        self.user = User.objects.create_user('john',
                                             'lennon@thebeatles.com',
                                             'johnpassword',
                                             first_name='john',
                                             last_name='lennon')
        self.user.save()
        # Creo una institucion para asociarlo al cadete
        self.user2 = User.objects.create_user('paul',
                                         'paul@thebeatles.com',
                                         'paulpassword',
                                         first_name='paul',
                                         last_name='mccarny')
        self.institucion = Institucion.objects.create(
            nombre=self.user2.first_name,
            director='paul The Beatle',
            fecha_fundacion=date(1983,7,19),
            domicilio='Calle falsa 123',
            localidad='local',
            provincia='prov',
            pais='pais',
            telefono='',
            cant_empleados=5,
            descripcion='Esto es una descripcion',
            cbu=123456789012,
            cuenta_bancaria='',
            usuario=self.user2
        )
        self.url = reverse('cadetes-list')

    def test_crear_cadete(self):
        """
        Valido que al realizar un POST con todos los datos de un Cadete,
        se genere una instancia Cadete en la Base de Datos.
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
            'medio_transporte': 'triciclo a motor',
            'usuario': self.user.id,
            'institucion': self.institucion.id
        }
        response = self.client.post(self.url, data)
        cantidad = Cadete.objects.count()
        if cantidad > 0:
            cadete = Cadete.objects.get(id=response.data['id'])
        self.assertEqual(cantidad, 1)
        self.assertEqual(cadete.nombre, self.user.first_name)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_no_crear_cadete_con_todos_nulos(self):
        """
        Valido que al realizar un POST sin ningún dato, devuelva un mensaje
        HTTP_400 sin generar una instancia Cadete en la Base de Datos.
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
        data = {
            'nombre': 'null',
            'apellido': 'null',
            'fecha_nacimiento': 'null',
            'dni': 'null',
            'domicilio': 'null',
            'localidad': 'null',
            'provincia': 'null',
            'pais': 'null',
            'telefono': 'null',
            'estado_civil': 'null',
            'genero': 'null',
            'ocupacion': 'null',
            'medio_transporte': 'null',
            'usuario': 'null',
            'institucion': 'null'
        }
        response = self.client.post(self.url, data)
        cantidad = Cadete.objects.count()
        self.assertEqual(cantidad, 0)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_no_crear_cadete_con_todos_blancos(self):
        """
        Valido que al realizar un POST con todos los datos blancos, devuelva
        un mensaje HTTP_400 sin generar una instancia Cadete en la Base de
        Datos.
        """
        data = {
            'nombre': '',
            'apellido': '',
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
            'medio_transporte': '',
            'usuario': '',
            'institucion': ''
        }
        response = self.client.post(self.url,data)
        cantidad = Cadete.objects.count()
        self.assertEqual(cantidad,0)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_crear_cadete_con_datos_minimos(self):
        """
        Valido que al realizar un POST con los datos mínimos necesarios para
        registrar un Cadete, se genere una instancia Donante en la Base de
        Datos.
        """

        #? Esto se debe definir según nuetro criterio
        data = {
            'nombre': self.user.first_name,
            'apellido': self.user.last_name,
            'usuario': self.user.id,
            'institucion': self.institucion.id
        }
        response = self.client.post(self.url,data)
        cantidad = Cadete.objects.count()
        if cantidad > 0:
            cadete = Cadete.objects.get(id=response.data['id'])
        self.assertEqual(cantidad,1)
        self.assertIsNone(response.data['fecha_nacimiento'])
        self.assertEqual(cadete.nombre, self.user.first_name)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_listar_cadete(self):
        """
        Valido que al realizar un GET después de registrar un solo Cadete en
        la Base de Datos, devuelva sólo los datos del Cadete registrado.
        """
        cadete = Cadete.objects.create(
            nombre=self.user.first_name,
            apellido=self.user.last_name,
            fecha_nacimiento=date(1983,7,19),
            dni='87654321',
            domicilio='Calle falsa 789',
            localidad='local',
            provincia='prov',
            pais='pais',
            telefono='1675-138745',
            estado_civil='soltere',
            genero='masculine',
            ocupacion='reportero deportivo',
            medio_transporte='triciclo a motor',
            usuario=self.user,
            institucion=self.institucion
        )
        cadete.save()
        response = self.client.get(self.url)
        cantidad = len(response.data['results'])
        self.assertEqual(cantidad,1)
        cadete_response = response.data['results'][0]
        self.assertEqual(cadete.nombre,cadete_response['nombre'])
        self.assertEqual(cadete.apellido,cadete_response['apellido'])
        self.assertEqual(cadete.fecha_nacimiento,
                    date.fromisoformat(cadete_response['fecha_nacimiento']))
        self.assertEqual(cadete.dni,cadete_response['dni'])
        self.assertEqual(cadete.domicilio,cadete_response['domicilio'])
        self.assertEqual(cadete.localidad,cadete_response['localidad'])
        self.assertEqual(cadete.provincia,cadete_response['provincia'])
        self.assertEqual(cadete.pais,cadete_response['pais'])
        self.assertEqual(cadete.telefono,cadete_response['telefono'])
        self.assertEqual(cadete.estado_civil,
                    cadete_response['estado_civil'])
        self.assertEqual(cadete.genero,cadete_response['genero'])
        self.assertEqual(cadete.ocupacion,cadete_response['ocupacion'])
        self.assertEqual(cadete.medio_transporte,cadete_response['medio_transporte'])
        self.assertEqual(cadete.usuario.id,cadete_response['usuario'])
        self.assertEqual(cadete.institucion.id,cadete_response['institucion'])

    def test_listar_varios_cadetes(self):
        """
        Valido que al realizar un GET después de registrar dos Cadetes en la
        Base de Datos, devuelva los datos de los Cadetes registrados.
        """
        cadete1 = Cadete.objects.create(
            nombre=self.user.first_name,
            apellido=self.user.last_name,
            fecha_nacimiento=date(1983,7,19),
            dni='87654321',
            domicilio='Calle falsa 789',
            localidad='local',
            provincia='prov',
            pais='pais',
            telefono='1675-138745',
            estado_civil='soltere',
            genero='masculine',
            ocupacion='reportero deportivo',
            medio_transporte='triciclo a motor',
            usuario=self.user,
            institucion=self.institucion
        )
        user3 = User.objects.create_user('george',
                                         'george@thebeatles.com',
                                         'georgepassword',
                                         first_name='george',
                                         last_name='Harryson')
        cadete2 = Cadete.objects.create(
            nombre=self.user2.first_name,
            apellido=self.user2.last_name,
            fecha_nacimiento=date(1983,7,19),
            dni='87654321',
            domicilio='Calle falsa 789',
            localidad='local',
            provincia='prov',
            pais='pais',
            telefono='1675-138745',
            estado_civil='soltere',
            genero='masculine',
            ocupacion='reportero deportivo',
            medio_transporte='triciclo a motor',
            usuario=user3,
            institucion=self.institucion
        )
        response = self.client.get(self.url)
        cantidad = len(response.data['results'])
        self.assertEqual(cantidad,2)
        cadete1_response = response.data['results'][0]
        cadete2_response = response.data['results'][1]
        self.assertEqual(cadete1.nombre,cadete1_response['nombre'])
        self.assertEqual(cadete1.apellido,cadete1_response['apellido'])
        self.assertEqual(cadete2.nombre,cadete2_response['nombre'])
        self.assertEqual(cadete2.apellido,cadete2_response['apellido'])

    def test_lista_cadetes_vacia(self):
        """
        Valido que al realizar un GET cuando no existen donantes en la Base de
        Datos, no devuelva nada.
        """
        response = self.client.get(self.url)
        cantidad = len(response.data['results'])
        self.assertEqual(cantidad,0)
