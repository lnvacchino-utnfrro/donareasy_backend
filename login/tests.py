"""docstring"""
from datetime import date, datetime, timedelta

from django.core import mail
from django.urls import reverse
from django.contrib.auth.models import User, Group
from django.contrib.sessions.models import Session

from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from rest_framework.authtoken.models import Token

from login.models import CodigoRecuperacion

from baseApp.models import Cadete, Donante, Institucion

# pylint: disable=no-member

class LogupUsuarioTestCase(APITestCase):
    """Pruebas que validan la creación de un usuario"""

    def setUp(self):
        """
        Preparo algunas variables utilizadas en las pruebas de la clase.
        Inicio el cliente y genero la url .../logup/.
        """
        self.group_donante = Group.objects.create(name='donantes')
        self.group_institucion = Group.objects.create(name='instituciones')
        self.group_cadete = Group.objects.create(name='cadetes')
        self.client = APIClient()
        # self.url = reverse('logup')
        self.url_donante = reverse('donante-create')
        self.url_institucion = reverse('institucion-create')
        self.url_cadete = reverse('cadete-create')

    def test_crear_usuario_donante(self):
        """
        Valido que al realizar un POST con todos los datos de un Usuario con el
        rol de donante, se genere una instancia Usuario y una instancia Donante
        en la Base de Datos.
        """
        usuario = {
            'username': 'juanp',
            'first_name': 'juan',
            'last_name': 'perez',
            'email': 'juanperez@gmail.com',
            'password': 'secretPassword'
        }
        data = {
            "usuario": usuario,
            "nombre": "Alejandro",
            "apellido": "Barrientos",
            "fecha_nacimiento": date(1983,7,19),
            "dni": "12345678",
            "domicilio": "Calle falsa 123",
            "localidad": "Loc",
            "provincia": "prov",
            "pais": "Arg",
            "telefono": "0123-123456789",
            "estado_civil": "Estado",
            "genero": "Genero",
            "ocupacion": "Ocupación"
        }
        response = self.client.post(self.url_donante, data, format='json')
        # Evaluo el usuario
        cantidad = User.objects.count()
        if cantidad > 0:
            usuario_db = User.objects.first()
        self.assertEqual(cantidad, 1)
        self.assertEqual(usuario_db.username, usuario['username'])
        # Evaluo el donante
        cantidad = Donante.objects.count()
        if cantidad > 0:
            donante = Donante.objects.first()
        self.assertEqual(cantidad, 1)
        self.assertEqual(donante.usuario, usuario_db)
        # Evaluo el estado del response
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_crear_usuario_institucion(self):
        """
        Valido que al realizar un POST con todos los datos de un Usuario con el
        rol de institucion, se genere una instancia Usuario y una instancia 
        Institución en la Base de Datos.
        """
        usuario = {
            'username': 'rlopez',
            'first_name': 'Raul',
            'last_name': 'Lopez',
            'email': 'rlopez@gmail.com',
            'password': 'rlopez'
        }
        data = {
            "usuario": usuario,
            "nombre": 'Corazón Delator',
            "director": usuario['first_name'],
            "fecha_fundacion": date(1983,7,19),
            "domicilio": "Calle falsa 123",
            "localidad": "Loc",
            "provincia": "prov",
            "pais": "Arg",
            "telefono": "0123-123456789",
            "cant_empleados": 7,
            "descripcion": "Esto es una instiucion",
            "cbu": 123456789012,
            "cuenta_bancaria": "123-123214/0"
        }
        response = self.client.post(self.url_institucion, data, format='json')
        # Evaluo el usuario
        cantidad = User.objects.count()
        if cantidad > 0:
            usuario_db = User.objects.first()
        self.assertEqual(cantidad, 1)
        self.assertEqual(usuario_db.username, usuario['username'])
        # Evaluo el donante
        cantidad = Institucion.objects.count()
        if cantidad > 0:
            institucion = Institucion.objects.first()
        self.assertEqual(cantidad, 1)
        self.assertEqual(institucion.usuario, usuario_db)
        # Evaluo el estado del response
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    
    def test_crear_usuario_cadete(self):
        """
        Valido que al realizar un POST con todos los datos de un Usuario con el
        rol de Cadete, se genere una instancia Usuario y una instancia Cadete
        en la Base de Datos.
        """
        # Creo la institución que será la que genere el nuevo usuario Cadete
        # username_usuario_institucion = 'rlopez'
        usuario_institucion = User.objects.create_user(
            'rlopez',
            'rlopez@gmail.com',
            password='rlopez',
            first_name='Raul',
            last_name='Lopez'
        )
        usuario_institucion.groups.set([self.group_institucion.id,])
        institucion = Institucion.objects.create(
            usuario=usuario_institucion,
            nombre='Corazón Delator',
            director=usuario_institucion.first_name,
            fecha_fundacion=date(1983,7,19),
            domicilio="Calle falsa 123",
            localidad="Loc",
            provincia="prov",
            pais="Arg",
            telefono="0123-123456789",
            cant_empleados=7,
            descripcion="Esto es una instiucion",
            cbu=123456789012,
            cuenta_bancaria="123-123214/0"
        )
        # Creación de Cadete
        usuario_cadete = {
            'username': 'tsanchez',
            'first_name': 'Teresa',
            'last_name': 'Sanchez',
            'email': 'tsanchez@gmail.com',
            'password': 'tsanchez'
        }
        data = {
            "usuario": usuario_cadete,
            "institucion": institucion.id,
            "nombre": "Teresa",
            "apellido": "Sanchez",
            "fecha_nacimiento": date(1983,7,19),
            "dni": "12345678",
            "domicilio": "Calle falsa 123",
            "localidad": "Loc",
            "provincia": "prov",
            "pais": "Arg",
            "telefono": "0123-123456789",
            "estado_civil": "Estado",
            "genero": "Genero",
            "ocupacion": "Ocupación",
            "medio_transporte": "Camioneta Chevrolet 3 asietos con caja (de madera)"
        }
        response = self.client.post(self.url_cadete, data, format='json')
        # Evaluo el usuario y la institucion
        cantidad = User.objects.count()
        if cantidad > 0:
            for u in User.objects.all():
                if u.groups.all()[0] == self.group_institucion:
                    usuario_institucion_db = u
                elif u.groups.all()[0] == self.group_cadete:
                    usuario_cadete_db = u
        self.assertGreater(cantidad, 0)
        self.assertEqual(usuario_institucion_db, usuario_institucion)
        # Evalúo la institución
        cantidad = Institucion.objects.count()
        if cantidad > 0:
            institucion_db = Institucion.objects.first()
        self.assertEqual(cantidad, 1)
        self.assertEqual(institucion_db.usuario, usuario_institucion_db)
        #self.assertEqual(institucion_db.usuario.username, usuario_institucion_db.username)
        # Evaluo el cadete
        cantidad = Cadete.objects.count()
        if cantidad > 0:
            cadete = Cadete.objects.first()
        self.assertEqual(cantidad, 1)
        self.assertEqual(cadete.usuario, usuario_cadete_db)
        # Evaluo el estado del response
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class LoginUsuarioTestCase(APITestCase):
    """Pruebas que validan el login de un usuario"""
    def setUp(self):
        self.username = 'john'
        self.password = 'johnpassword'
        self.usuario = User.objects.create_user(
                                        self.username,
                                        'lennon@thebeatles.com',
                                        self.password,
                                        first_name='john',
                                        last_name='lennon'
                                    )
        self.client = APIClient()
        self.url = reverse('login')

    def test_login_usuario(self):
        """Valido login de un usuario"""
        data = {
            'username': self.username,
            'password': self.password
        }
        response = self.client.post(self.url,data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.usuario.id,response.data['id'])
        self.assertEqual(self.usuario.username,response.data['username'])

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

    def test_doble_login_usuario(self):
        """Valido login de usuario cuando el usuario ya está logueado"""
        data = {
            'username': self.username,
            'password': self.password
        }
        self.client.post(self.url, data)
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.usuario.id,response.data['id'])
        self.assertEqual(self.usuario.username,response.data['username'])


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
        self.client.force_login(self.usuario)
        session = Session.objects.get(pk = self.client.session.session_key)
        user_id = int(session.get_decoded()['_auth_user_id'])
        self.assertEqual(user_id, self.usuario.id)
        if user_id:
            response = self.client.post(self.url)
            cantidad = Session.objects.filter(pk = self.client.session.session_key).count()
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(cantidad,0)

    def test_logout_doble_usuario(self):
        """
        Valida que ocurra un error si el usuario realiza un segundo logout
        consecutivo
        """
        login_user = self.client.login(username=self.username,
                                       password=self.password)
        self.assertTrue(login_user)
        if login_user is not None:
            token, created = Token.objects.get_or_create(user = self.usuario)
            self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
            data = {'token':token.key}
            self.client.post(self.url,data)
            response = self.client.post(self.url,data)
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_logout_con_token_aleatorio(self):
        random_token_key = Token.generate_key()
        data = {'token':random_token_key}
        response = self.client.post(self.url,data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class RecuperacionContraseniaEnvioMailTestCase(APITestCase):
    """
    Pruebas que validan la recuperación de contraseña a partir del envío de un
    mail al usuario donde podrá acceder al link con la página de recuperación
    donde ingresará la nueva contraseña
    """
    def setUp(self):
        self.username = 'john'
        self.password = 'johnpassword'
        self.usuario = User.objects.create_user(self.username,
                                                'lennon@thebeatles.com',
                                                self.password,
                                                first_name='john',
                                                last_name='lennon')
        self.client = APIClient()
        self.url = reverse('recuperacion_contrasenia')

    def test_envio_mail(self):
        """Valido que al ingresar mail, se envíe el mail"""
        data = {'email':self.usuario.email}
        response = self.client.post(self.url,data)
        cantidad = CodigoRecuperacion.objects.count()
        if cantidad > 0:
            codigo = CodigoRecuperacion.objects.first()
        self.assertEqual(cantidad,1)
        self.assertEqual(codigo.email,self.usuario.email)
        self.assertTrue(codigo.activo)
        self.assertEqual(codigo.usuario,self.usuario)


class RecuperacionContraseniaIngresoCodigoTestCase(APITestCase):
    """
    docstring
    """
    def setUp(self):
        self.username = 'john'
        self.password = 'johnpassword'
        self.usuario = User.objects.create_user(self.username,
                                                'lennon@thebeatles.com',
                                                self.password,
                                                first_name='john',
                                                last_name='lennon')
        self.client = APIClient()
        self.url = reverse('validar_codigo_recuperacion')
        # GENERO EL CÓDIGO DE VALIDACION QUE SE RECIBE POR MAIL
        self.codigo_recuperacion = CodigoRecuperacion.objects.create(
                                            email=self.usuario.email,
                                            usuario=self.usuario
                                        )

    def test_ingreso_codigo_correcto(self):
        """roscntril"""
        data = {
            'codigo':self.codigo_recuperacion.codigo
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_no_ingreso_codigo(self):
        """roscntril"""
        data = {
            'codigo':''
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_ingreso_codigo_incorrecto(self):
        """roscntril"""
        codigo_incorrecto = 'Hug7K4uRT8'
        data = {
            'codigo':codigo_incorrecto
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)        

    def test_ingreso_codigo_inactivo(self):
        self.codigo_recuperacion.activo = False
        self.codigo_recuperacion.save()
        data = {
            'codigo':self.codigo_recuperacion.codigo
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_ingreso_codigo_vencido(self):
        self.codigo_recuperacion.fecha_expiracion = date.today() - timedelta(days=1)
        self.codigo_recuperacion.save()
        data = {
            'codigo':self.codigo_recuperacion.codigo
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_ingreso_codigo_a_punto_de_vencer(self):
        self.codigo_recuperacion.fecha_expiracion = date.today()
        self.codigo_recuperacion.save()
        data = {
            'codigo':self.codigo_recuperacion.codigo
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

class RecuperacionContraseniaCambioClaveTestCase(APITestCase):
    """docstring"""
    def setUp(self):
        self.username = 'john'
        self.password = 'johnpassword'
        self.usuario = User.objects.create_user(self.username,
                                                'lennon@thebeatles.com',
                                                self.password,
                                                first_name='john',
                                                last_name='lennon')
        self.client = APIClient()
        self.url = reverse('cambiar_contrasenia_recuperada')
        # GENERO EL CÓDIGO DE VALIDACION QUE SE RECIBE POR MAIL
        self.codigo_recuperacion = CodigoRecuperacion.objects.create(
                                            email=self.usuario.email,
                                            usuario=self.usuario
                                        )
        self.nueva_contrasenia = 'ati3rJRgfU5bPy45'

    def test_cambio_contrasenia_por_codigo_correcto(self):
        """roscntril"""
        data = {
            'password':self.nueva_contrasenia,
            'id_user':self.usuario.id
        }
        response = self.client.post(self.url, data)
        usuario = User.objects.get(username=self.usuario.username)
        self.assertTrue(usuario.check_password(self.nueva_contrasenia))
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
    def test_no_cambio_contrasenia_por_codigo_con_vacios(self):
        """roscntril"""
        data = {
            'password':'',
            'id_user':self.codigo_recuperacion.usuario.id
        }
        response = self.client.post(self.url, data)
        usuario = User.objects.get(username=self.usuario.username)
        self.assertFalse(self.usuario.check_password(''))
        self.assertTrue(self.usuario.check_password(self.password))
        self.assertEqual(response.status_code, status.HTTP_409_CONFLICT)


class CambioContraseniaTestCase(APITestCase):
    """docstring"""
    def setUp(self):
        self.username = 'john'
        self.password = 'johnpassword'
        self.usuario = User.objects.create_user(self.username,
                                                'lennon@thebeatles.com',
                                                self.password,
                                                first_name='john',
                                                last_name='lennon')
        self.client = APIClient()
        self.url = reverse('cambiar_contrasenia')
        # Logueo al cliente
        self.client.login(username=self.username,
                          password=self.password)
        self.token, self.created = Token.objects.get_or_create(user = self.usuario)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

        self.nueva_contrasenia = 'nuevaContrasenia'

    def test_cambiar_contrasenia(self):
        data = {
            'old_password':self.password,
            'new_password':self.nueva_contrasenia
        }
        response = self.client.post(self.url, data)
        usuario = User.objects.get(username=self.usuario.username)
        self.assertTrue(usuario.check_password(self.nueva_contrasenia))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_no_cambiar_contra_con_logout(self):
        self.client.logout()
        data = {
            'old_password':self.password,
            'new_password':self.nueva_contrasenia
        }
        response = self.client.post(self.url, data)
        usuario = User.objects.get(username=self.usuario.username)
        self.assertTrue(usuario.check_password(self.password))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_no_cambiar_contra_sin_session(self):

        session = Session.objects.get(pk = self.client.session.session_key)
        self.assertIsNotNone(session)
        session.delete()
        data = {
            'old_password':self.password,
            'new_password':self.nueva_contrasenia
        }
        response = self.client.post(self.url, data)
        usuario = User.objects.get(username=self.usuario.username)
        self.assertTrue(usuario.check_password(self.password))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_no_cambiar_contra_con_password_incorrecto(self):
        password_incorrecto='contraIncorrecta'
        data = {
            'old_password':password_incorrecto,
            'new_password':self.nueva_contrasenia
        }
        response = self.client.post(self.url, data)
        usuario = User.objects.get(username=self.usuario.username)
        self.assertTrue(usuario.check_password(self.password))
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
