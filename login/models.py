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

class Donante(models.Model):
    nombre = models.CharField(blank=True,max_length=100,verbose_name='nombre')
    apellido = models.CharField(blank=True,max_length=100,verbose_name='apellido')
    fecha_nacimiento = models.DateField(blank=True, verbose_name='fecha_nacimiento', null=True)
    dni = models.CharField(blank=True,max_length=8,verbose_name='dni', null=True) #? El dni no puede ser null
    domicilio = models.CharField(blank=True,max_length=100,verbose_name='domicilio', null=True)
    localidad = models.CharField(blank=True,max_length=100,verbose_name='ciudad', null=True)
    provincia = models.CharField(blank=True,max_length=100,verbose_name='provincia', null=True)
    pais = models.CharField(blank=True,max_length=100,verbose_name='pais', null=True)
    telefono = models.CharField(blank=True,max_length=15,verbose_name='telefono', null=True)
    estado_civil = models.CharField(blank=True,max_length=20,verbose_name='provincia', null=True)
    genero = models.CharField(blank=True,max_length=20,verbose_name='genero', null=True)
    ocupacion = models.CharField(blank=True,max_length=100,verbose_name='ocupacion', null=True)
    usuario = models.OneToOneField(User, verbose_name=("id_usuario"), on_delete=models.CASCADE, related_name='usuario_donante', null=True)

    def __str__(self):
        return self.nombre

    class Meta:
        ordering = ['nombre']
        verbose_name = 'Donante'
        verbose_name_plural = 'Donantes'

    # def save(self, *args, **kwargs):
    #     nombre = self.nombre
    #     apellido = self.apellido
    #     email = self.email
    #     edad = self.edad
    #     #self.highlighted = highlight(self.code, lexer, formatter)
    #     super(Donante, self).save(*args, **kwargs)

class Institucion(models.Model):
    nombre = models.CharField(blank=True,max_length=100,verbose_name='nombre')
    director = models.CharField(blank=True,max_length=100,verbose_name='director')
    fecha_fundacion = models.DateField(blank=True, verbose_name='fecha_fundacion', null=True)
    domicilio = models.CharField(blank=True,max_length=100,verbose_name='domicilio', null=True)
    localidad = models.CharField(blank=True,max_length=100,verbose_name='ciudad', null=True)
    provincia = models.CharField(blank=True,max_length=100,verbose_name='provincia', null=True)
    pais = models.CharField(blank=True,max_length=100,verbose_name='pais', null=True)
    telefono = models.CharField(blank=True,max_length=15,verbose_name='telefono', null=True)
    #chicos = (ver como poner acá una relación uno a muchos (una institución tiene muchos chicos))
    cant_empleados = models.SmallIntegerField(blank=True, verbose_name='cant_empleados', null=True)
    descripcion = models.CharField(blank=True,max_length=500,verbose_name='descripción',null=True)
    cbu = models.BigIntegerField(blank=True,verbose_name='CBU',null=True) #En caso de que el CBU sea null no se podrán realizar donaciones por transferencia
    cuenta_bancaria = models.CharField(blank=True,max_length=12,null=True) #! Formato cuenta bancaria: xxx-xxxxxx/x
    usuario = models.OneToOneField(User, verbose_name=("id_usuario"), on_delete=models.CASCADE, related_name='usuario_institucion', null=True)

    def __str__(self):
        return self.nombre

    class Meta:
        ordering = ['nombre']
        verbose_name = 'Institucion'
        verbose_name_plural = 'Instituciones'
