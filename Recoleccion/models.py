from django.db import models
from django.contrib.auth.models import User
from baseApp.models import Donante, Institucion, Cadete
# Create your models here.

class Recoleccion(models.Model):
    """
    Recolección: es un conjunto de donaciones definidas por el cadete para recolectar en un día y hora
    en particular
    """
    cadete = models.ForeignKey(Cadete,
                                on_delete=models.SET_NULL,
                                null=True,
                                verbose_name='cadete'
                                )
    
    #! 1:Creada , 2:En proceso , 3:Finalizada , 4:No finalizada , 0:Cancelada
    estado_recoleccion = models.SmallIntegerField(blank = True, 
                                    verbose_name='estado'
                                    )
    fecha_cancelacion = models.DateTimeField(blank=True,
                                    verbose_name='fecha_cancelacion',
                                    null=True
                                    )
    fecha_finalizacion = models.DateTimeField(blank=True,
                                    verbose_name='fecha_finalizacion',
                                    null=True
                                    )
    motivo_cancelacion = models.CharField(blank=True,
                                   max_length=100,
                                   verbose_name='descripcion',
                                   null=True)
    hora_recoleccion = models.TimeField(blank=True,
                                   verbose_name='hora_recoleccion',
                                   null=True)
    fecha_recoleccion = models.DateField(blank=True,
                                   verbose_name='fecha_recoleccion',
                                   null=True)
    #Falta agregar el campo de Ruta, ver si necesitamos ejes de coordenadas

    class Meta:
        # pylint: disable=missing-class-docstring, too-few-public-methods
        #ordering = ['fecha_recoleccion']
        verbose_name = 'Recolección'
        verbose_name_plural = 'Recolecciones'
