"""docstring"""
from django.urls import reverse
from django.contrib.auth.models import User, Group

from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from rest_framework.authtoken.models import Token

# pylint: disable=no-member

class LogupUsuarioTestCase(APITestCase):
    """Pruebas que validan la creación de un usuario"""

    def setUp(self):
        """
        Preparo algunas variables utilizadas en las pruebas de la clase.
        Inicio el cliente y genero la url .../logup/.
        """
        self.group_donante = Group.objects.create(name='donantes')
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
            'groups': [self.group_donante.id]
        }
        response = self.client.post(self.url, data)
        cantidad = User.objects.count()
        if cantidad > 0:
            usuario = User.objects.first()
        self.assertEqual(cantidad, 1)
        self.assertEqual(usuario.username, data['username'])
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    #? COLOCAR AQUÍ LAS DEMÁS PRUEBAS RELACIONADAS AL ALTA DE UN USUARIO,
    #? UN DONANTE Y UNA INSTITUCIÓN


class LoginUsuarioTestCase(APITestCase):
    """Pruebas que validan el login de un usuario"""
    def setUp(self):
        self.username = 'john'
        self.password = 'johnpassword'
        self.usuario = User.objects.create_user(self.username,
                                                'lennon@thebeatles.com',
                                                self.password,
                                                first_name='john',
                                                last_name='lennon')
        self.client = APIClient()
        self.url = reverse('login')

    def test_login_usuario(self):
        """Valido login de un usuario"""
        data = {
            'username': self.username,
            'password': self.password
        }
        response = self.client.post(self.url, data)
        #! EN LO SIGUIENTE, SE DEBE DEVOLVER EN EL RESPONSE LA INSTANCIA
        #! USUARIO (NO LOS DATOS)
        usuario = User.objects.get(username=response.data['user']['username'])
        self.assertTrue(usuario.is_authenticated)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_login_usuario_inexistente(self):
        """valido falla de login de un usuario que no existe"""
        data = {
            'username':'anonimo1',
            'password':'passwordAnonimo'
        }
        response = self.client.post(self.url,data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_login_contrasena_incorrecta(self):
        """Valido falla de login al ingresar mal la contraseña"""
        data = {
            'username':self.username,
            'password':self.password+'incorrecto'
        }
        response = self.client.post(self.url,data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_login_usuario_inactivo(self):
        """Valido falla de login de un usuario inactivo"""
        self.usuario.is_active = False
        self.usuario.save()
        data = {
            'username':self.username,
            'password':self.password
        }
        response = self.client.post(self.url,data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class LoguotUsuarioTestCase(APITestCase):
    """Pruebas que validan la salida (logout) del usuario"""
    def setUp(self):
        self.username = 'john'
        self.password = 'johnpassword'
        self.usuario = User.objects.create_user(self.username,
                                                'lennon@thebeatles.com',
                                                self.password,
                                                first_name='john',
                                                last_name='lennon')
        self.client = APIClient()
        self.url = reverse('logout')

    def test_logout_usuario(self):
        """Valida la salida del usuario"""
        login_user = self.client.login(username=self.username,
                                       password=self.password)
        self.assertTrue(login_user)
        if login_user is not None:
            token, created = Token.objects.get_or_create(user = self.usuario)
            self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
            data = {'token':token.key}
            response = self.client.post(self.url,data)
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(Token.objects.filter(user=self.usuario).count(),0)
