"""docstring"""
from unittest.util import _MAX_LENGTH
from django.contrib.auth.models import User, UserManager, Group
from django.contrib.auth.password_validation import validate_password

from django.contrib.auth.models import User
from django.core.mail import BadHeaderError, send_mail
from django.template import loader
from django.urls import reverse

from rest_framework import serializers

from baseApp.models import Cadete, Donante, Institucion
from baseApp.serializers import DonanteSinForeingKeySerializer

from login.models import CodigoRecuperacion

# pylint: disable=no-member

class UserSerializer(serializers.ModelSerializer):
    """docstring"""
    class Meta:
        # pylint: disable=missing-class-docstring
        model = User
        fields = ['id','username','first_name','last_name','email','password','groups']


class UserAuthSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=255)
    password = serializers.CharField(max_length=255)


class UserSinGroupSerializer(serializers.ModelSerializer):
    """docstring"""
    class Meta:
        # pylint: disable=missing-class-docstring
        model = User
        fields = ['username','first_name','last_name','email','password']


class EmailSerializer(serializers.Serializer):
    """docstring"""
    email = serializers.EmailField(max_length=255)


class CodigoSerializer(serializers.Serializer):
    """docstring"""
    codigo = serializers.CharField(max_length=255)


class CodigoRecuperacionSerializer(serializers.ModelSerializer):
    """docstring"""
    class Meta:
        # pylint: disable=missing-class-docstring
        model = CodigoRecuperacion
        fields = ['email','usuario']

    def create(self, validated_data):
        """parámetro validated_data es un dato tipo diccionario. Ya está validado"""
        codigo_recuperacion = self.Meta.model(
            email=validated_data['email'],
            usuario=validated_data['usuario'],
        )
        codigo_recuperacion.save()
        return codigo_recuperacion.codigo


class RecuperacionContraseniaSerializer(serializers.Serializer):
    """docstring"""
    password = serializers.CharField(max_length=255)
    id_user = serializers.IntegerField()

    def save(self):
        """docstring"""
        user = User.objects.get(id=self.validated_data['id_user'])
        user.set_password(self.validated_data['password'])
        CodigoRecuperacion.objects.filter(usuario=user).filter(activo=1).delete()
        user.save()
        return user

    def validate_password(self,value):
        """docstring"""
        validate_password(value)
        return value


class CambioContraseniaSerializer(serializers.Serializer):
    old_password = serializers.CharField(max_length=128, write_only=True, required=True)
    new_password = serializers.CharField(max_length=128, write_only=True, required=True)

    def validate_new_password(self,value):
        """docstring"""
        validate_password(value)
        return value


class LogupDonanteUserSerializer(serializers.ModelSerializer):
    usuario = UserSinGroupSerializer()

    class Meta:
        model = Donante
        fields = ['usuario','nombre','apellido','fecha_nacimiento','dni','domicilio','localidad','provincia',
        'pais','telefono','estado_civil','genero','ocupacion']

    def create(self, validated_data):
        usuario_data = validated_data.pop('usuario', None)
        usuario = User.objects.create_user(
            username=usuario_data['username'],
            email=usuario_data['email'],
            password=usuario_data['password'],
            first_name=usuario_data['first_name'],
            last_name=usuario_data['last_name']
        )
        usuario.groups.set([1])
        donante = Donante.objects.create(
            usuario=usuario,
            **validated_data
        )
        return donante


class DonanteUserSerializer(serializers.ModelSerializer):
    usuario = UserSerializer()

    class Meta:
        model = Donante
        fields = ['usuario','nombre','apellido','fecha_nacimiento','dni','domicilio','localidad','provincia',
        'pais','telefono','estado_civil','genero','ocupacion']

    def create(self, validated_data):
        usuario_data = validated_data.pop('usuario', None)
        usuario = User.objects.create_user(
            username=usuario_data['username'],
            email=usuario_data['email'],
            password=usuario_data['password'],
            first_name=usuario_data['first_name'],
            last_name=usuario_data['last_name']
        )
        usuario.groups.set(usuario_data['groups'])
        donante = Donante.objects.create(
            usuario=usuario,
            **validated_data
        )
        return donante


class LogupInstitucionUserSerializer(serializers.ModelSerializer):
    usuario = UserSinGroupSerializer()

    class Meta:
        model = Institucion
        fields = ['usuario','nombre','director','fecha_fundacion','domicilio',
                    'localidad','provincia','pais','telefono','cant_empleados',
                    'descripcion','cbu']

    def create(self, validated_data):
        usuario_data = validated_data.pop('usuario', None)
        usuario = User.objects.create_user(
            username=usuario_data['username'],
            email=usuario_data['email'],
            password=usuario_data['password'],
            first_name=usuario_data['first_name'],
            last_name=usuario_data['last_name']
        )
        usuario.groups.set([2])
        institucion = Institucion.objects.create(
            usuario=usuario,
            **validated_data
        )

         #* ENVIAR MAIL CON EL CÓDIGO DE RECUPERACIÓN
        email = 'donareasy@gmail.com'
        dominio = 'http://127.0.0.1:8000'
        ruta = ''
        template = loader.get_template('nueva_institucion.html')
        context = {
            'dominio': dominio,
            'ruta':ruta,
            'institucion':institucion,
            'email':usuario_data['email'],
        }
        html_message = template.render(context)
        try:
            send_mail(
                email,
                'esto es un mensaje de institución nuevo',
                'donareasy@gmail.com',
                [email,],
                html_message=html_message
            )
        except BadHeaderError:
            raise serializers.ValidationError("Error en el envío de codigo de habilitación")

        return institucion


