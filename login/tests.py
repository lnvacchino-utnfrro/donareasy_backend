from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
from login.models import Donante
from serializers import DonanteSerializer

class DonantesLoginTests(APITestCase):

    def test_crear_donante(self):
        """
        Crear un donante y verificar que exista
        """
        url = reverse('donantes-list')
        data = {
            'nombre': 'juansito', 
            'apellido':'janterini', 
            'email':'juan.jan@gmail.com',
            'edad':11
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Donante.objects.count(), 1)
