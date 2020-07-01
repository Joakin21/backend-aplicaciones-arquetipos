from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.decorators import api_view

from .lista_arquetipos import paciente_collection


@api_view(['GET', 'PUT', 'POST'])
def pacientesView(request, rut_paciente):
    #obtener token desde el header (front), obtener token del usuario logeado (back)
    #ejemplo token: 9e85bf9faf3d2c7de18e6fa069c795ca89e48dca
    
    is_token_valid = True
    #Se captura un error en caso de que no se envie un token o el token enviado sea incorrecto
    try:
        token_in_request = request.headers["Authorization"]
        user = Token.objects.get(key=token_in_request).user
    except:
        is_token_valid = False

    #print("Usuario valido:",is_token_valid)
    if is_token_valid:
        if request.method == 'GET':
            paciente = paciente_collection.find_one({"rut":rut_paciente})
            if(paciente):
                paciente["_id"] = str(paciente["_id"])
                respuesta = paciente#{"rut":paciente["rut"], "nombre":paciente["nombre"], "apellidos":paciente["apellidos"]}
            else:
                respuesta = {"detail": "Patient not found"}

            return Response(respuesta)

        if request.method == 'PUT':
            #print(request.data)
            request.data.pop('_id')
            result_update = paciente_collection.update_one({'rut': rut_paciente}, {'$set': request.data})
            return Response({"result": True})
        
        if request.method == 'POST':
            result_post = paciente_collection.insert_one(request.data).inserted_id
            return Response({"_id": str(result_post)})
        
    else:
        return Response({"detail": "Authentication credentials were not provided."})