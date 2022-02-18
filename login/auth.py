from datetime import datetime

from rest_framework import status
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.views import APIView

from login.serializers import CodigoRecuperacionSerializer, EmailSerializer, UserAuthSerializer
from login.models import CodigoRecuperacion
from django.contrib.sessions.models import Session
from django.contrib.auth.models import User

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
                    