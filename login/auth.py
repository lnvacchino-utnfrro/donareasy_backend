"""docstring"""
from datetime import datetime

from django.contrib.sessions.models import Session
from django.contrib.auth.models import User
from django.contrib import auth
from django.core.exceptions import ObjectDoesNotExist, EmptyResultSet, MultipleObjectsReturned
from django.core.mail import BadHeaderError, send_mail
from django.template import loader
from django.urls import reverse

from rest_framework import status
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.views import APIView

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema, no_body

from login.serializers import CodigoRecuperacionSerializer, EmailSerializer, \
                                UserAuthSerializer, TokenSerializer, \
                                CambioContraseniaSerializer, CodigoSerializer, \
                                RecuperacionContraseniaSerializer, UserSerializer, \
                                LoginResponseSerializer
from login.models import CodigoRecuperacion
from baseApp.models import Donante, Institucion, Cadete

from donareasy.utils import CsrfExemptSessionAuthentication
from rest_framework.authentication import BasicAuthentication 

# pylint: disable:no-member

def obtenerDatosUsuario(user):
    group = user.groups.first()
    if group:
        if group.id == 1:
            # El usuario es un donante
            grupo = group.name
            donante = Donante.objects.get(usuario=user.id)
            nombre = donante.nombre + ' ' + donante.apellido
            grupo_id = donante.id
        
        elif group.id == 2:
            # El usuario es una institución
            grupo = group.name
            institucion = Institucion.objects.get(usuario=user.id)
            nombre = institucion.nombre
            grupo_id = institucion.id

            if institucion.habilitado == 0:
                grupo = 'Institución inhabilitada'

        elif group.id == 3:
            # El usuario es un cadete
            grupo = group.name
            cadete = Cadete.objects.get(usuario=user.id)
            nombre = cadete.nombre + ' ' + cadete.apellido
            grupo_id = cadete.id

        else:
            grupo = 'Undefined'
            nombre = user.username

    else:
        # El usuario no tiene definido ningún rol
        grupo = 'Undefined'
        nombre = user.username

    response = {
        'id': user.id,
        'username': user.username,
        'group': grupo,
        'nombre': nombre,
        'groupId': grupo_id,
    }

    return response

class Login(APIView):
    """
    Ingreso de un usuario al sistema. Al recibir el usuario y contraseña, 
    se devuelven los datos del usuario y el token.
    """
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)
    serializer_class = UserAuthSerializer

    @swagger_auto_schema(
        request_body=UserAuthSerializer,
        operation_summary='Login',
        responses={
            200: LoginResponseSerializer,
            400: 'Los datos no son válidos',
            401: 'El usuario no se encuentra autorizado',
        }
    )
    def post(self,request,*args, **kwargs):
        """
        Al recibir los datos, se validan que sean correctos y pertenezca a un
        usuario que esté activo. Luego, se crea el token de sesion y se lo
        devuelve. En caso de ya existir la sesión, se lo cerrará y se creará
        otro.
        """
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            user = auth.authenticate(
                username=serializer.validated_data['username'],
                password=serializer.validated_data['password']
            )
            if user is not None:
                if user.is_active:                   
                    #? Formas de acceder a los datos de la sesión
                    # print(request.user)
                    # print('session: ',request.session.session_key)
                    # session = Session.objects.get(pk = request.session.session_key)
                    # print('data: ',session.session_data)
                    # print('expire_date: ',session.expire_date)
                    # print('get_decode: ',session.get_decoded())

                    # Busco los datos restantes del usuario según el tipo de usuario
                    response = obtenerDatosUsuario(user)

                    #Si la institucion está inhabilitada, le niego el ingreso
                    if response['group'] == 'Institución inhabilitada':
                        return Response({'mensaje':'La institución se encuentra inhabilitada'},
                                        status = status.HTTP_406_NOT_ACCEPTABLE)

                    # Contraseña correcta y usuario activo y habilitado
                    auth.login(request,user)

                    return Response(response, status = status.HTTP_200_OK)

                return Response({'mensaje':'El usuario no se encuentra autorizado'},
                                status = status.HTTP_401_UNAUTHORIZED)

            return Response({'mensaje':'Los datos no son válidos'},
                            status = status.HTTP_400_BAD_REQUEST)

        return Response({'mensaje':'Los datos no son válidos'},
                            status = status.HTTP_400_BAD_REQUEST)

