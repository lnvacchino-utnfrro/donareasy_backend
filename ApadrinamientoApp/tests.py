from ApadrinamientoApp.models import Chicos
from ApadrinamientoApp.models import SolicitudApadrinamiento
# Create your tests here.
"""Pruebas de integración"""
from datetime import date, datetime
#from queue import Empty

from django.urls import reverse
from django.contrib.auth.models import User
#from faker import Faker  #--Librería para generar datos fakes, pero no funciona bien
from rest_framework.test import APITestCase, APIClient
from rest_framework import status

from baseApp.models import Donante, Institucion


class AltaChicoTestCase(APITestCase):
    """
    Pruebas realizadas sobre la creación y alta de un nuevo chico en una institución
    """
    def setUp(self):
        """
        Preparo algunas variables utilizadas en las pruebas de la clase.
        Inicio el cliente, creo el usuario institución
        """
        self.client = APIClient()
        self.user1 = User.objects.create_user('insti',
                                             'tuto@gmail.com',
                                             'instituto',
                                             first_name='insti',
                                             last_name='tuto')
        self.user1.save()
        self.user2 = User.objects.create_user('tutito',
                                             'mail@gmail.com',
                                             'tito',
                                             first_name='tito',
                                             last_name='aaa')
        self.user2.save()
        self.institucion = Institucion.objects.create(nombre= self.user1.first_name,
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
                                                        usuario= self.user1)
        self.institucion.save()
        self.institucion2 = Institucion.objects.create(nombre= self.user2.first_name,
                                                        director= "tito",
                                                        fecha_fundacion= date(1990,1,1),
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
        self.institucion2.save()
        self.url = reverse('alta_chico')
    
    def test_agregar_nuevo_chico(self):

        """Agrego un nuevo chico a la institución"""
        data =  {'nombre': 'Roman',
            'apellido': 'Riquelme',
            'edad': 1,
            'descripcion': 'menor',
            'institucion': self.institucion.id,
            'fotografia': ''
            }
        
        response = self.client.post(self.url, data)
        cantidad = Chicos.objects.count()
        if cantidad > 0:
            chico = Chicos.objects.get(id=response.data['id'])
        self.assertEqual(cantidad, 1)
        self.assertEqual(chico.nombre, response.data['nombre'])
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
    def test_agregar_nuevo_chico_mayor_edad(self):

        """Agrego un nuevo chico a la institución"""
        data =  {'nombre': 'Patricia',
            'apellido': 'Riquelme',
            'edad': 18,
            'descripcion': 'Mayor de edad',
            'institucion': self.institucion2.id,
            'fotografia': ''
            }
        
        response = self.client.post(self.url, data)
        cantidad = Chicos.objects.count()
        # if cantidad > 0:
        #     chico = Chicos.objects.get(id=response.data['id'])
        self.assertEqual(cantidad, 0)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_agregar_nuevo_chico_edad_negativa(self):

        """Agrego un nuevo chico a la institución"""
        data =  {'nombre': 'Patricia',
            'apellido': 'Riquelme',
            'edad': -10,
            'descripcion': 'edad invalida',
            'institucion': self.institucion2.id,
            'fotografia': ''
            }
        
        response = self.client.post(self.url, data)
        cantidad = Chicos.objects.count()
        # if cantidad > 0:
        #     chico = Chicos.objects.get(id=response.data['id'])
        self.assertEqual(cantidad, 0)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_agregar_nuevo_chico_sin_institucion(self):

        """Agrego un nuevo chico a la institución"""
        data =  {'nombre': 'Patricia',
            'apellido': 'Riquelme',
            'edad': 12,
            'descripcion': 'edad invalida',
            'institucion': '',
            'fotografia': ''
            }
        
        response = self.client.post(self.url, data)
        cantidad = Chicos.objects.count()
        # if cantidad > 0:
        #     chico = Chicos.objects.get(id=response.data['id'])
        self.assertEqual(cantidad, 0)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

class AltaSolicitudApadrinamientoTestCase(APITestCase):
    """
    Pruebas realizadas sobre la creación de una solicitud de apadrinamiento
    """
    def setUp(self):
        """
        Preparo algunas variables utilizadas en las pruebas de la clase.
        Inicio el cliente...
        """
        self.client = APIClient()
        self.user1 = User.objects.create_user('donan',
                                             'ante@don.com',
                                             'donante',
                                             first_name='don',
                                             last_name='ante')
        self.user1.save()
        self.user2 = User.objects.create_user('tutito',
                                             'mail@gmail.com',
                                             'tito',
                                             first_name='tito',
                                             last_name='aaa')
        self.user2.save()
        self.institucion = Institucion.objects.create(nombre= self.user2.first_name,
                                                        director= "tito",
                                                        fecha_fundacion= date(1990,1,1),
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
        self.institucion.save()
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
                                            ocupacion='reportero',
                                            usuario= self.user1)
        self.donante.save()
        self.chico = Chicos.objects.create(
                                        nombre = "nene",
                                        apellido = "malo",
                                        edad = 15,
                                        descripcion = "aaaaa",
                                        institucion = self.institucion,
                                        fotografia = '',
        )
        self.chico.save()
        self.url = reverse('alta_solicitud')

    def test_crear_solicitud_apadrinamiento(self):
        """
        Valido que al realizar un POST de una solicitud se genere
        una instancia de solicitud_apadrinamiento en la BD
        """
        data = {
            'motivo_FS': '',
            'dni_frente': None,
            'dni_dorso': None,
            'recibo_sueldo': None,
            'acta_matrimonio': None,
            'visita': True,
            'fecha_visita': datetime.now(),
            'chico_apadrinado': self.chico.id
        }

        response = self.client.post(self.url, data, format='json')
        cant = SolicitudApadrinamiento.objects.count()
        chico = Chicos.objects.get(id=self.chico.id)
        self.assertEqual(chico.nombre,'nene')
        self.assertEqual(cant, 1)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_crear_solicitud_apadrinamiento_sin_chico_seleccionado(self):
        """
        Valido que al realizar un POST de una solicitud sin ningun chico seleccionado 
        NO se genere una instancia de solicitud_apadrinamiento en la BD
        """
        data = {
            'motivo_FS': '',
            'dni_frente': None,
            'dni_dorso': None,
            'recibo_sueldo': None,
            'acta_matrimonio': None,
            'visita': True,
            'fecha_visita': datetime.now(),
            'chico_apadrinado': ''
        }

        response = self.client.post(self.url, data, format='json')
        cant = SolicitudApadrinamiento.objects.count()
        self.assertEqual(cant, 0)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_solicitud_apadrinamiento_duplicada(self):
        """
        Valido que al realizar un POST de una solicitud se genere
        una instancia de solicitud_apadrinamiento en la BD y al generar un segundo POST de
        una solicitud de apadrinamiento para el mismo chico no se registre ninguna instancia
        y falle la solicitud.
        """
        data = {
            'motivo_FS': '',
            'dni_frente': None,
            'dni_dorso': None,
            'recibo_sueldo': None,
            'acta_matrimonio': None,
            'visita': True,
            'fecha_visita': datetime.now(),
            'chico_apadrinado': self.chico.id
        }

        data2 = {
            'motivo_FS': '',
            'dni_frente': None,
            'dni_dorso': None,
            'recibo_sueldo': None,
            'acta_matrimonio': None,
            'visita': True,
            'fecha_visita': datetime.now(),
            'chico_apadrinado': self.chico.id
        }

        response = self.client.post(self.url, data, format='json')
        response2 = self.client.post(self.url, data2, format='json')
        cant = SolicitudApadrinamiento.objects.count()
        self.assertEqual(cant, 1)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response2.status_code, status.HTTP_400_BAD_REQUEST)

