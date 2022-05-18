# Create your tests here.
"""Pruebas de integración"""
from datetime import date, datetime

from django.urls import reverse
from django.contrib.auth.models import User
#from faker import Faker  #--Librería para generar datos fakes, pero no funciona bien
from rest_framework.test import APITestCase, APIClient
from rest_framework import status

from baseApp.models import Donante, Institucion
from DonacionesApp.models import DonacionBienes,Donacion

#fake = Faker()
class DonanacionBienesListCreateTestCase(APITestCase):
    """
    Pruebas realizadas sobre el listado y la creación de instancias de la
    clase DonacionBienes.
    """
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
        

    def test_crear_donacion_bienes(self):
        """
        Valido que al realizar un POST con todos los datos de una donacion,
        se genere una instancia Donacion de bienes en la Base de Datos.
        """
        data = {
            'donante': self.donante.id,
            'institucion': self.institucion.id,
            'cod_estado': 1,
            'fecha_creacion': datetime.now(),
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
        cantidad = DonacionBienes.objects.count()
        donante = Donante.objects.get(id=self.donante.id) #Aca me trae solo el nombre del donante y no el objeto
        #print(donante)   
        donacion = DonacionBienes.objects.get(donante=response.data['donante']) #Aca me trae todo el objeto
        #print(donacion.donante)
        self.assertEqual(cantidad, 1)
        self.assertEqual(donacion.donante, donante)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_no_crear_donacion_bienes_todos_nulos(self): #Funciona
        """
        Valido que al realizar un POST sin ningún dato, devuelva un mensaje
        HTTP_400 sin generar una instancia Donacion_bienes en la Base de Datos.
        """
        data = {
            "donante": 'null',
            "institucion": 'null',
            "cod_estado": 'null',
            "fecha_creacion": 'null',
            "fecha_retiro":'null',
            "fecha_creacion":'null',
            "fecha_cancelacion":'null',
            "fecha_aceptacion":'null',
            "motivo_cancelacion":'null',
            "fecha_entrega_real":'null',
            "bienes":'null'       
        }
        response = self.client.post(self.url, data, format='json')
        cantidad = DonacionBienes.objects.count()
        self.assertEqual(cantidad, 0)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_no_crear_donacion_bienes_todos_enblanco(self): #Funciona
        """
        Valido que al realizar un POST sin ningún dato, devuelva un mensaje
        HTTP_400 sin generar una instancia Donacion_bienes en la Base de Datos.
        """
        data = {
            "donante": '',
            "institucion": '',
            "cod_estado": '',
            "fecha_creacion": '',
            "fecha_retiro":'',
            "fecha_creacion":'',
            "fecha_cancelacion":'',
            "fecha_aceptacion":'',
            "motivo_cancelacion":'',
            "fecha_entrega_real":'',
            "bienes":''       
        }
        response = self.client.post(self.url, data, format='json')
        cantidad = DonacionBienes.objects.count()
        self.assertEqual(cantidad, 0)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_listar_instituciones(self):
        """
        Valido que al realizar un GET se obtengan todas las instituciones
        """
        #Creo usuario3 y la institución numero 2...
        self.url = reverse('instituciones_list')
        self.user3 = User.objects.create_user('Leonardo',
                                             'leo@dan.com',
                                             'leodan222',
                                             first_name='Leo',
                                             last_name='Dan')
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
        response = self.client.get(self.url)
        print(response.data)
        cantidad = len(response.data['results'])
        self.assertEqual(cantidad,2)