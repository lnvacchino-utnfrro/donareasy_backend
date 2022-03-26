#Creación modelo Donación, 
from operator import truediv
from pkgutil import get_data
from django.db import models
from django.contrib.auth.models import User
from baseApp.models import Donante, Institucion

# Create your models here.

class Donacion(models.Model):
    """
    Donación: aquel objeto que haga referencia a una donación
    tanto monetaria como de bienes. Solo permitido para rol donante
    """
    donante = models.ForeignKey(Donante,
                                models.SET_NULL,
                                on_delete=models.CASCADE,
                                verbose_name='donante'
                                )
    # ForeignKey, ya que una donacion tiene un solo donante, 
    # pero el mismo donante puede haber hecho muchas donaciones.

    institucion = models.ForeignKey(Institucion,
                                    models.SET_NULL,
                                    on_delete=models.CASCADE,
                                    verbose_name='institución'
                                    )
    fecha_creacion = models.DateField(blank=True,
                                    verbose_name='fecha_creacion'
                                    )
    fecha_aceptacion = models.DateField(blank=True,
                                    verbose_name='fecha_aceptacion'
                                    )
    fecha_entrega_real = models.DateField(blank=True,
                                    verbose_name='fecha_entrega',
                                    null=True
                                    )
    cod_estado = models.SmallIntegerField(blank = True, #! 1:Creada , 2:Aceptada , 3:Enviada , 4:Recibida , 0:Cancelada
                                    verbose_name='estado'
                                    ) 
    
class DonacionMonetaria(Donacion):
    monto = models.FloatField(blank=True,
                            verbose_name='monto'
                            )
    fecha_transferencia = models.DateField(blank=True,
                                    verbose_name='fecha_transferencia'
                                    )

class DonacionBienes(Donacion):
    tipo = models.CharField(blank=True,
                            verbose_name='tipo'
                            ) 
    #puede ser tipo alimentos, utiles, prendas u otros.
    
    fecha_retiro = models.DateField(blank=True,
                                    verbose_name='fecha_retiro',
                                    null=True
                                    )
