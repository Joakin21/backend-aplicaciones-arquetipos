from django.db import models
from django.contrib.auth.models import User

class ProfesionalSalud(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profesion = models.CharField(max_length=50)
    centro_salud = models.CharField(max_length=50)

