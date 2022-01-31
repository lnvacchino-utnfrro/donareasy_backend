from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
from login.models import Donante
from login.serializers import DonanteSerializer

class DonantesLoginTests(APITestCase):

    def test_crear_donante(self):
        """
        Crear un donante y verificar que exista
        """
        url = reverse('donantes-list')
        #serializer = DonanteSerializer(nombre='juansito', apellido='janterini', email='kxx@xxx.com', edad=12)
        serializer = DonanteSerializer({'nombre':'juansito', 'apellido':'janterini', 'email':'kxx@xxx.com', 'edad':12})
        response = self.client.post(url, serializer.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Donante.objects.count(), 1)
