"""docstring"""
from django.contrib.auth.models import User, UserManager
from django.contrib.auth.password_validation import validate_password

from rest_framework import serializers

from baseApp.models import Donante
from baseApp.serializers import DonanteSinForeingKeySerializer

from login.models import CodigoRecuperacion

# pylint: disable=no-member

class UserSerializer(serializers.ModelSerializer):
    """docstring"""
    class Meta:
        # pylint: disable=missing-class-docstring
        model = User
        fields = ['id','username','first_name','last_name','email','password','groups']


class UserAuthSerializer(serializers.ModelSerializer):
    """docstring"""
    class Meta:
        # pylint: disable=missing-class-docstring
        model = User
        fields = ['username','email','first_name','last_name']


class EmailSerializer(serializers.Serializer):
    """docstring"""
    email = serializers.EmailField(max_length=255)


class CodigoRecuperacionSerializer(serializers.ModelSerializer):
    """docstring"""
    class Meta:
        # pylint: disable=missing-class-docstring
        model = CodigoRecuperacion
        fields = ['email','usuario']

    def create(self, validated_data):
        """docstring"""
        codigo_recuperacion = self.Meta.model(
            email=validated_data['email'],
            usuario=validated_data['usuario'],
        )
        codigo_recuperacion.save()
        return codigo_recuperacion.codigo


class UserPasswordSerializer(serializers.Serializer):
    """docstring"""
    password1 = serializers.CharField(max_length=255)
    password2 = serializers.CharField(max_length=255)
    username = serializers.CharField(max_length=255)

    def save(self):
        """docstring"""
        user = User.objects.get(username=self.validated_data['username'])
        user.set_password(self.validated_data['password1'])
        CodigoRecuperacion.objects.filter(usuario=user).filter(activo=1).delete()
        user.save()
        return user

    def validate_password1(self,value):
        """docstring"""
        validate_password(value)
        return value

    def validate_password2(self,value):
        """docstring"""
        validate_password(value)
        return value

    def validate(self,attrs):
        """docstring"""
        if attrs['password1']!=attrs['password2']:
            raise serializers.ValidationError('Las contraseñas ingresadas no son iguales')
        return super().validate(attrs)

# class PasswordSerializer(serializers.ModelSerializer):
#     password = serializers.CharField(max_length=255)
#     password_validate = serializers.CharField(max_length=255)

#     class Meta:
#         fields = ['password','password_validate']

class CambioContraseniaSerializer(serializers.Serializer):
    old_password = serializers.CharField(max_length=128, write_only=True, required=True)
    new_password1 = serializers.CharField(max_length=128, write_only=True, required=True)
    new_password2 = serializers.CharField(max_length=128, write_only=True, required=True)

    def validate(self, data):
        password1 = data['new_password1']
        password2 = data['new_password2']
        if password1 != password2:
            raise serializers.ValidationError({
                                          'new_password2': "Las dos contraseñas ingresadas no coinciden."
                                      })
        validate_password(password1)
        validate_password(password2)
        return data

    # def save(self, **kwargs):
    #     password = self.validated_data['new_password1']
    #     user = self.context['request'].user
    #     user.set_password(password)
    #     user.save()
    #     return user

class UsuarioSistemaSerializer(serializers.ModelSerializer):
    donante = DonanteSinForeingKeySerializer()

    class Meta:
        model = User
        # fields = "__all__"
        # fields = ['id','username','first_name','last_name','email','password','groups']
        fields = ['username','first_name','last_name','email','password','groups','donante']
        # fields = ['nombre','apellido','fecha_nacimiento','dni','domicilio','localidad','provincia','pais','telefono','estado_civil','genero','ocupacion','usuario']

    def create(self, validated_data):
        print('1: ',validated_data)
        donante_data = validated_data.pop('donante', None)
        print('2: ',validated_data)
        print('3: ',donante_data)
        # username = validated_data.pop('username')
        # email = validated_data.pop('email')
        # password = validated_data.pop('password')

        # username=validated_data['username'],
        # email=validated_data['email'],
        # password=validated_data['password'],
        # first_name=validated_data['first_name'],
        # last_name=validated_data['last_name'],
        # groups=validated_data['groups']
        # print('4: ',username[0],'5: ',email[0],'6: ',password[0])
        # print('4: ',type(username[0]),'5: ',type(email[0]),'6: ',type(password[0]))
        # print('7: ',first_name[0],'8: ',last_name[0],'9: ',groups)
        # print('7: ',type(first_name[0]),'8: ',type(last_name[0]),'9: ',type(groups[0]))
        usuario = User.objects.create_user(
            username=validated_data['username'][0],
            email=validated_data['email'][0],
            password=validated_data['password'][0],
            first_name=validated_data['first_name'][0],
            last_name=validated_data['last_name'][0]
        ) 
        usuario.groups.set(validated_data['groups'])
        print('HASTA ACÁ LLEGÓ')
        try:
            for donante in donante_data:
                print('10: ',donante)
                print('10: ',type(donante))
                Donante.objects.create(usuario=usuario, **donante)
        except:
            usuario.delete()
            print('OCURRIÓ UN ERROR')
            return ''
        return 'TODO OK'#usuario


class UsuarioPruebaSerializer(serializers.ModelSerializer):
    class Meta:
        # pylint: disable=missing-class-docstring
        model = User
        fields = ['id','username','first_name','last_name','email','password','groups']