class Logout(APIView):
    """Cierre de sesión de un usuario del sistema."""
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)

    @swagger_auto_schema(
        request_body=no_body,
        operation_summary='Logout',
        responses={
            200: 'Cierre Exitoso',
            400: 'Ocurrió un error al cerrar la sesión',
        }
    )
    def post(self,request):
        """
        Se recibe el token asociado a la sesión de un usuario. Si el token y la
        sesión asociada existen, entonces se borra la sesión y el token.
        """
        if not request.user.is_anonymous:
            auth.logout(request)

            return Response({'mensage':'Cierre exitoso!'},
                            status = status.HTTP_200_OK)

        return Response({'message':'Ocurrió un error al cerrar la sesión'},
                        status = status.HTTP_400_BAD_REQUEST)


class GenerarCodigoRecuperacionContrasenia(APIView):
    """
    Generación del código de Recuperación de contraseña a partir de la
    recepción de un correo electrónico de un usuario activo del sistema
    """
    serializer_class = EmailSerializer
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)

    @swagger_auto_schema(
        request_body=EmailSerializer,
        operation_summary='Recuperación 1: Generación de Código',
        responses={
            201: 'Éxito',
            400: 'Ocurrió un error en la recepción de los datos',
            401: 'El usuario está inactivo o no es válido',
        }
    )
    def post(self, request):
        """
        Se recibe un correo electrónico de un usuario existente en el sistema.
        Si existe el usuario con dicho mail, se genera el código de recuperación
        y se desactivan los anteriores generados por el usuario. Por último, se
        envía un mail al usuario con el código.
        """
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            email = serializer.data['email']
            try:
                usuario = User.objects.get(email=email)
                print(usuario)
                #* DESACTIVAR TODOS LOS CODIGOS DE RECUPERACIÓN EXISTENTES EN
                #* BASE DE DATOS PARA ESE USUARIO
                try:
                    codigos_anteriores = CodigoRecuperacion.objects\
                                            .filter(activo=1)\
                                            .filter(usuario=usuario.id)
                    for codigo in codigos_anteriores:
                        codigo.delete()
                except CodigoRecuperacion.DoesNotExist:
                    pass

                if usuario.is_active:
                    #* CREAR UNA NUEVA INSTANCIA DE CÓDIGO DE RECUPERACIÓN Y
                    #* ASIGNAR RESULTADO EN VARIABLE
                    codigo_recup_serializer = CodigoRecuperacionSerializer(
                                                        data = {
                                                            'email':email,
                                                            'usuario':usuario.id
                                                        })
                    codigo_recup_serializer.usuario = usuario
                    if codigo_recup_serializer.is_valid():
                        codigo = codigo_recup_serializer.save()

                    #* ENVIAR MAIL CON EL CÓDIGO DE RECUPERACIÓN
                    dominio = 'http://127.0.0.1:8000'
                    ruta = reverse('validar_codigo_recuperacion')
                    template = loader.get_template('recuperacion_password.html')
                    context = {
                        'dominio': dominio,
                        'ruta':ruta,
                        'codigo':codigo
                    }
                    html_message = template.render(context, request)
                    try:
                        send_mail(
                            email,
                            'esto es un mensaje de recuperacion',
                            'donareasy@gmail.com',
                            [email,],
                            html_message=html_message
                        )
                    except BadHeaderError:
                        return Response({'mensaje':'invalid header found'},
                                        status=status.HTTP_400_BAD_REQUEST)

                    #* DEVOLVER LOS DATOS DE LA VARIABLE SERIALIZADA
                    #* (EN LO POSIBLE, SINO ARMAR JSON MANUALMENTE)
                    return Response({'mensaje':'Exito'},
                                    status=status.HTTP_201_CREATED)

                return Response({'mensaje':'El usuario está inactivo'},
                                status=status.HTTP_401_UNAUTHORIZED)

            except User.DoesNotExist:
                return Response({'mensaje':'El correo ingresado es incorrecto'},
                                status=status.HTTP_400_BAD_REQUEST)

        else:
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)


