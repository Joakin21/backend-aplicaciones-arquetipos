from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.decorators import api_view

from .lista_arquetipos import paciente_collection

@api_view(['GET'])
def pacientesAtendidosView(request, usuario):
    is_token_valid = True
    #Se captura un error en caso de que no se envie un token o el token enviado sea incorrecto
    try:
        token_in_request = request.headers["Authorization"]
        user = Token.objects.get(key=token_in_request).user
    except:
        is_token_valid = False
    if is_token_valid:
        if request.method == 'GET':
            
            pacientes_atendidos = paciente_collection.find({ "profesionales_que_atendieron":int(usuario) }, { "nombre":1, "apellidos":1, "rut":1 })
            lista_pacientes = []
            for paciente in pacientes_atendidos:
                paciente["_id"] = str(paciente["_id"])
                lista_pacientes.append(paciente)
                #print(paciente)
            
            return Response({"pacientes_atendidos":lista_pacientes})
    else:
        return Response({"detail": "Authentication credentials were not provided."})