class InstitucionUserSerializer(serializers.ModelSerializer):
    usuario = UserSerializer()

    class Meta:
        model = Institucion
        fields = ['usuario','nombre','director','fecha_fundacion','domicilio',
                    'localidad','provincia','pais','telefono','cant_empleados',
                    'descripcion','cbu']

    def create(self, validated_data):
        usuario_data = validated_data.pop('usuario', None)
        usuario = User.objects.create_user(
            username=usuario_data['username'],
            email=usuario_data['email'],
            password=usuario_data['password'],
            first_name=usuario_data['first_name'],
            last_name=usuario_data['last_name']
        )
        usuario.groups.set(usuario_data['groups'])
        institucion = Institucion.objects.create(
            usuario=usuario,
            **validated_data
        ) 
        return institucion


class LogupCadeteUserSerializer(serializers.ModelSerializer):
    usuario = UserSinGroupSerializer()

    class Meta:
        model = Cadete
        fields = ['usuario','nombre','apellido','fecha_nacimiento','dni','domicilio','localidad','provincia',
        'pais','telefono','estado_civil','genero','ocupacion','medio_transporte']

    def create(self, validated_data):
        usuario_data = validated_data.pop('usuario', None)
        usuario = User.objects.create_user(
            username=usuario_data['username'],
            email=usuario_data['email'],
            password=usuario_data['password'],
            first_name=usuario_data['first_name'],
            last_name=usuario_data['last_name']
        )
        usuario.groups.set([3])
        cadete = Cadete.objects.create(
            usuario=usuario,
            **validated_data
        )
        return cadete


class CadeteUserSerializer(serializers.ModelSerializer):
    usuario = UserSerializer()

    class Meta:
        model = Cadete
        fields = ['usuario','nombre','apellido','fecha_nacimiento','dni','domicilio','localidad','provincia',
        'pais','telefono','estado_civil','genero','ocupacion','medio_transporte']

    def create(self, validated_data):
        usuario_data = validated_data.pop('usuario', None)
        usuario = User.objects.create_user(
            username=usuario_data['username'],
            email=usuario_data['email'],
            password=usuario_data['password'],
            first_name=usuario_data['first_name'],
            last_name=usuario_data['last_name']
        )
        usuario.groups.set(usuario_data['groups'])
        cadete = Cadete.objects.create(
            usuario=usuario,
            **validated_data
        )
        return cadete


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ['id','name']


class TokenSerializer(serializers.Serializer):
    """docstring"""
    token = serializers.CharField(max_length=255)


class PublicUserSerializer(serializers.ModelSerializer):
    """docstring""" 
    class Meta:
        # pylint: disable=missing-class-docstring
        model = User
        fields = ['id','username','first_name','last_name']


class LoginResponseSerializer(serializers.Serializer):
    """docstring"""
    id = serializers.IntegerField()
    username = serializers.CharField(max_length=255)
    group = serializers.CharField(max_length=255)
    nombre = serializers.CharField(max_length=255)


class InstitucionNoHabilitadaSerializer(serializers.Serializer):

    # username = serializers.CharField(max_length=255)
    # password = serializers.CharField(max_length=255)
    codigo_habilitacion = serializers.CharField(max_length=255)

    # class Meta:
    #     model = Institucion
    #     fields = '__all__'
    #     read_only_fields = ['usuario','nombre','director','fecha_fundacion','domicilio',
    #                         'localidad','provincia','pais','telefono','cant_empleados',
    #                         'descripcion','cbu','habilitado']
        

    # def update(self,institucion,validated_data):
    #     usuario_data = validated_data['username']
    #     password_data = validated_data['password']
    #     codigo_habilitacion = validated_data['codigo_habilitacion']
    #     usuario = User.objects.get(username = usuario_data)
    #     if usuario:
    #         if usuario.check_password(password_data):
    #             institucion = Institucion.objects.get(usuario=usuario)
    #             if institucion:
    #                 if not institucion.habilitado:
    #                     if institucion.codigo_habilitacion == codigo_habilitacion:
    #                         institucion.habilitado = True
    #                         institucion.save()
    #                         return institucion
    #                     else:
    #                         raise serializers.ValidationError("Codigo de habilitacion incorrecto")
    #                 else:
    #                     raise serializers.ValidationError("La institucion ya se encuentra habilitada")
    #             else:
    #                 raise serializers.ValidationError("No existe la institución")
    #         else:
    #             raise serializers.ValidationError("Contraseña Incorrecta")
    #     else:
    #         raise serializers.ValidationError("No existe el usuario")

         
                
        
        
