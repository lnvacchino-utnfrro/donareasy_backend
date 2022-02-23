import binascii
import os
import datetime

from django.db import models
from django.db.models.fields import EmailField
from django.contrib.auth.models import User

"""
#* contrib.auth.model
#* Class: User
Fields:
    username: Required. char(150 Max). Puede contener alphanumeric, _, @, +, . and - characters.
    first_name: Optional. char(150 Max)
    last_name: Optional. char(150 Max)
    email: Optional. email Type (tipo de dato validado por Django)
    password: Required. (el tipo de dato es definido por Django)
    groups: integer (clave foránea de la clase Group)
    user_permission: integer (clave foránea de la clase Permission)
    is_staff: Boolean. (Designa si el usuario tiene acceso a la página de administración)
    is_active: Boolean.
    is_superuser: Boolean.
    last_login: Datetime.
    date_joined: Datetime.

#* Class: Groups
Fields:
    name: Required. 
    permissions: integer (clave foránea de la clase Permission)

#* Class: Permission
Fields:
    name: Required. char(255)
    content_type: Required. (Relacionado al django_content_type)
    codename: Required. char(100)

"""

class CodigoRecuperacion(models.Model):
    email = models.EmailField(blank=True,max_length=255,verbose_name='mail_usuario')
    codigo = models.CharField(blank=True,max_length=20,verbose_name='codigo_recuperacion')
    activo = models.BooleanField(blank=True,verbose_name='codigo_activo')
    fecha_expiracion = models.DateField(blank=True,verbose_name='fecha_expiracion')
    usuario = models.ForeignKey(User, verbose_name="id_usuario_codigo_recuperacion", on_delete=models.CASCADE, related_name='usuario_codigo_recuperacion', null=True)

    def save(self, *args, **kwargs):
        print('ENTRÓ EN EL SAVE DEL MODELO')
        print(self.email)
        print(self.usuario)
        print(self.id)
        if self.id is None:
            if self.email is None and self.usuario is None:
                return
            self.codigo = binascii.hexlify(os.urandom(10)).decode('utf-8')
            self.activo = True
            self.fecha_expiracion = datetime.datetime.now() + datetime.timedelta(days=2)
            print('PARECE QUE SE GUARDÓ')
        super().save(*args, **kwargs)

    def delete(self):
        self.activo = False
        self.save()

class paseInvitado(models.Model):
    fecha_alta = models.DateTimeField(blank=True,verbose_name='fecha_alta')
    nombre_invitado = models.CharField(blank=True,max_length=50,verbose_name='nombre_invitado')
    email_invitado = models.EmailField(blank=True,max_length=255,verbose_name='mail_invitado')
    #Usuario_invitado
    codigo_pase = models.CharField(blank=True,max_length=20,verbose_name='codigo_recuperacion')
    estado = models.IntegerField(blank=True,verbose_name='codigo_estado')
    activo = models.BooleanField(blank=True,verbose_name='pase_activo')
    usuario = models.ForeignKey(User, verbose_name=("id_usuario"), on_delete=models.CASCADE, related_name='usuario_que_invita', null=True)