from django.db import models

from django.contrib.auth.models import User

from baseApp.models import Institucion


class Etiqueta(models.Model):
	"""
	Etiquetas o tags: palabras claves para clasificar o identificar varias
	noticias
	"""
	nombre = models.CharField(max_length=50,
							  verbose_name='etiqueta')

	class Meta:
        # pylint: disable=missing-class-docstring, too-few-public-methods
		ordering = ['id']
		verbose_name = 'Etiqueta'
		verbose_name_plural = 'Etiquetas'


class Reaccion(models.Model):
	"""
	Forma de expresar emocionalmente la reacción del usuario sobre una noticia
	o comentario
	"""
	descripcion = models.CharField(max_length=50,
								  verbose_name='reaccion')

	class Meta:
        # pylint: disable=missing-class-docstring, too-few-public-methods
		ordering = ['id']
		verbose_name = 'Reaccion'
		verbose_name_plural = 'Reacciones'


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
	etiquetas = models.ManyToManyField(Etiqueta,
									   verbose_name='etiquetas_noticia')
	reacciones = models.ManyToManyField(Reaccion,
										verbose_name='reacciones_noticias')
	# imagen o imagenes

	class Meta:
        # pylint: disable=missing-class-docstring, too-few-public-methods
		ordering = ['institucion','fecha_publicacion']
		verbose_name = 'Noticia'
		verbose_name_plural = 'Noticias'


class ComentarioPublicacion(models.Model):
	"""
	Comentario realizado por un usuario del sistema y que se encuentra dirigido
	a una noticia o a otro comentario
	"""
	texto_comentario = models.CharField(max_length=500,
										verbose_name='comentario')
	fecha_publicacion = models.DateTimeField(blank=True,
											 verbose_name='fecha_publicacion',
											 null=True)
	usuario = models.ForeignKey(User,
                                on_delete=models.SET_NULL,
                                verbose_name='usuario_publicacion',
								related_name='usuario_publicacion',
                                null=True)
	noticia = models.ForeignKey(Noticia,
								on_delete=models.CASCADE,
								verbose_name='noticia_comentario',
								related_name='noticia_comentario',
								null=True)
	comentario_dirigido = models.ForeignKey('self', 
											on_delete=models.CASCADE,
											related_name='comentario_comentario',
											null=True)
	reacciones = models.ManyToManyField(Reaccion,
										verbose_name='reacciones_comentario',
										related_name='reacciones_comentario')

	class Meta:
        # pylint: disable=missing-class-docstring, too-few-public-methods
		ordering = ['noticia','fecha_publicacion']
		verbose_name = 'Comentario'
		verbose_name_plural = 'Comentarios'

