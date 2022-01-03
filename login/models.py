from django.db import models
from django.db.models.fields import EmailField

class Donante(models.Model):
    nombre = models.CharField(blank=True,max_length=100,verbose_name='Nombre')
    apellido = models.CharField(blank=True,max_length=100,verbose_name='Apellido')
    email = models.EmailField(unique=True,max_length=100,verbose_name='Email')
    edad = models.IntegerField(null=True,blank=True)
    #owner = models.ForeignKey('auth.User', related_name='donante', on_delete=models.CASCADE, null=True)
    #highlighted = models.TextField(null=True)

    def __str__(self):
        return self.nombre

    class Meta:
        ordering = ['nombre']
        verbose_name = 'Donante'
        verbose_name_plural = 'Donantes'

    def save(self, *args, **kwargs):
        nombre = self.nombre
        apellido = self.apellido
        email = self.email
        edad = self.edad
        #self.highlighted = highlight(self.code, lexer, formatter)
        super(Donante, self).save(*args, **kwargs)
