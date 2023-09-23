"""Creación modelo Donación"""
from datetime import date
from operator import truediv
from pkgutil import get_data
from django.db import models
from django.db.models import Q
from django.contrib.auth.models import User
from baseApp.models import Donante, Institucion
from Recoleccion.models import Recoleccion
from django.db.models import Sum

class Donacion(models.Model):
    """
    Donación: aquel objeto que haga referencia a una donación
    tanto monetaria como de bienes. Solo permitido para rol donante
    """
    donante = models.ForeignKey(Donante,
                                on_delete=models.SET_NULL,
                                verbose_name='donante',
                                null=True
                                )
    # ForeignKey, ya que una donacion tiene un solo donante, 
    # pero el mismo donante puede haber hecho muchas donaciones.

    institucion = models.ForeignKey(Institucion,
                                    on_delete=models.SET_NULL,
                                    verbose_name='institución',
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
                                   verbose_name='descripcion',
                                   null=True)
    fecha_entrega_real = models.DateField(blank=True,
                                    verbose_name='fecha_entrega',
                                    null=True
                                    )
    #! Donacione bienes: 1:Creada , 2:Aceptada , 5:En Recoleccion , 6:Recogida , 0:Cancelada
    #! Donacion monetaria: 3:Enviada , 4:Recibida , 0:Cancelada
    cod_estado = models.SmallIntegerField(blank=True,
                                    verbose_name='cod_estado'
                                    )
    #Se agrega campo observación para que el donante pueda decir que va a donar
    observacion = models.CharField(blank=True,
                                   null=True,
                                   max_length=500,
                                   verbose_name='observacion')

    CODIGOS_ESTADO = [
        (1,'Creada'), #Bienes
        (2,'Aceptada'), #Bienes
        (3,'Enviada'), #Monetaria
        (4,'Recibida'), #Monetaria
        (5,'Entregado'), #Bienes
        (0,'Cancelada'),
    ]

    # cod_estado = models.CharField(max_length=2,
    #                         verbose_name='estado',
    #                         choices=CODIGOS_ESTADO
    #                     )

    class Meta:
        # pylint: disable=missing-class-docstring, too-few-public-methods
        ordering = ['fecha_creacion']
        verbose_name = 'Donación'
        verbose_name_plural = 'Donaciones'

    def get_donaciones(**kwargs):
        if 'tipo' in kwargs:
            if kwargs['tipo'] == 'bienes':
                result = DonacionBienes.objects.all()
            elif kwargs['tipo'] == 'monetarias':
                result = DonacionMonetaria.objects.all()
        else:
            result = Donacion.objects.all()
    
        if 'institucion' in kwargs:
            result = result.filter(institucion=kwargs['institucion'])
        if 'donante' in kwargs:
            result = result.filter(donante=kwargs['donante'])
        if 'cod_estado' in kwargs:
            result = result.filter(cod_estado=kwargs['cod_estado'])
        
        return result

    def get_cantidad_total_donaciones(**kwargs):
        cantidad = Donacion.get_donaciones(**kwargs).count()
        return cantidad

    def get_donantes(**kwargs):
        donaciones = Donacion.get_donaciones(**kwargs)
        donantes = []

        for donacion in donaciones:
            donante = donacion.donante
            if donante not in donantes:
                donantes.append(donante)
        
        return donantes

    def get_monto_total_donaciones_monetarias(**kwargs):
        donaciones = Donacion.get_donaciones(tipo='monetarias',**kwargs)
        if not donaciones:
            return 0
        total_monto = donaciones.aggregate(Sum('monto'))['monto__sum']
        return total_monto

    def get_cantidad_total_donaciones_por_bien(tipo_bien,**kwargs):
        donaciones = Donacion.get_donaciones(tipo='bienes',**kwargs)
        result = 0
        for donacion in donaciones:
            result += Bien.objects.filter(tipo=tipo_bien,donacion=donacion).count()
        return result

    def get_institucion(**kwargs):
        donaciones = Donacion.get_donaciones(**kwargs)
        instituciones = []

        for donacion in donaciones:
            institucion = donacion.institucion
            if institucion not in instituciones:
                instituciones.append(institucion)
        
        return instituciones

class DonacionMonetaria(Donacion):
    """docstring"""
    monto = models.FloatField(blank=True,
                            verbose_name='monto'
                            )
    fecha_transferencia = models.DateField(blank=True,
                                    verbose_name='fecha_transferencia'
                                    )
    comprobante_transaccion = models.FileField(
                                   blank=True,
                                   max_length=50,
                                   verbose_name='comprobante_transaccion',
                                   null=True
                                   )

    class Meta:
        # pylint: disable=missing-class-docstring, too-few-public-methods
        ordering = ['fecha_creacion']
        verbose_name = 'Donación monetaria'
        verbose_name_plural = 'Donaciones monetarias'



