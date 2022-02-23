from datetime import datetime
from urllib import response

from django.contrib.sessions.models import Session
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist, EmptyResultSet, MultipleObjectsReturned

from rest_framework import status
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.views import APIView

from login.serializers import CodigoRecuperacionSerializer, EmailSerializer, UserAuthSerializer, UserPasswordSerializer
from login.models import CodigoRecuperacion

class Login(ObtainAuthToken):

    def post(self,request,*args, **kwargs):
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
                else:
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
            else:
                return Response({'mensaje':'El usuario no se encuentra autorizado'}, status = status.HTTP_401_UNAUTHORIZED)
        else:
            return Response({'mensaje':'El usuario ingresado no se válido'}, status = status.HTTP_400_BAD_REQUEST)

class Logout(APIView):

    def post(self,request,*args, **kwargs):
        token = request.POST.get('token')
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

            return Response({'mensage':'Cierre exitoso!'}, status = status.HTTP_200_OK)
        else:
            return Response({'message':'Ocurrió un error al cerrar la sesión'},status = status.HTTP_400_BAD_REQUEST)


class RecuperacionContraseña(APIView):
    serializer_class = EmailSerializer

    def post(self, request, format=None):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            email = serializer.data['email']

            try:
                usuario = User.objects.get(email=email)

                # * DESACTIVAR TODOS LOS CODIGOS DE RECUPERACIÓN EXISTENTES EN BASE DE DATOS PARA ESE USUARIO
                try:
                    codigos_anteriores = CodigoRecuperacion.objects.filter(activo=1).filter(usuario=usuario.id)
                    for codigo in codigos_anteriores:
                        codigo.delete()
                except CodigoRecuperacion.DoesNotExist:
                    #codigos_anteriores = None
                    pass

                if usuario.is_active:
                    #* CREAR UNA NUEVA INSTANCIA DE CÓDIGO DE RECUPERACIÓN Y ASIGNAR RESULTADO EN VARIABLE
                    codigo_recup_serializer = CodigoRecuperacionSerializer(data = {'email':email,'usuario':usuario.id})
                    codigo_recup_serializer.usuario = usuario
                    if codigo_recup_serializer.is_valid():
                        codigo_recup_serializer.save()

                    #* ENVIAR MAIL CON EL CÓDIGO DE RECUPERACIÓN

                    #* DEVOLVER LOS DATOS DE LA VARIABLE SERIALIZADA (EN LO POSIBLE, SINO ARMAR JSON MANUALMENTE)
                    return Response({'email':codigo_recup_serializer.data['email']}, status=status.HTTP_201_CREATED)
            
            except User.DoesNotExist:
                return Response({'mensaje':'El usuario no es válido'}, status=status.HTTP_401_UNAUTHORIZED)

        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
                    

class CambiarContraseñaRecuperada(APIView):
    serializer_class = UserPasswordSerializer
    
    def get(self, request, code):
        try:
            cod_rec = CodigoRecuperacion.objects.get(codigo=code)
        except ObjectDoesNotExist:
            return Response({'mensaje':'Código Incorrecto'},status=status.HTTP_400_BAD_REQUEST)
        except EmptyResultSet:
            return Response({'mensaje':'Código Incorrecto'},status=status.HTTP_400_BAD_REQUEST)
        except MultipleObjectsReturned:
            return Response({'mensaje':'Código Incorrecto'},status=status.HTTP_400_BAD_REQUEST)

        if not(cod_rec.activo):
            return Response({'mensaje':'El código no se encunetra activo'},status=status.HTTP_401_UNAUTHORIZED)

        if cod_rec.fecha_expiracion < datetime.now().date():
            return Response({'mensaje':'El código se encunetra caducado'},status=status.HTTP_401_UNAUTHORIZED)
        print(cod_rec.usuario.get_username())
        #cod_rec_serializer = UserPasswordSerializer(cod_rec.usuario.get_username())
        #cod_rec_serializer = UserPasswordSerializer(data={'username':cod_rec.usuario.get_username()})
        #print(cod_rec_serializer)
        #if cod_rec_serializer.is_valid():
        #    return Response(cod_rec_serializer.data,status=status.HTTP_200_OK)
        #else:
        #    print('UPS2')
        #    return Response({'mensaje':cod_rec_serializer.error_messages},status=status.HTTP_409_CONFLICT)
        return Response({'username':cod_rec.usuario.get_username()},status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        print(request.data)
        rec_password_serializer = UserPasswordSerializer(data = request.data)
        print(rec_password_serializer)
        print(rec_password_serializer.is_valid())
        if rec_password_serializer.is_valid():
            print('HASTA ACÁ LLEGÓ')
            rec_password_serializer.save()
            print('Y POR ACÁ TAMBIÉN')
            return Response({'mensaje':'La contraseña fue cambiada con éxito'},status=status.HTTP_201_CREATED)
        
        return Response({'mensaje':rec_password_serializer.error_messages},status=status.HTTP_409_CONFLICT)

# class ChangePasswordView(UpdateAPIView):
#     serializer_class = RecuperarContraseñaSerializer

#     def update(self, request, *args, **kwargs):
#         serializer = self.get_serializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         user = serializer.save()
#         # if using drf authtoken, create a new token 
#         if hasattr(user, 'auth_token'):
#             user.auth_token.delete()
#         token, created = Token.objects.get_or_create(user=user)
#         # return new token
#         return Response({'token': token.key}, status=status.HTTP_200_OK)