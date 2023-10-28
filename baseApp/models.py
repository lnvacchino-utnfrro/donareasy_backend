"""Modelos: Donante, Institucion"""
import binascii
import os

from django.db import models
from django.contrib.auth.models import User

class Donante(models.Model):
    """
    Rol de un usuario. Aquel que realiza donaciones a una o varias
    instituciones.
    """
    nombre = models.CharField(max_length=100,
                              verbose_name='nombre')
    apellido = models.CharField(max_length=100,
                                verbose_name='apellido')
    fecha_nacimiento = models.DateField(blank=True,
                                        verbose_name='fecha_nacimiento',
                                        null=True)
    dni = models.CharField(blank=True,  #? El dni no puede ser null
                           max_length=8,
                           verbose_name='dni',
                           null=True)
    domicilio = models.CharField(blank=True,
                                 max_length=100,
                                 verbose_name='domicilio',
                                 null=True)
    localidad = models.CharField(blank=True,
                                 max_length=100,
                                 verbose_name='ciudad',
                                 null=True)
    provincia = models.CharField(blank=True,
                                 max_length=100,
                                 verbose_name='provincia',
                                 null=True)
    pais = models.CharField(blank=True,
                            max_length=100,
                            verbose_name='pais',
                            null=True)
    telefono = models.CharField(blank=True,
                                max_length=15,
                                verbose_name='telefono',
                                null=True)
    estado_civil = models.CharField(blank=True,
                                    max_length=20,
                                    verbose_name='provincia',
                                    null=True)
    genero = models.CharField(blank=True,
                              max_length=20,
                              verbose_name='genero',
                              null=True)
    ocupacion = models.CharField(blank=True,
                                 max_length=100,
                                 verbose_name='ocupacion',
                                 null=True)
    usuario = models.OneToOneField(User,
                                   verbose_name=("id_usuario"),
                                   on_delete=models.CASCADE,
                                   related_name='usuario_donante',
                                   null=True)

    def __str__(self):
        return str(self.nombre)

    def __eq__(self, other):
        return self.nombre == other.nombre \
            and self.apellido == other.apellido \
            and self.fecha_nacimiento == other.fecha_nacimiento \
            and self.dni == other.dni \
            and self.domicilio == other.domicilio \
            and self.localidad == other.localidad \
            and self.provincia == other.provincia \
            and self.pais == other.pais \
            and self.telefono == other.telefono \
            and self.estado_civil == other.estado_civil \
            and self.genero == other.genero \
            and self.ocupacion == other.ocupacion \
            and self.usuario == other.usuario

    class Meta:
        # pylint: disable=missing-class-docstring, too-few-public-methods
        ordering = ['nombre']
        verbose_name = 'Donante'
        verbose_name_plural = 'Donantes'

class Institucion(models.Model):
    """
    Rol de un usuario. Aquel que gestiona la recepción de donaciones de parte
    de uno o varios donantes, controla el apadrinamiento de chicos y publica
    noticias en el sistema.
    """
    nombre = models.CharField(blank=True,
                              max_length=100,
                              verbose_name='nombre')
    director = models.CharField(blank=True,
                                max_length=100,
                                verbose_name='director')
    fecha_fundacion = models.DateField(blank=True,
                                       verbose_name='fecha_fundacion',
                                       null=True)
    domicilio = models.CharField(blank=True,
                                 max_length=100,
                                 verbose_name='domicilio',
                                 null=True)
    localidad = models.CharField(blank=True,
                                 max_length=100,
                                 verbose_name='ciudad',
                                 null=True)
    provincia = models.CharField(blank=True,
                                 max_length=100,
                                 verbose_name='provincia',
                                 null=True)
    pais = models.CharField(blank=True,
                            max_length=100,
                            verbose_name='pais',
                            null=True)
    telefono = models.CharField(blank=True,
                                max_length=15,
                                verbose_name='telefono',
                                null=True)
    cant_empleados = models.SmallIntegerField(blank=True,
                                              verbose_name='cant_empleados',
                                              null=True)
    descripcion = models.CharField(blank=True,
                                   max_length=500,
                                   verbose_name='descripción',
                                   null=True)
    #En caso de que el CBU sea null no se podrán realizar donaciones por transferencia
    cbu = models.CharField(blank=True,
                                max_length=50,
                                 verbose_name='CBU',
                                 null=True)

    usuario = models.OneToOneField(User,
                                   verbose_name=("id_usuario"),
                                   on_delete=models.CASCADE,
                                   related_name='usuario_institucion',
                                   null=True)

    habilitado = models.BooleanField(null=False,
                                    verbose_name='institucion_habilitada',
                                    default=False)

    codigo_habilitacion = models.CharField(blank=True,
                                           max_length=20,
                                           verbose_name='codigo_habilitacion')

    def __str__(self):
        return str(self.nombre)
    
    def save(self, *args, **kwargs):
        # Verifica si la instancia tiene una clave primaria
        if not self.id:
            # Si no tiene clave primaria, es una nueva instancia
            self.codigo_habilitacion = binascii.hexlify(os.urandom(10)).decode('utf-8')
        super().save(*args, **kwargs)

    def instituciones_habilitadas():
        return Institucion.objects.filter(habilitado=True)

    class Meta:
        # pylint: disable=missing-class-docstring, too-few-public-methods
        ordering = ['nombre']
        verbose_name = 'Institucion'
        verbose_name_plural = 'Instituciones'