class DonacionBienes(Donacion):
    """docstring""" 
    fecha_retiro = models.DateField(blank=True,
                                    verbose_name='fecha_retiro',
                                    null=True
                                    )
    recoleccion = models.ForeignKey(Recoleccion,
                                on_delete=models.SET_NULL,
                                null=True,
                                related_name='donaciones'
                                )
    FORMA_ENTREGA = [ #Se mira del lado del donante
        (1,'Retirar'),
        (2,'Envio'),
        (3,'Contactar Institución')
    ]

    tipo = models.CharField(max_length=2,
                            choices=FORMA_ENTREGA
                        )

    def __str__(self):
        return str(self.donante)

    class Meta:
        # pylint: disable=missing-class-docstring, too-few-public-methods
        ordering = ['fecha_creacion']
        verbose_name = 'Donación de bienes'
        verbose_name_plural = 'Donaciones de bienes'


class Bien(models.Model):
    """Objetos que va adonar el Donante a una institucion"""
    TIPOS_BIEN = [
        (1,'alimento'),
        (2,'útil'),
        (3,'prenda'),
        (4,'otro'),
    ]

    tipo = models.CharField(max_length=2,
                            choices=TIPOS_BIEN
                        )
    # puede ser tipo alimentos, utiles, prendas u otros.
    nombre = models.CharField(blank=True,
                              max_length=100,
                              verbose_name='nombre')
    descripcion = models.CharField(blank=True,
                                   max_length=500,
                                   verbose_name='descripcion')
    cantidad = models.IntegerField(blank=True,
                                   verbose_name='cantidad')
    donacion = models.ForeignKey(DonacionBienes,
                                on_delete=models.SET_NULL,
                                null=True,
                                related_name='bienes'
                                )
    # imagen 

    class Meta:
        # pylint: disable=missing-class-docstring, too-few-public-methods
        ordering = ['tipo']
        verbose_name = 'Bien'
        verbose_name_plural = 'Bienes'

class Necesidad(models.Model):
    TIPOS_NECESIDAD = [
        (1,'alimento'),
        (2,'útil'),
        (3,'prenda'),
        (4,'otro'),
        (0,'monetaria')
    ]

    tipo = models.CharField(max_length=2,
                            choices=TIPOS_NECESIDAD
                        )
    # puede ser tipo alimentos, utiles, prendas u otros.
    titulo = models.CharField(blank=True,
                              null=True,
                              max_length=100,
                              verbose_name='titulo')
    descripcion = models.CharField(blank=True,
                                   null=True,
                                   max_length=500,
                                   verbose_name='descripcion')
    cantidad = models.IntegerField(blank=True,
                                   null=True,
                                   verbose_name='cantidad')
    fecha_alta = models.DateTimeField(blank=True,
                                    null=True,
                                    verbose_name='fecha_alta')
    fecha_vigencia = models.DateTimeField(blank=True,
                                    verbose_name='fecha_vigencia',
                                    null=True)
    fecha_baja = models.DateTimeField(blank=True,
                                    verbose_name='fecha_baja',
                                    null=True)
    institucion = models.ForeignKey(Institucion,
                                on_delete=models.SET_NULL,
                                null=True,
                                related_name='necesidad'
                                )
    isDelete = models.BooleanField(blank=True,
                                null=True,
                                verbose_name='isDelete',
                                default=False)

    def delete(self, using=None, keep_parents=False):
        """docstring"""
        self.isDelete = True
        self.save()

    class Meta:
        # pylint: disable=missing-class-docstring, too-few-public-methods
        ordering = ['fecha_alta']
        verbose_name = 'Necesidad'
        verbose_name_plural = 'Necesidades'

    def get_necesidades(**kwargs):
        result = Necesidad.objects.all()
        if 'institucion' in kwargs:
            result = result.filter(institucion=kwargs['institucion'])
        if 'tipo' in kwargs:
            result = result.filter(tipo=kwargs['tipo'])        
        return result

    def get_cantidad_total_necesidades(**kwargs):
        return Necesidad.get_necesidades(**kwargs).count()

    def get_cantidad_total_necesidades_activas(**kwargs):
        return Necesidad.get_necesidades(**kwargs).filter(isDelete=False).filter(fecha_vigencia__gte=date.today()).count()
        
    def get_cantidad_total_necesidades_inactivas(**kwargs):
        return Necesidad.get_necesidades(**kwargs).exclude(isDelete=False,fecha_vigencia__gte=date.today()).count()
    