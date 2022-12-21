from django.db import models
from django.forms import ImageField
from baseApp.models import Institucion


class Chicos(models.Model):

    nombre = models.CharField(blank=True,
                              max_length=100,
                              verbose_name='nombre')
    apellido = models.CharField(blank=True,
                              max_length=100,
                              verbose_name='apellido')
    edad = models.SmallIntegerField(blank=True,
                                    verbose_name='edad')
    descripcion = models.CharField(blank=True,
                              max_length=500,
                              verbose_name='descripcion',
                              null=True)
    institucion = models.ForeignKey(Institucion,
                                on_delete=models.CASCADE,
                                verbose_name='chicos',
                                related_name='chicos'
                                )
    fotografia = models.ImageField(blank=True,
                                   verbose_name='fotografia',
                                   null=True)
    def __str__(self):
        return str(self.nombre)
        
class SolicitudApadrinamiento(models.Model):

    cod_estado = models.SmallIntegerField(blank=True,
                                    verbose_name='cod_estado'
                                    )
    #! cod_estado values = 1:Creada , 2:Aceptada , 0:Cancelada
    motivo_FS =  models.CharField(blank=True,
                                   max_length=500,
                                   verbose_name='motivo_apadrinamiento',
                                   null=True
                                   )
    fecha_creacion = models.DateTimeField(blank=True,
                                    verbose_name='fecha_creacion'  
                                    )                               
    fecha_aceptacion = models.DateTimeField(blank=True,
                                    verbose_name='fecha_aceptacion',
                                    null=True
                                    )
    fecha_cancelacion = models.DateTimeField(blank=True,
                                    verbose_name='fecha_cancelacion',
                                    null=True
                                    )
    motivo_cancelacion = models.CharField(blank=True,
                                   max_length=100,
                                   verbose_name='motivo_cancelacion',
                                   null=True
                                   )
    dni_frente = models.ImageField(blank=True,
                                   max_length=50,
                                   verbose_name='dni_frente',
                                   null=True
                                   )
    dni_dorso = models.ImageField(blank=True,
                                   max_length=50,
                                   verbose_name='dni_dorso',
                                   null=True
                                   )
    recibo_sueldo = models.FileField(
                                   blank=True,
                                   max_length=50,
                                   verbose_name='recibo_sueldo',
                                   null=True
                                   )
    acta_matrimonio = models.FileField(
                                   blank=True,
                                   max_length=50,
                                   verbose_name='acta_matrimonio',
                                   null=True
                                   )
    visita = models.BooleanField(  default=False,
                                   verbose_name='visita',
                                   null=True
                                   )
    fecha_visita = models.DateTimeField(blank=True,
                                    verbose_name='fecha_visita',
                                    null=True
                                    )
    chico_apadrinado = models.OneToOneField(Chicos,
                                   verbose_name=("chico"),
                                   on_delete=models.CASCADE,
                                   related_name='chico_apadrinado'
                                   )