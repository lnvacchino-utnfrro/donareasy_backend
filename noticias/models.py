from django.db import models

from django.contrib.auth.models import User

from baseApp.models import Institucion


class Tag(models.Model):
	""""docstnring"""
	nombre = models.CharField(max_length=50,
							  verbose_name='nombre')


class Noticia(models.Model):
	"""
	Noticia publicada por una institución para compartirla con los demás
	usuarios de la aplicación
	"""
	# TITULO - DESCRIPCION - IMAGEN- AUTORES - INSTITUCION - USUARIO - 
	# ETIQUETA - FECHA PUBLICACION - ¿CANT VISTAS?
	titulo = models.CharField(max_length=100,
                              verbose_name='titulo')
	descripcion = models.CharField(max_length=500,
								  verbose_name='descripcion')
	fecha_publicacion = models.DateTimeField(blank=True,
											 verbose_name='fecha_publicacion',
											 null=True)
	autores = models.CharField(max_length=250,
							   verbose_name='autores')
	institucion = models.ForeignKey(Institucion,
                                on_delete=models.SET_NULL,
                                verbose_name='institucion_publicacion',
                                null=True)
	usuario = models.ForeignKey(User,
                                on_delete=models.SET_NULL,
                                verbose_name='usuario_publicacion',
                                null=True)
	tags = models.ForeignKey(Tag,
                            on_delete=models.SET_NULL,
                            verbose_name='tag_publicacion',
                            null=True)
	# imagen o imagenes


class ComentarioPublicacion(models.Model):
	"""dostring"""
	comentario = models.CharField(max_length=500,
								  verbose_name='comentario')
	fecha_publicacion = models.DateTimeField(blank=True,
											 verbose_name='fecha_publicacion',
											 null=True)
	usuario = models.ForeignKey(User,
                                on_delete=models.SET_NULL,
                                verbose_name='usuario_publicacion',
                                null=True)
	

