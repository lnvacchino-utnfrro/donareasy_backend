from django.db import models
from django.db.models.fields import EmailField

# Create your models here.
class Donante(models.Model):
    nombre = models.CharField(blank=True,max_length=100,verbose_name='Nombre')
    apellido = models.CharField(blank=True,max_length=100,verbose_name='Apellido')
    email = models.EmailField(unique=True,max_length=100,verbose_name='Email')
    edad = models.IntegerField(null=True,blank=True)

    def __str__(self):
        return self.nombre

    class Meta:
        ordering = ['nombre']
        verbose_name = 'Donante'
        verbose_name_plural = 'Donantes'