class LstaSolicitudesApadrinamientoTestCase(APITestCase):
    """
    Pruebas realizadas sobre la creación de una solicitud de apadrinamiento
    """
    def setUp(self):
        """
        Preparo algunas variables utilizadas en las pruebas de la clase.
        Inicio el cliente. Creo un usuario institución, 3 chicos para esa institución
        y 3 solicitudes de apadrinamiento en donde 2 están con estado "creada" y una "cancelada"
        """
        self.client = APIClient()
        self.user2 = User.objects.create_user('tutito',
                                             'mail@gmail.com',
                                             'tito',
                                             first_name='tito',
                                             last_name='aaa')
        self.user2.save()
        self.institucion = Institucion.objects.create(nombre= self.user2.first_name,
                                                        director= "tito",
                                                        fecha_fundacion= date(1990,1,1),
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
        self.institucion.save()
        self.chico = Chicos.objects.create(
                                        nombre = "nene",
                                        apellido = "malo",
                                        edad = 15,
                                        descripcion = "aaaaa",
                                        institucion = self.institucion,
                                        fotografia = '',
        )
        self.chico.save()
        self.chico2 = Chicos.objects.create(
                                        nombre = "ooo",
                                        apellido = "aaa",
                                        edad = 5,
                                        descripcion = "aaaaa",
                                        institucion = self.institucion,
                                        fotografia = '',
        )
        self.chico2.save()
        self.chico3 = Chicos.objects.create(
                                        nombre = "trew",
                                        apellido = "abc",
                                        edad = 3,
                                        descripcion = "aaaaa",
                                        institucion = self.institucion,
                                        fotografia = '',
        )
        self.chico3.save()
        self.soli1 = SolicitudApadrinamiento.objects.create(
                                        cod_estado = 1,
                                        motivo_FS = '',
                                        fecha_creacion = datetime.now(),
                                        fecha_aceptacion = None,
                                        fecha_cancelacion = None,
                                        motivo_cancelacion = None,
                                        dni_frente = '',
                                        dni_dorso = '',
                                        recibo_sueldo = '',
                                        acta_matrimonio = '',
                                        visita = True,
                                        fecha_visita = datetime.now(),
                                        chico_apadrinado = self.chico
        )
        self.soli1.save()
        self.soli2 = SolicitudApadrinamiento.objects.create(
                                        cod_estado = 1,
                                        motivo_FS = '',
                                        fecha_creacion = datetime.now(),
                                        fecha_aceptacion = None,
                                        fecha_cancelacion = None,
                                        motivo_cancelacion = None,
                                        dni_frente = '',
                                        dni_dorso = '',
                                        recibo_sueldo = '',
                                        acta_matrimonio = '',
                                        visita = False,
                                        fecha_visita = None,
                                        chico_apadrinado = self.chico2
        )
        self.soli2.save()
        self.soli3 = SolicitudApadrinamiento.objects.create(
                                        cod_estado = 0,
                                        motivo_FS = '',
                                        fecha_creacion = datetime.now(),
                                        fecha_aceptacion = None,
                                        fecha_cancelacion = datetime.now(),
                                        motivo_cancelacion = 'no se puede',
                                        dni_frente = '',
                                        dni_dorso = '',
                                        recibo_sueldo = '',
                                        acta_matrimonio = '',
                                        visita = False,
                                        fecha_visita = None,
                                        chico_apadrinado = self.chico3
        )
        self.soli3.save()
        self.url = reverse('revisa_solicitudes')

    def test_listar_solicitudes_apadrinamiento(self):
        """
        Valido que al realizar un GET me traiga todas las solicitudes con estado "Creada" (1)
        """
        response = self.client.get(self.url)
        cantidad = len(response.data['results'])
        solicitud_response = response.data['results'][1] 
        #Toma la posición 1 ya que a medida que se agrega un objeto nuevo se coloca en posición 0, metodo pila (el primero se coloca encima)
        solicitud2_response = response.data['results'][0]
        self.assertEqual(cantidad,2)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.soli2.id,solicitud_response['id']) #valido nombre institucion1
        self.assertEqual(self.soli1.id,solicitud2_response['id'])

