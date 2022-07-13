from datetime import datetime, date, time
from django.urls import reverse
from django.contrib.auth.models import User

from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from DonacionesApp.models import Bien, DonacionBienes
from Recoleccion.models import Recoleccion

from baseApp.models import Cadete, Institucion, Donante

# pylint: disable=no-member

class RecoleccionListTestCase(APITestCase):
    """
    Pruebas realizadas sobre el listado de Recolecciones previamente creadas
    """
    def setUp(self):
        """
        Preparo algunas variables utilizadas en las pruebas de la clase.
        Inicio el cliente, creo el usuario john (que será el que tenga el rol
        de Donante) y genero la url .../donantes/.
        """
        self.client = APIClient()
        self.user_donante = User.objects.create_user(
            'csolano',
            'csolano@gmail.com',
            'password',
            first_name='Cintia',
            last_name='Solano'
        )
        self.user_institucion = User.objects.create_user(
            'unainstitucion',
            'institucion@gmail.com',
            'password',
            first_name='Steve',
            last_name='Caprinne'
        )
        self.user_cadete = User.objects.create_user(
            'rporian',
            'rporian@gmail.com',
            'password',
            first_name='Ricardo',
            last_name='Porian'
        )
        self.donante = Donante.objects.create(
            nombre='Cintia',
            apellido='Solano',
            usuario=self.user_donante
        )
        self.institucion1 = Institucion.objects.create(
            nombre='UnaInstitucion',
            director='Steve Caprinne',
            usuario=self.user_institucion
        )
        self.cadete = Cadete.objects.create(
            nombre='Ricardo',
            apellido='Porian',
            institucion=self.institucion1
        )
        self.donacion1 = DonacionBienes.objects.create(
            donante=self.donante,
            institucion=self.institucion1,
            fecha_creacion=datetime.now(),
            cod_estado=1
        )
        self.bien1 = Bien.objects.create(
            tipo=2,
            nombre='objeto',
            descripcion='Esto es una descripcion',
            cantidad=2,
            donacion=self.donacion1
        )
        self.url = reverse('lista_recoleccion')

    def test_listado_sin_recolecciones(self):
        """
        Valido que cuando no exista ninguna recolección creada al realizar un
        GET, devuelva la lista vacía
        """
        response = self.client.get(self.url)
        cantidad = Recoleccion.objects.count()
        self.assertEqual(cantidad, 0)
        self.assertEqual(response.data['count'],0)
        self.assertEqual(len(response.data['results']),0)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_listado_una_recoleccion(self):
        """
        Valido que cuando exista una recolección al realizar un GET, devuelva
        la lista con dicha recolección
        """
        recoleccion = Recoleccion.objects.create(
            cadete=self.cadete,
            estado_recoleccion=1,
            hora_recoleccion=datetime.now().time(),
            fecha_recoleccion=date(2022,11,20)
        )
        recoleccion.save()
        self.donacion1.recoleccion = recoleccion
        self.donacion1.save()
        response = self.client.get(self.url)

        self.assertEqual(Recoleccion.objects.count(),1)
        self.assertEqual(response.data['count'],1)
        self.assertEqual(len(response.data['results']),1)
        #self.assertEqual(response.data['results'][0],recoleccion)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_listado_varias_recolecciones(self):
        recoleccion1 = Recoleccion.objects.create(
            cadete=self.cadete,
            estado_recoleccion=1,
            hora_recoleccion=datetime.now().time(),
            fecha_recoleccion=date(2022,11,20)
        )
        self.donacion1.recoleccion = recoleccion1
        self.donacion1.save()

        recoleccion2 = Recoleccion.objects.create(
            cadete=self.cadete,
            estado_recoleccion=1,
            hora_recoleccion=datetime.now().time(),
            fecha_recoleccion=date(2022,11,20)
        )
        donacion2 = DonacionBienes.objects.create(
            donante=self.donante,
            institucion=self.institucion1,
            fecha_creacion=datetime.now(),
            cod_estado=1,
            recoleccion=recoleccion2
        )
        bien2 = Bien.objects.create(
            tipo=2,
            nombre='otroobjecto',
            descripcion='Esto es otra descripcion',
            cantidad=2,
            donacion=donacion2
        )

        recoleccion2.save()
        donacion2.recoleccion = recoleccion2
        donacion2.save()
        response = self.client.get(self.url)
        self.assertEqual(Recoleccion.objects.count(),2)
        self.assertEqual(response.data['count'],2)
        self.assertEqual(len(response.data['results']),2)
        #self.assertEqual(response.data['results'][0],recoleccion1)
        #self.assertEqual(response.data['results'][1],recoleccion2)
        self.assertEqual(response.status_code, status.HTTP_200_OK)