class ValidarCodigoRecuperacionContrasenia(APIView):
    """
    Ingreso de Código de Recuperación para validar la identificación del usuario
    que ha solicitado la recuperación de la contraseña.
    """
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)
    serializer_class = CodigoSerializer

    user_response = openapi.Response('Usuario',UserSerializer)

    @swagger_auto_schema(
        request_body=CodigoSerializer,
        operation_summary='Recuperación 2: Ingreso de Código',
        responses={
            200: LoginResponseSerializer,
            400: 'El código es incorrecto o se ha ingresado incorrectamente los datos',
            401: 'El código no se encuentra activo o se encuentra caducado',
        }
    )
    def post(self,request):
        """
        Se ingresa un código de recuperación y se valida que éste exista y se
        encuentra activo y no caducado. Si es válido, se devuelven los datos
        del usuario
        """
        rec_password_serializer = CodigoSerializer(data = {'codigo':request.data['codigo']})
        if rec_password_serializer.is_valid():
            try:
                cod_rec = CodigoRecuperacion.objects.get(codigo=rec_password_serializer.data['codigo'])
            except ObjectDoesNotExist:
                return Response({'mensaje':'Código Incorrecto'},
                                status=status.HTTP_400_BAD_REQUEST)
            except EmptyResultSet:
                return Response({'mensaje':'Código Incorrecto'},
                                status=status.HTTP_400_BAD_REQUEST)
            except MultipleObjectsReturned:
                return Response({'mensaje':'Código Incorrecto'},
                                status=status.HTTP_400_BAD_REQUEST)
            if not cod_rec.activo:
                return Response({'mensaje':'El código no se encuentra activo'},
                                status=status.HTTP_401_UNAUTHORIZED)

            if cod_rec.fecha_expiracion < datetime.now().date():
                return Response({'mensaje':'El código se encuentra caducado'},
                                status=status.HTTP_401_UNAUTHORIZED)

            # usuario_serializer = UserSerializer(cod_rec.usuario)
            response = obtenerDatosUsuario(cod_rec.usuario)

            return Response(response, status = status.HTTP_200_OK)

        else:
            return Response(rec_password_serializer.errors,
                                status=status.HTTP_400_BAD_REQUEST)

    
class RecuperacionContrasenia(APIView):
    """
    Registro de la nueva contraseña a partir de la utilización del Código de
    Recuperación.
    """
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)
    serializer_class = RecuperacionContraseniaSerializer

    @swagger_auto_schema(
        request_body=RecuperacionContraseniaSerializer,
        operation_summary='Recuperación 3: Actualización de Contraseña',
        responses={
            201: 'La contraseña fue cambiada con éxito',
            409: 'Se ha ingresado incorrectamente los datos',
        }
    )
    def post(self,request):
        """Se ingresa el ID del usuario y la nueva contraseña a actualizar"""
        rec_password_serializer = RecuperacionContraseniaSerializer(data = {
                                                                'password':request.data['password'],
                                                                'id_user':request.data['id_user']
                                                            })
        if rec_password_serializer.is_valid():
            rec_password_serializer.save()
            return Response({'mensaje':'La contraseña fue cambiada con éxito'},
                            status=status.HTTP_201_CREATED)

        return Response({'mensaje':rec_password_serializer.errors},
                        status=status.HTTP_409_CONFLICT)


class CambioContrasenia(APIView):
    """Cambio de contraseña"""
    serializer_class = CambioContraseniaSerializer
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)
    
    @swagger_auto_schema(
        request_body=CambioContraseniaSerializer,
        operation_summary='Cambio de Contraseña',
        responses={
            200: 'La contraseña fue actualizada con éxito',
            400: 'La contraseña ingresada no es correcta',
            403: 'Usuario no ha iniciado sesión',
            406: 'Error en el ingreso de datos',
        }
    )
    def post(self,request):
        """
        Se ingresa el token, la contraseña actual y la nueva contraseña. En el 
        caso de éxito, se actualiza la contraseña. Pero, si el token es inválido
        o la contraseña actual no coincide al usuario o la nueva contraseña no
        es correcta según los patrones de seguridad, se retorna error. 
        """
        user = request.user
        if not user.is_anonymous:
            serializer = CambioContraseniaSerializer(data = request.data)
            if serializer.is_valid():
                if user.check_password(serializer.validated_data['old_password']):
                    user.set_password(serializer.validated_data['new_password'])
                    user.save()

                    return Response({'mensaje':'La contraseña fue actualizada con éxito'},
                                    status=status.HTTP_200_OK)
                
                return Response({'mensaje':'La contraseña ingresada no es correcta'},
                                status=status.HTTP_400_BAD_REQUEST)

            return Response({'mensaje':serializer.errors},
                            status=status.HTTP_406_NOT_ACCEPTABLE)

        return Response({'mensaje':'Usuario no ha iniciado sesión'},
                        status=status.HTTP_403_FORBIDDEN)
