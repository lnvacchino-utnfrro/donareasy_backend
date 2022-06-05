"""docstring"""
from datetime import datetime

from django.contrib.sessions.models import Session
from django.contrib.auth.models import User
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
from drf_yasg.utils import swagger_auto_schema

from login.serializers import CodigoRecuperacionSerializer, EmailSerializer, \
                                UserAuthSerializer, TokenSerializer, \
                                CambioContraseniaSerializer, CodigoSerializer, \
                                RecuperacionContraseniaSerializer, UserSerializer
from login.models import CodigoRecuperacion

# pylint: disable:no-member

class Login(ObtainAuthToken):
    """
    Ingreso de un usuario al sistema. Al recibir el usuario y contraseña, 
    se devuelven los datos del usuario y el token.
    """
    @swagger_auto_schema(
        operation_summary='Login',
        response={
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
        login_serializer = self.serializer_class(data = request.data, context = {'request':request})
        if login_serializer.is_valid():
            user = login_serializer.validated_data['user']
            if user.is_active:
                token, created = Token.objects.get_or_create(user = user)
                user_serializer = UserAuthSerializer(user)
                if created:
                    return Response({
                        'token': token.key,
                        'user': user_serializer.data,
                        'message': 'Ingreso Exitoso!'
                    }, status = status.HTTP_200_OK)

                sessions = Session.objects.filter(expire_date__gte = datetime.now())
                if sessions.exists():
                    for session in sessions:
                        session_data = session.get_decoded()
                        if int(session_data.get('_auth_user_id')) == user.id:
                            session.delete()
                token.delete()
                token = Token.objects.create(user = user)
                return Response({
                    'token': token.key,
                    'user': user_serializer.data,
                    'message': 'Ingreso Exitoso!'
                }, status = status.HTTP_200_OK)

            return Response({'mensaje':'El usuario no se encuentra autorizado'},
                            status = status.HTTP_401_UNAUTHORIZED)

        return Response({'mensaje':'Los datos no son válidos'},
                        status = status.HTTP_400_BAD_REQUEST)

class Logout(APIView):
    """Cierre de sesión de un usuario del sistema."""
    # token_schema = openapi.Schema(
    #     title='token',
    #     description='esto es una descripcion',
    #     type=openapi.TYPE_STRING
    # )
    # token_param = openapi.Parameter(
    #     'token',
    #     openapi.IN_BODY,
    #     # type=openapi.TYPE_STRING,
    #     schema=token_schema,
    #     required=True,
    # )
    @swagger_auto_schema(
        request_body=TokenSerializer,
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
        token = request.data['token']
        token = Token.objects.filter(key = token).first()
        if token:
            user = token.user
            sessions = Session.objects.filter(expire_date__gte = datetime.now())
            if sessions.exists():
                for session in sessions:
                    session_data = session.get_decoded()
                    if int(session_data.get('_auth_user_id')) == user.id:
                        session.delete()
            token.delete()

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
                return Response({'mensaje':'El usuario no es válido'},
                                status=status.HTTP_401_UNAUTHORIZED)

        else:
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)


class ValidarCodigoRecuperacionContrasenia(APIView):
    """
    Ingreso de Código de Recuperación para validar la identificación del usuario
    que ha solicitado la recuperación de la contraseña.
    """
    serializer_class = CodigoSerializer

    user_response = openapi.Response('Usuario',UserSerializer)

    @swagger_auto_schema(
        request_body=CodigoSerializer,
        operation_summary='Recuperación 2: Ingreso de Código',
        responses={
            200: user_response,
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

            usuario_serializer = UserSerializer(cod_rec.usuario)
            return Response({'user':usuario_serializer.data},
                            status=status.HTTP_200_OK)
        else:
            return Response(rec_password_serializer.errors,
                                status=status.HTTP_400_BAD_REQUEST)

    
class RecuperacionContrasenia(APIView):
    """
    Registro de la nueva contraseña a partir de la utilización del Código de
    Recuperación.
    """
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

    @swagger_auto_schema(
        request_body=CambioContraseniaSerializer,
        operation_summary='Cambio de Contraseña',
        responses={
            200: 'La contraseña fue actualizada con éxito',
            400: 'La contraseña y/o el token ingresados no son correctos',
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
        token = request.POST.get('token')
        token = Token.objects.filter(key=token).first()
        if token:
            user = token.user
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
        return Response({'mensaje':'Token inválido'},
                        status=status.HTTP_400_BAD_REQUEST)

    