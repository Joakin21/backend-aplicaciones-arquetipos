from django.contrib.auth.models import User
from rest_framework import serializers

from editor.models import ProfesionalSalud

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('id','username', 'email', 'first_name', 'last_name','password')
        extra_kwargs = {'password' : {'write_only' : True, 'required' : True}}
    
    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

#serializer para el perfil de usuario
class ProfesionalSaludSerializer(serializers.HyperlinkedModelSerializer):
    user = UserSerializer(required = True)

    class Meta:
        model = ProfesionalSalud
        fields = ('user','profesion', 'centro_salud')
