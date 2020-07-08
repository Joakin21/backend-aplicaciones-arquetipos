from django.shortcuts import render

from rest_framework.decorators import api_view
from rest_framework import generics
from rest_framework.response import Response

#-------------------------para el login-------------------------------------
from django.contrib.auth.models import User
from editor.models import ProfesionalSalud

from rest_framework import viewsets
from rest_framework import permissions

from editor.serializers import UserSerializer
from editor.serializers import ProfesionalSaludSerializer

from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token

from cryptography.fernet import Fernet
#---------------------------------------------------------------------------

from editor.fileXmlManager import procesarXML
from pymongo import MongoClient
from bson.objectid import ObjectId
import pprint

client = MongoClient()
db = client['proyecto4']
arq_collection = db["arquetipos"]#db["arquetipos_es"]
paciente_collection = db["historial_paciente"]

key_test = "QJhfUw_LWLPe6uEbDd808C9eUeOxUBQfj5a4ln6o8UU=".encode()
algoritmo = Fernet(key_test)

def procesar(dato, accion):
	global algoritmo
	if accion == "encriptar":
		return algoritmo.encrypt(dato.encode("utf-8"))
	if accion == "desencriptar":
		return algoritmo.decrypt(dato).decode("utf-8")
	return dato

#Encriptacion  de prueba
def encriptar_or_desencriptar(historial_clinico, accion):
	"""key_test = "QJhfUw_LWLPe6uEbDd808C9eUeOxUBQfj5a4ln6o8UU=".encode()
				algoritmo = Fernet(key_test)"""
	global key_test
	global algoritmo


	historial_clinico["nombre"] = procesar(historial_clinico["nombre"], accion)#algoritmo.encrypt(historial_clinico["nombre"].encode("utf-8"))
	historial_clinico["apellidos"] = procesar(historial_clinico["apellidos"], accion)
	#historial_clinico["rut"] = procesar(historial_clinico["rut"], accion)
	historial_clinico["direccion"] = procesar(historial_clinico["direccion"], accion)
	historial_clinico["fecha_nacimiento"] = procesar(historial_clinico["fecha_nacimiento"], accion)
	historial_clinico["ciudad"] = procesar(historial_clinico["ciudad"], accion)

	"""for i in range(len(historial_clinico["profesionales_que_atendieron"])):
		if accion == "encriptar":
			historial_clinico["profesionales_que_atendieron"][i] = procesar(str(historial_clinico["profesionales_que_atendieron"][i]), accion)
		if accion == "desencriptar":
			historial_clinico["profesionales_que_atendieron"][i] = procesar(historial_clinico["profesionales_que_atendieron"][i], accion)
    """
	for i in range(len(historial_clinico["sesiones_medica"])):
		historial_clinico["sesiones_medica"][i]["nombre_sesion"] = procesar(historial_clinico["sesiones_medica"][i]["nombre_sesion"], accion)
		historial_clinico["sesiones_medica"][i]["fecha"] = procesar(historial_clinico["sesiones_medica"][i]["fecha"], accion)
		historial_clinico["sesiones_medica"][i]["nombre_profesional"] = procesar(historial_clinico["sesiones_medica"][i]["nombre_profesional"], accion)
		historial_clinico["sesiones_medica"][i]["profesion"] = procesar(historial_clinico["sesiones_medica"][i]["profesion"], accion)
		historial_clinico["sesiones_medica"][i]["centro_salud"] = procesar(historial_clinico["sesiones_medica"][i]["centro_salud"], accion)
		#Arquetipos:
		for j in range(len(historial_clinico["sesiones_medica"][i]["arquetipos"])):
			for k in range(len(historial_clinico["sesiones_medica"][i]["arquetipos"][j])):
				#print(historial_clinico["sesiones_medica"][i]["arquetipos"][j][k]["clave"])
				if accion == "encriptar":
					historial_clinico["sesiones_medica"][i]["arquetipos"][j][k]["tipo"] = procesar(str(historial_clinico["sesiones_medica"][i]["arquetipos"][j][k]["tipo"]), accion)
				if accion == "desencriptar":
					historial_clinico["sesiones_medica"][i]["arquetipos"][j][k]["tipo"] = procesar(historial_clinico["sesiones_medica"][i]["arquetipos"][j][k]["tipo"], accion)

				historial_clinico["sesiones_medica"][i]["arquetipos"][j][k]["clave"] = procesar(historial_clinico["sesiones_medica"][i]["arquetipos"][j][k]["clave"], accion)
				historial_clinico["sesiones_medica"][i]["arquetipos"][j][k]["valor"] = procesar(historial_clinico["sesiones_medica"][i]["arquetipos"][j][k]["valor"], accion)

	return historial_clinico

