import datetime
from django.utils import timezone
from django.db import models

class Usuario (models.Model):
	nombre = models.CharField (max_length=200)
	email = models.CharField (max_length=200)
	contrasenia = models.CharField (max_length=200)
	ultima_visita = models.DateTimeField ('Ultima visita')

	def __unicode__(self):
		return self.nombre