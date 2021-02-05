#from django.db import models
from django.contrib.auth.models import User
from djongo import models
from django import forms

class Arquetipo(models.Model):
    _id = models.CharField(max_length=100)
    nombre = models.CharField(max_length=100)
    tipo_arquetipo = models.CharField(max_length=30)
    class Meta:
        abstract = True

class ArquetipoForm(forms.ModelForm):
    class Meta:
        model = Arquetipo
        fields = ('_id', 'nombre', 'tipo_arquetipo',)


class ListaArquetipos(models.Model):
    nombre_lista = models.CharField(max_length=200)#nom lista
    arquetipos = models.ArrayField(
        model_container=Arquetipo,
        model_form_class=ArquetipoForm
    )
    idioma = models.CharField(max_length=50)
    
    class Meta:
        abstract = True
    objects = models.DjongoManager()

class ListaArquetiposForm(forms.ModelForm):
    class Meta:
        model = ListaArquetipos
        fields = ('nombre_lista', 'arquetipos', 'idioma')

#------------------------------------------------------------------

class UltimosPacientesAtendidos(models.Model):
    rut = models.CharField(max_length=50)
    fecha = models.CharField(max_length=50)
    class Meta:
        abstract = True
    objects = models.DjongoManager()

class UltimosPacientesAtendidosForm(forms.ModelForm):
    class Meta:
        model = UltimosPacientesAtendidos
        fields = ('rut','fecha',)


class ProfesionalSalud(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profesion = models.CharField(max_length=50)
    centro_salud = models.CharField(max_length=50)

    listas_arquetipos = models.ArrayField(
        model_container=ListaArquetipos,
        model_form_class=ListaArquetiposForm
    )
    ultimos_pacientes_atendidos = models.ArrayField(
        model_container=UltimosPacientesAtendidos,
        model_form_class=UltimosPacientesAtendidosForm
    )

    objects = models.DjongoManager()
   

