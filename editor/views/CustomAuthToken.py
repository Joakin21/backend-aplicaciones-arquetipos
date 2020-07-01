from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken

from ..models import ProfesionalSalud

class CustomAuthToken(ObtainAuthToken):
    
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                        context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        #solu: retornar el id del profesional relacionado a ese usuario
        #obtenemos el profesional
        profesional = ProfesionalSalud.objects.get(user_id=user.pk)
        print (profesional.id)

        return Response({
            'token': token.key,
            'user_id': profesional.id,#user.pk,
            'usurname': user.username
        })