def listaArquetipos():
    aArquetipos = []
    arquetipo = {}
    for arq in arq_collection.find():
        arq["_id"] = str(arq["_id"])
        arquetipo["id"] = arq["_id"]
        arquetipo["nombre"] = arq["text"]
        arquetipo["tipo_arquetipo"] = arq["tipo_arquetipo"]
        aArquetipos.append(arquetipo)
        arquetipo = {}
    return aArquetipos

@api_view(['PUT'])
def configurarDataBaseView(request):
    #print(idioma) 
    idioma_seteado = True
    idioma = request.data["idioma"]
    #print(idioma)
    global arq_collection
    if idioma == "es":
        arq_collection = db["arquetipos_es"]
    elif idioma == "en":
        arq_collection = db["arquetipos"]
    else:
        idioma_seteado = False

    return Response({"idioma_seteado": idioma_seteado})

@api_view(['GET', 'POST', 'DELETE'])
def paraListaArquetipos(request):
    if request.method == 'POST':
        tipo_archivo = list(request.FILES.keys())[0]
        if tipo_archivo == "xml":
            #intente procesar un xml
            archivoProcesado = procesarXML(arq_collection,request.FILES["xml"])
            return Response(archivoProcesado)
        else: #si o si es un adl"""
            return Response({"respuestra":True})

    if request.method == 'GET':
        #obtenerArquetipo()
        return Response(listaArquetipos())

    if request.method == 'DELETE':
        arq_collection.delete_many({})

        return Response({"eliminar":True})

"""@api_view(['GET'])
def obtenerUsuarioLogeado(request, token):
    if request.method == 'GET':
        user = Token.objects.get(key=token).user
        print (user)
        return Response({"respuestra":True})"""
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
                print(paciente)
                paciente["_id"] = str(paciente["_id"])
                #paciente["nombre"] = procesar(paciente["nombre"], "desencriptar")
                paciente["nombre"] = procesar(paciente["nombre"], "desencriptar")
                paciente["apellidos"] = procesar(paciente["apellidos"], "desencriptar")
                #paciente["rut"] = procesar(paciente["rut"], "desencriptar")
                lista_pacientes.append(paciente)
                #print(paciente)
            
            return Response({"pacientes_atendidos":lista_pacientes})
    else:
        return Response({"detail": "Authentication credentials were not provided."})

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
            paciente = encriptar_or_desencriptar(paciente, "desencriptar")
            if(paciente):
                paciente["_id"] = str(paciente["_id"])
                respuesta = paciente#{"rut":paciente["rut"], "nombre":paciente["nombre"], "apellidos":paciente["apellidos"]}
            else:
                respuesta = {"detail": "Patient not found"}

            return Response(respuesta)

        if request.method == 'PUT':
            request.data.pop('_id')
            historial_clinico = encriptar_or_desencriptar(request.data, "encriptar")
            #print(historial_clinico)
            result_update = paciente_collection.update_one({'rut': rut_paciente}, {'$set': historial_clinico})
            return Response({"result": True})
        
        if request.method == 'POST':
            #print(request.data)
            historial_clinico = encriptar_or_desencriptar(request.data, "encriptar")
            #print(historial_clinico)
            result_post = paciente_collection.insert_one(historial_clinico).inserted_id
            return Response({"_id": str(result_post)})
        
    else:
        return Response({"detail": "Authentication credentials were not provided."})

@api_view(['GET', 'POST', 'PUT', 'DELETE'])
def paraEditorArquetipos(request, question_id):
    if request.method == 'GET':
        try:
            arquetipoSolicitado = arq_collection.find_one({"_id": ObjectId(question_id)})
            arquetipoSolicitado["_id"]= str(arquetipoSolicitado["_id"])
        except:
            arquetipoSolicitado = arq_collection.find_one({"_id": question_id})
            arquetipoSolicitado["_id"]= str(arquetipoSolicitado["_id"])

        return Response(arquetipoSolicitado)

    if request.method == 'POST':
        result_post = arq_collection.insert_one(request.data).inserted_id
        return Response({"_id": str(result_post)})
        
    if request.method == 'PUT':
        request.data.pop('_id')
        result_update = arq_collection.update_one({'_id': ObjectId(question_id)}, {'$set': request.data})
        return Response({"result": True})
    
    if request.method == 'DELETE':
        try:
            eliminar_arquetipo = arq_collection.remove({'_id':ObjectId(question_id)})
        except:
            eliminar_arquetipo = arq_collection.remove({'_id':question_id})
        if eliminar_arquetipo['n'] == 0: #no lo pudo elinar
            arq_collection.remove({'_id':question_id})

        return Response({"eliminar":True})

#----------------------------------------------------------------------------------------
#Para el login de usuarios
#----------------------------------------------------------------------------------------
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
