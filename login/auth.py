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

from login.serializers import CodigoRecuperacionSerializer, EmailSerializer, \
                                UserAuthSerializer, \
                                CambioContraseniaSerializer, CodigoSerializer, \
                                RecuperacionContraseniaSerializer
from login.models import CodigoRecuperacion

# pylint: disable:no-member

class Login(ObtainAuthToken):
    """docstring"""
    def post(self,request,*args, **kwargs):
        """docstring"""
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
    """docstring"""
    def post(self,request):
        """docstring"""
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
    """docstring"""
    serializer_class = EmailSerializer

    def post(self, request):
        """docstring"""
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
    """docstring"""
    serializer_class = CodigoSerializer

    def post(self,request):
        """docstring"""
        print(request.data)
        print(request.data['codigo'])
        rec_password_serializer = CodigoSerializer(data = {'codigo':request.data['codigo']})
        print(rec_password_serializer)
        print(rec_password_serializer.is_valid())
        print('ESTO ES codigo: ',rec_password_serializer['codigo'])
        print('TIPO CODIGO: ',type(rec_password_serializer['codigo']))
        if rec_password_serializer.is_valid():
            try:
                cod_rec = CodigoRecuperacion.objects.get(codigo=rec_password_serializer['codigo'])
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
                return Response({'mensaje':'El código no se encunetra activo'},
                                status=status.HTTP_401_UNAUTHORIZED)

            if cod_rec.fecha_expiracion < datetime.now().date():
                return Response({'mensaje':'El código se encunetra caducado'},
                                status=status.HTTP_401_UNAUTHORIZED)

            return Response({'user':cod_rec.usuario},
                            status=status.HTTP_200_OK)
        else:
            return Response(rec_password_serializer.errors,
                                status=status.HTTP_400_BAD_REQUEST)

    
class RecuperacionContrasenia(APIView):
    """docstring"""
    serializer_class = RecuperacionContraseniaSerializer

    def post(request):
        """docstring"""
        print(request.data)
        rec_password_serializer = RecuperacionContraseniaSerializer(data = request.data)
        print(rec_password_serializer)
        print(rec_password_serializer.is_valid())
        if rec_password_serializer.is_valid():
            print('HASTA ACÁ LLEGÓ')
            rec_password_serializer.save()
            print('Y POR ACÁ TAMBIÉN')
            return Response({'mensaje':'La contraseña fue cambiada con éxito'},
                            status=status.HTTP_201_CREATED)

        return Response({'mensaje':rec_password_serializer.error_messages},
                        status=status.HTTP_409_CONFLICT)


# class CambiarContraseniaRecuperada(APIView):
#     """docstring"""
#     serializer_class = UserPasswordSerializer

#     def get(code, *args, **kwargs):
#         """docstring"""
#         try:
#             cod_rec = CodigoRecuperacion.objects.get(codigo=code)
#         except ObjectDoesNotExist:
#             return Response({'mensaje':'Código Incorrecto'},
#                             status=status.HTTP_400_BAD_REQUEST)
#         except EmptyResultSet:
#             return Response({'mensaje':'Código Incorrecto'},
#                             status=status.HTTP_400_BAD_REQUEST)
#         except MultipleObjectsReturned:
#             return Response({'mensaje':'Código Incorrecto'},
#                             status=status.HTTP_400_BAD_REQUEST)

#         if not cod_rec.activo:
#             return Response({'mensaje':'El código no se encunetra activo'},
#                             status=status.HTTP_401_UNAUTHORIZED)

#         if cod_rec.fecha_expiracion < datetime.now().date():
#             return Response({'mensaje':'El código se encunetra caducado'},
#                             status=status.HTTP_401_UNAUTHORIZED)

#         return Response({'user':cod_rec.usuario},
#                         status=status.HTTP_200_OK)

#     def post(request):
#         """docstring"""
#         print(request.data)
#         rec_password_serializer = UserPasswordSerializer(data = request.data)
#         print(rec_password_serializer)
#         print(rec_password_serializer.is_valid())
#         if rec_password_serializer.is_valid():
#             print('HASTA ACÁ LLEGÓ')
#             rec_password_serializer.save()
#             print('Y POR ACÁ TAMBIÉN')
#             return Response({'mensaje':'La contraseña fue cambiada con éxito'},
#                             status=status.HTTP_201_CREATED)

#         return Response({'mensaje':rec_password_serializer.error_messages},
#                         status=status.HTTP_409_CONFLICT)


class CambioContrasenia(APIView):
    serializer_class = CambioContraseniaSerializer

    def post(self,request):
        token = request.POST.get('token')
        token = Token.objects.filter(key=token).first()
        if token:
            user = token.user
            serializer = CambioContraseniaSerializer(data = request.data)
            serializer.is_valid(raise_exception=True)
            print(serializer.validated_data)
            if user.check_password(serializer.validated_data['old_password']):
                user.set_password(serializer.validated_data['new_password1'])
                user.save()
                return Response({'mensaje':'La contraseña fue actualizada con éxito'},
                                status=status.HTTP_200_OK)
            
            return Response({'mensaje':'La contraseña ingresada no es correcta'},
                            status=status.HTTP_400_BAD_REQUEST)
        
        return Response({'ensaje':'Token inválido'},
                        status=status.HTTP_400_BAD_REQUEST)

        
        # # if using drf authtoken, create a new token
        # if hasattr(user, 'auth_token'):
        #     user.auth_token.delete()
        # token, created = Token.objects.get_or_create(user=user)
        # # return new token
        # return Response({'token': token.key}, status=status.HTTP_200_OK)
