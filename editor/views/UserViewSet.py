from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets

from ..models import ProfesionalSalud
from ..serializers import ProfesionalSaludSerializer



class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    """ 
    queryset = ProfesionalSalud.objects.all().order_by('-date_joined')
    serializer_class = ProfesionalSaludSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
