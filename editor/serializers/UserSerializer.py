from rest_framework import serializers

# Model
from django.contrib.auth.models import User

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('id','username', 'email', 'first_name', 'last_name','password')
        extra_kwargs = {'password' : {'write_only' : True, 'required' : True}}
    
    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user