class EligeSolicitudApadrinamientoTestCase(APITestCase):
    """
    Pruebas realizadas para elegir una solicitud del listado
    """
    def setUp(self):
        """
        Preparo algunas variables utilizadas en las pruebas de la clase.
        Inicio el cliente. Creo un usuario institución, 4 chicos para esa institución
        y 4 solicitudes de apadrinamiento en donde 2 están con estado "creada", una "cancelada" y una "aceptada"
        """
        self.client = APIClient()
        self.user2 = User.objects.create_user('tutito',
                                             'mail@gmail.com',
                                             'tito',
                                             first_name='tito',
                                             last_name='aaa')
        self.user2.save()
        self.institucion = Institucion.objects.create(nombre= self.user2.first_name,
                                                        director= "tito",
                                                        fecha_fundacion= date(1990,1,1),
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
        self.institucion.save()
        self.chico = Chicos.objects.create(
                                        nombre = "nene",
                                        apellido = "malo",
                                        edad = 15,
                                        descripcion = "aaaaa",
                                        institucion = self.institucion,
                                        fotografia = '',
        )
        self.chico.save()
        self.chico2 = Chicos.objects.create(
                                        nombre = "ooo",
                                        apellido = "aaa",
                                        edad = 5,
                                        descripcion = "aaaaa",
                                        institucion = self.institucion,
                                        fotografia = '',
        )
        self.chico2.save()
        self.chico3 = Chicos.objects.create(
                                        nombre = "trew",
                                        apellido = "abc",
                                        edad = 3,
                                        descripcion = "aaaaa",
                                        institucion = self.institucion,
                                        fotografia = '',
        )
        self.chico3.save()
        self.chico4 = Chicos.objects.create(
                                        nombre = "po",
                                        apellido = "poc",
                                        edad = 10,
                                        descripcion = "8000",
                                        institucion = self.institucion,
                                        fotografia = '',
        )
        self.chico4.save()
        self.soli1 = SolicitudApadrinamiento.objects.create(
                                        cod_estado = 1,
                                        motivo_FS = '',
                                        fecha_creacion = datetime.now(),
                                        fecha_aceptacion = None,
                                        fecha_cancelacion = None,
                                        motivo_cancelacion = None,
                                        dni_frente = '',
                                        dni_dorso = '',
                                        recibo_sueldo = '',
                                        acta_matrimonio = '',
                                        visita = True,
                                        fecha_visita = datetime.now(),
                                        chico_apadrinado = self.chico
        )
        self.soli1.save()
        self.soli2 = SolicitudApadrinamiento.objects.create(
                                        cod_estado = 1,
                                        motivo_FS = '',
                                        fecha_creacion = datetime.now(),
                                        fecha_aceptacion = None,
                                        fecha_cancelacion = None,
                                        motivo_cancelacion = None,
                                        dni_frente = '',
                                        dni_dorso = '',
                                        recibo_sueldo = '',
                                        acta_matrimonio = '',
                                        visita = False,
                                        fecha_visita = None,
                                        chico_apadrinado = self.chico2
        )
        self.soli2.save()
        self.soli3 = SolicitudApadrinamiento.objects.create(
                                        cod_estado = 0,
                                        motivo_FS = '',
                                        fecha_creacion = datetime.now(),
                                        fecha_aceptacion = None,
                                        fecha_cancelacion = datetime.now(),
                                        motivo_cancelacion = 'no se puede',
                                        dni_frente = '',
                                        dni_dorso = '',
                                        recibo_sueldo = '',
                                        acta_matrimonio = '',
                                        visita = False,
                                        fecha_visita = None,
                                        chico_apadrinado = self.chico3
        )
        self.soli3.save()
        self.soli4 = SolicitudApadrinamiento.objects.create(
                                        cod_estado = 2,
                                        motivo_FS = '',
                                        fecha_creacion = datetime.now(),
                                        fecha_aceptacion = datetime.now(),
                                        fecha_cancelacion = None,
                                        motivo_cancelacion = None,
                                        dni_frente = '',
                                        dni_dorso = '',
                                        recibo_sueldo = '',
                                        acta_matrimonio = '',
                                        visita = False,
                                        fecha_visita = None,
                                        chico_apadrinado = self.chico4
        )
        self.soli4.save()
        self.url = reverse('elige_solicitud',args=[self.soli1.id]) #Test 1 solicitud creada
        self.url2 = reverse('elige_solicitud',args=[self.soli3.id]) #Test 2 solicitud cancelada
        self.url3 = reverse('elige_solicitud',args=[self.soli4.id]) #Test 3 solicitud aceptada

    def test_elegir_solicitud_apadrinamiento(self):
        """
        Valido que al realizar un GET de una solicitud traiga esa misma
        """
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['chico_apadrinado']['id'],self.chico.id)
        self.assertEqual(response.data['id'],self.soli1.id)

    def test_no_mostrar_solicitud_apadrinamiento_cancelada(self):
        """
        Valido que al realizar un GET de una solicitud cancelada no la encuentre
        """
        
        response = self.client.get(self.url2)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_no_mostrar_solicitud_apadrinamiento_aceptada(self):
        """
        Valido que al realizar un GET de una solicitud aceptada no la encuentre
        """
        
        response = self.client.get(self.url3)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