class Cadete(models.Model):
    """
    Rol de un usuario. Aquel que realiza la recolección de los donativos.
    """
    nombre = models.CharField(max_length=100,
                              verbose_name='nombre')
    apellido = models.CharField(max_length=100,
                                verbose_name='apellido')
    fecha_nacimiento = models.DateField(blank=True,
                                        verbose_name='fecha_nacimiento',
                                        null=True)
    dni = models.CharField(blank=True,  #? El dni no puede ser null
                           max_length=8,
                           verbose_name='dni',
                           null=True)
    domicilio = models.CharField(blank=True,
                                 max_length=100,
                                 verbose_name='domicilio',
                                 null=True)
    localidad = models.CharField(blank=True,
                                 max_length=100,
                                 verbose_name='ciudad',
                                 null=True)
    provincia = models.CharField(blank=True,
                                 max_length=100,
                                 verbose_name='provincia',
                                 null=True)
    pais = models.CharField(blank=True,
                            max_length=100,
                            verbose_name='pais',
                            null=True)
    telefono = models.CharField(blank=True,
                                max_length=15,
                                verbose_name='telefono',
                                null=True)
    estado_civil = models.CharField(blank=True,
                                    max_length=20,
                                    verbose_name='provincia',
                                    null=True)
    genero = models.CharField(blank=True,
                              max_length=20,
                              verbose_name='genero',
                              null=True)
    ocupacion = models.CharField(blank=True,
                                 max_length=100,
                                 verbose_name='ocupacion',
                                 null=True)
    medio_transporte = models.CharField(blank=True,
                                        max_length=100,
                                        verbose_name='medio-de-transporte',
                                        null=True)
    usuario = models.OneToOneField(User,
                                   verbose_name=("id_usuario"),
                                   on_delete=models.CASCADE,
                                   related_name='usuario_cadete',
                                   null=True)
    institucion = models.ForeignKey(Institucion,
                                on_delete=models.SET_NULL,
                                verbose_name='institucion',
                                null=True)

    def __str__(self):
        return str(self.nombre)

    def __eq__(self, other):
        return self.nombre == other.nombre \
            and self.apellido == other.apellido \
            and self.fecha_nacimiento == other.fecha_nacimiento \
            and self.dni == other.dni \
            and self.domicilio == other.domicilio \
            and self.localidad == other.localidad \
            and self.provincia == other.provincia \
            and self.pais == other.pais \
            and self.telefono == other.telefono \
            and self.estado_civil == other.estado_civil \
            and self.genero == other.genero \
            and self.ocupacion == other.ocupacion \
            and self.medio_transporte == other.medio_transporte \
            and self.usuario == other.usuario

    class Meta:
        # pylint: disable=missing-class-docstring, too-few-public-methods
        ordering = ['nombre']
        verbose_name = 'Cadete'
        verbose_name_plural = 'Cadetes'

