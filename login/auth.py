from datetime import datetime

from rest_framework import status
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.views import APIView

from login.serializers import UserAuthSerializer
from django.contrib.sessions.models import Session

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
                        'message': 'Exito!'
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
                        'message': 'Exito!'
                    }, status = status.HTTP_200_OK)
            else:
                return Response({'mensaje':'2-'}, status = status.HTTP_401_UNAUTHORIZED)
        else:
            return Response({'mensaje':'3-'}, status = status.HTTP_400_BAD_REQUEST)
        return Response({'mensaje':'1-'}, status = status.HTTP_200_OK)

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

            return Response({
                'logout Exito!'
            }, status = status.HTTP_200_OK)
        else:
            return Response({'message':'Error'},status = status.HTTP_400_BAD_REQUEST)