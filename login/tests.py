"""docstring"""
from django.urls import reverse
from django.contrib.auth.models import User

from rest_framework.test import APITestCase, APIClient
from rest_framework import status

class LogupUsuarioTestCase(APITestCase):
    """Pruebas que validan la creación de un usuario"""

    def setUp(self):
        """
        Preparo algunas variables utilizadas en las pruebas de la clase.
        Inicio el cliente y genero la url .../logup/.
        """
        self.client = APIClient()
        self.url = reverse('logup')

    def test_crear_usuario(self):
        """
        Valido que al realizar un POST con todos los datos de un Usuario,
        se genere una instancia Usuario en la Base de Datos.
        """
        data = {
            'username': 'juanp',
            'first_name': 'juan',
            'last_name': 'perez',
            'email': 'juanperez@gmail.com',
            'password': 'secretPassword',
            'groups': 1
        }
        response = self.client.post(self.url, data)
        cantidad = User.objects.count()
        if cantidad > 0:
            usuario = User.objects.get(id=response.data['results'][0]['id'])
        self.assertEqual(cantidad, 1)
        self.assertEqual(usuario.username, data['username'])
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
