from django.db import models
#from mongoengine import Document, EmbeddedDocument, fields

# Create your models here.
class usuario(models.Model):
    email = models.EmailField()
    password = models.CharField(max_length=50)
    
"""
class atribution(models.Model):
    id_arquetipo = models.TextField()
    autor = models.ListField()
    contribuidores = models.ListField()
    otros_detalles = models.ListField()

class description(models.Model):
    palabras_clave = models.ListField()
    proposito = models.TextField()
    uso = models.TextField()

class conjuntoItems(models.Model):
    #items = ListField(EmbeddedModelField('item'))
    items = models.ListField()

"""
"""
class item(models.Model):
    i = ListField()
"""