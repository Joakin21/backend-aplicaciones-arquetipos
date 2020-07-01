from rest_framework import serializers
from .UserSerializer import UserSerializer

# Model
from ..models import ProfesionalSalud

class ProfesionalSaludSerializer(serializers.HyperlinkedModelSerializer):
    user = UserSerializer(required = True)

    class Meta:
        model = ProfesionalSalud
        fields = ('user','profesion', 'centro_salud')