#Actualizar aceptar o rechazar solicitud
class ActualizaSolicitudApadrinamientoTestCase(APITestCase):
    """
    Pruebas realizadas para actualizar el estado de una solicitud de apadrinamiento
    """
    def setUp(self):
        """
        Preparo algunas variables utilizadas en las pruebas de la clase.
        Inicio el cliente. Creo un usuario institución, 4 chicos para esa institución
        y 4 solicitudes de apadrinamiento en donde 2 están con estado "creada", una "cancelada" y una "aceptada"
        """
        self.client = APIClient()
        self.user2 = User.objects.create_user('tutito',
                                             'mail@gmail.com',
                                             'tito',
                                             first_name='tito',
                                             last_name='aaa')
        self.user2.save()
        self.institucion = Institucion.objects.create(nombre= self.user2.first_name,
                                                        director= "tito",
                                                        fecha_fundacion= date(1990,1,1),
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
        self.institucion.save()
        self.chico = Chicos.objects.create(
                                        nombre = "nene",
                                        apellido = "malo",
                                        edad = 15,
                                        descripcion = "aaaaa",
                                        institucion = self.institucion,
                                        fotografia = '',
        )
        self.chico.save()
        self.chico2 = Chicos.objects.create(
                                        nombre = "ooo",
                                        apellido = "aaa",
                                        edad = 5,
                                        descripcion = "aaaaa",
                                        institucion = self.institucion,
                                        fotografia = '',
        )
        self.chico2.save()
        self.chico3 = Chicos.objects.create(
                                        nombre = "trew",
                                        apellido = "abc",
                                        edad = 3,
                                        descripcion = "aaaaa",
                                        institucion = self.institucion,
                                        fotografia = '',
        )
        self.chico3.save()
        self.chico4 = Chicos.objects.create(
                                        nombre = "po",
                                        apellido = "poc",
                                        edad = 10,
                                        descripcion = "8000",
                                        institucion = self.institucion,
                                        fotografia = '',
        )
        self.chico4.save()
        self.soli1 = SolicitudApadrinamiento.objects.create(
                                        cod_estado = 1,
                                        motivo_FS = '',
                                        fecha_creacion = datetime.now(),
                                        fecha_aceptacion = None,
                                        fecha_cancelacion = None,
                                        motivo_cancelacion = None,
                                        dni_frente = '',
                                        dni_dorso = '',
                                        recibo_sueldo = '',
                                        acta_matrimonio = '',
                                        visita = True,
                                        fecha_visita = datetime.now(),
                                        chico_apadrinado = self.chico
        )
        self.soli1.save()
        self.soli2 = SolicitudApadrinamiento.objects.create(
                                        cod_estado = 1,
                                        motivo_FS = '',
                                        fecha_creacion = datetime.now(),
                                        fecha_aceptacion = None,
                                        fecha_cancelacion = None,
                                        motivo_cancelacion = None,
                                        dni_frente = '',
                                        dni_dorso = '',
                                        recibo_sueldo = '',
                                        acta_matrimonio = '',
                                        visita = False,
                                        fecha_visita = None,
                                        chico_apadrinado = self.chico2
        )
        self.soli2.save()
        self.soli3 = SolicitudApadrinamiento.objects.create(
                                        cod_estado = 0,
                                        motivo_FS = '',
                                        fecha_creacion = datetime.now(),
                                        fecha_aceptacion = None,
                                        fecha_cancelacion = datetime.now(),
                                        motivo_cancelacion = 'no se puede',
                                        dni_frente = '',
                                        dni_dorso = '',
                                        recibo_sueldo = '',
                                        acta_matrimonio = '',
                                        visita = False,
                                        fecha_visita = None,
                                        chico_apadrinado = self.chico3
        )
        self.soli3.save()
        self.soli4 = SolicitudApadrinamiento.objects.create(
                                        cod_estado = 2,
                                        motivo_FS = '',
                                        fecha_creacion = datetime.now(),
                                        fecha_aceptacion = datetime.now(),
                                        fecha_cancelacion = None,
                                        motivo_cancelacion = None,
                                        dni_frente = '',
                                        dni_dorso = '',
                                        recibo_sueldo = '',
                                        acta_matrimonio = '',
                                        visita = False,
                                        fecha_visita = None,
                                        chico_apadrinado = self.chico4
        )
        self.soli4.save()
        self.url = reverse('acepta_solicitud',args=[self.soli1.id]) #Test 1 solicitud creada
        self.url2 = reverse('acepta_solicitud',args=[self.soli3.id]) #Test 2 solicitud cancelada
        self.url3 = reverse('acepta_solicitud',args=[self.soli4.id]) #Test 3 solicitud aceptada

    def test_aceptar_rechazar_solicitud_apadrinamiento(self):
        """
        Valido que al realizar un GET de una solicitud traiga esa misma
        """
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
        response = self.client.put(self.url,data) #Acepta donacion
        response2 = self.client.put(self.url,data2) #Cancela donacion
        """Valido que el response sea correcto tanto para la aceptacion como para la cancelacion"""
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response2.status_code, status.HTTP_200_OK)

    def test_actualizar_solicitud_apadrinamiento_cancelada(self):
        """
        Valido que al realizar un GET de una solicitud traiga esa misma
        """
        data = {
            "cod_estado": 2,
            #"motivo_cancelacion": None,
            "fecha_aceptacion": datetime.now()
            #"fecha_cancelacion": None
        }
        response = self.client.put(self.url2,data) #Acepta donacion
        #response2 = self.client.put(self.url,data2) #Cancela donacion
        """Valido que el response sea correcto tanto para la aceptacion como para la cancelacion"""
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertNotEqual(response.data['cod_estado'],self.soli3.cod_estado)
        #self.assertEqual(response2.status_code, status.HTTP_200_OK)