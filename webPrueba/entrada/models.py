from django.db import models
from django.db.models.base import Model

# Create your models here.

class Entrada(models.Model):
    titulo = models.CharField(max_length=60)
    enlace = models.CharField(max_length=200)
    valoracion = models.IntegerField(default=0)
    usuario = models.IntegerField(default=1)
    fecha_creacion = models.DateTimeField(auto_now_add=True)