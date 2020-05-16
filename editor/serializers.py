#from django.contrib.auth.models import User
from rest_framework import serializers

from editor.models import usuario

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = usuario
        fields = ['id','email', 'password']
