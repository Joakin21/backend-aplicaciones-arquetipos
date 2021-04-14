from django.shortcuts import render

from rest_framework.decorators import api_view
from rest_framework import generics
from rest_framework.response import Response

from django.contrib.auth.models import User
from editor.models import ProfesionalSalud
from editor.models import ListaArquetipos
from editor.models import Arquetipo
from editor.models import UltimosPacientesAtendidos

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

from editor.fileXmlManager import procesarXML
from pymongo import MongoClient
from bson.objectid import ObjectId
import pprint

from datetime import datetime

client = MongoClient()
db = client['proyecto4']

paciente_collection = db["historial_paciente"]
profesionales_salud_collection = db["editor_profesionalsalud"]

language_collection = db["application_language"]
lang = language_collection.find_one({})

if lang['language'] == 'es':
    arq_collection = db["arquetipos_es"]
else:
    arq_collection = db["arquetipos"]  

key_test = "QJhfUw_LWLPe6uEbDd808C9eUeOxUBQfj5a4ln6o8UU=".encode()
algoritmo = Fernet(key_test)


def procesar(dato, accion):
    global algoritmo
    if accion == "encriptar":
        return algoritmo.encrypt(dato.encode("utf-8"))
    if accion == "desencriptar":
        return algoritmo.decrypt(dato).decode("utf-8")
    return dato


def encriptar_or_desencriptar(historial_clinico, accion):

    global key_test
    global algoritmo

    historial_clinico["nombre"] = procesar(historial_clinico["nombre"], accion)
    historial_clinico["apellidos"] = procesar(
        historial_clinico["apellidos"], accion)
    #historial_clinico["rut"] = procesar(historial_clinico["rut"], accion)
    historial_clinico["direccion"] = procesar(
        historial_clinico["direccion"], accion)
    historial_clinico["fecha_nacimiento"] = procesar(
        historial_clinico["fecha_nacimiento"], accion)
    historial_clinico["ciudad"] = procesar(historial_clinico["ciudad"], accion)

    for i in range(len(historial_clinico["sesiones_medica"])):
        historial_clinico["sesiones_medica"][i]["nombre_sesion"] = procesar(
            historial_clinico["sesiones_medica"][i]["nombre_sesion"], accion)
        historial_clinico["sesiones_medica"][i]["fecha"] = procesar(
            historial_clinico["sesiones_medica"][i]["fecha"], accion)
        historial_clinico["sesiones_medica"][i]["nombre_profesional"] = procesar(
            historial_clinico["sesiones_medica"][i]["nombre_profesional"], accion)
        historial_clinico["sesiones_medica"][i]["profesion"] = procesar(
            historial_clinico["sesiones_medica"][i]["profesion"], accion)
        historial_clinico["sesiones_medica"][i]["centro_salud"] = procesar(
            historial_clinico["sesiones_medica"][i]["centro_salud"], accion)
        if accion == "encriptar":
            historial_clinico["sesiones_medica"][i]["user_id"] = procesar(
                str(historial_clinico["sesiones_medica"][i]["user_id"]), accion)
        else:
            historial_clinico["sesiones_medica"][i]["user_id"] = procesar(
                historial_clinico["sesiones_medica"][i]["user_id"], accion)
        # Arquetipos:
        for j in range(len(historial_clinico["sesiones_medica"][i]["arquetipos"])):
            for k in range(len(historial_clinico["sesiones_medica"][i]["arquetipos"][j])):
                if accion == "encriptar":
                    historial_clinico["sesiones_medica"][i]["arquetipos"][j][k]["tipo"] = procesar(
                        str(historial_clinico["sesiones_medica"][i]["arquetipos"][j][k]["tipo"]), accion)
                if accion == "desencriptar":
                    historial_clinico["sesiones_medica"][i]["arquetipos"][j][k]["tipo"] = procesar(
                        historial_clinico["sesiones_medica"][i]["arquetipos"][j][k]["tipo"], accion)

                historial_clinico["sesiones_medica"][i]["arquetipos"][j][k]["clave"] = procesar(
                    historial_clinico["sesiones_medica"][i]["arquetipos"][j][k]["clave"], accion)
                historial_clinico["sesiones_medica"][i]["arquetipos"][j][k]["valor"] = procesar(
                    historial_clinico["sesiones_medica"][i]["arquetipos"][j][k]["valor"], accion)

    return historial_clinico

# Se captura un error en caso de que no se envie un token o el token enviado sea incorrecto
def tokenDeSesionValido(autorizacion):
    is_token_valid = True
    try:
        user = Token.objects.get(key=autorizacion).user
    except:
        is_token_valid = False 
    return is_token_valid

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


def desencriptarListaDePacientes(pacientes):
    pacientes_desencriptados = []
    for paciente in pacientes:
        paciente["_id"] = str(paciente["_id"])
        paciente["nombre"] = procesar(paciente["nombre"], "desencriptar")
        paciente["apellidos"] = procesar(paciente["apellidos"], "desencriptar")
        #paciente["rut"] = procesar(paciente["rut"], "desencriptar")
        paciente["direccion"] = procesar(paciente["direccion"], "desencriptar")
        paciente["fecha_nacimiento"] = procesar(
            paciente["fecha_nacimiento"], "desencriptar")
        paciente["ciudad"] = procesar(paciente["ciudad"], "desencriptar")
        pacientes_desencriptados.append(paciente)
    return pacientes_desencriptados

def getPatients(skip):
    pacientes = paciente_collection.find({}, {"nombre": 1, "apellidos": 1, "rut": 1, "direccion": 1, "fecha_nacimiento": 1, "ciudad": 1}).skip(skip).limit(10)
    pacientes_desencriptados = desencriptarListaDePacientes(pacientes)
    return pacientes_desencriptados

@api_view(['GET', 'PUT'])
def languageConfigurationView(request):
    if request.method == 'GET':
        lang = language_collection.find_one({})
        return Response({"language": lang["language"]})

    if request.method == 'PUT':
        new_lang = request.data
        update_lang = language_collection.update_one({}, {'$set': new_lang})
        global arq_collection
        if new_lang['language'] == "es":
            arq_collection = db["arquetipos_es"]
        else: #Arquetipos en ingles
            arq_collection = db["arquetipos"]
        #arq_collection = db["arquetipos"]  # db["arquetipos_es"]
        return Response({"result": True})


@api_view(['GET', 'POST', 'DELETE'])
def paraListaArquetipos(request):
    if request.method == 'POST':
        tipo_archivo = list(request.FILES.keys())[0]
        if tipo_archivo == "xml":
            # intente procesar un xml
            archivoProcesado = procesarXML(
                arq_collection, request.FILES["xml"])
            return Response(archivoProcesado)
        else:  # si o si es un adl"""
            return Response({"respuestra": True})

    if request.method == 'GET':
        # obtenerArquetipo()
        return Response(listaArquetipos())

    if request.method == 'DELETE':
        arq_collection.delete_many({})

        return Response({"eliminar": True})

# Api view para trabajar sobre los pacientes, no se necesita especificar id
@api_view(['GET', 'POST'])
def pacientesView(request):
    if not tokenDeSesionValido(request.headers["Authorization"]):
        return Response({"detail": "Authentication credentials were not provided."})
    
    if request.method == 'GET':

        return Response(getPatients(0))

    if request.method == 'POST':
        """
        # verificamos si el paciente ya existe:
        patient_exists = paciente_collection.find_one(
            {"rut": request.data["rut"]})
        # insertamos paciente si no existe
        if patient_exists == None:
            historial_clinico = encriptar_or_desencriptar(
                request.data, "encriptar")
            result_post = paciente_collection.insert_one(
                historial_clinico).inserted_id
            return Response({"_id": str(result_post)})
        else:
            return Response({"detail": "Patient rut already exists"})
        """
        historial_clinico = encriptar_or_desencriptar(request.data, "encriptar")
        result_post = paciente_collection.insert_one(historial_clinico).inserted_id
        return Response({"_id": str(result_post)})



@api_view(['POST'])
def getSkipPatientsView(request, skip):
    if request.method == 'POST':
        return Response(getPatients(int(skip)))

@api_view(['GET'])
def getAmountDocuments(request, collection_name):
    if request.method == 'GET':
        amount_documents = 0
        if collection_name == "historial_paciente":
            amount_documents = paciente_collection.count({})
        elif collection_name == "editor_profesionalsalud":
            amount_documents = profesionales_salud_collection.count({})
        return Response({"amount_documents" : amount_documents})

# Api view para trabajar sobre un paciente especifico
@api_view(['GET', 'PUT', 'DELETE']) 
def pacienteEspecificoView(request, rut_paciente):
    if not tokenDeSesionValido(request.headers["Authorization"]):
        return Response({"detail": "Authentication credentials were not provided."})

    if request.method == 'GET':
        paciente = paciente_collection.find_one({"rut": rut_paciente})
        paciente = encriptar_or_desencriptar(paciente, "desencriptar")
        if(paciente):
            paciente["_id"] = str(paciente["_id"])
            respuesta = paciente
        else:
            respuesta = {"detail": "Patient not found"}

        return Response(respuesta)

    if request.method == 'PUT':
        patient_exists = paciente_collection.find_one(
            {"rut": request.data["rut"]})
        # que no exista o que exista pero que coincida con el rut del patient que quiero editar
        if patient_exists == None or (patient_exists != None and rut_paciente == request.data["rut"]):
            # actualizar
            request.data.pop('_id')
            historial_clinico = encriptar_or_desencriptar(
                request.data, "encriptar")
            result_update = paciente_collection.update_one(
                {'rut': rut_paciente}, {'$set': historial_clinico})
            return Response({"result": True})
        else:
            return Response({"detail": "Patient rut already exists"})

    if request.method == 'DELETE':

        delete_patient = paciente_collection.delete_one(
            {'rut': rut_paciente})

        if delete_patient.deleted_count > 0:
            return Response({"pateient deleted": True})
        else:
            return Response({"detail": "The patient does not exist"})

@api_view(['PUT']) 
def setEsAtendidoAhoraView(request, rut_paciente):
    if not tokenDeSesionValido(request.headers["Authorization"]):
        return Response({"detail": "Authentication credentials were not provided."})
        
    if request.method == 'PUT':
        es_atendido_ahora = request.data['es_atendido_ahora']
        result_update = paciente_collection.update_one(
            {'rut': rut_paciente}, {'$set': { "es_atendido_ahora": es_atendido_ahora }}
        )

        return Response({"result": True})

@api_view(['GET', 'PUT'])
def pacientesAtendidosView(request, usuario):

    if not tokenDeSesionValido(request.headers["Authorization"]):
        return Response({"detail": "Authentication credentials were not provided."})
    
    profesional_salud = ProfesionalSalud.objects.get(
        user_id=usuario)
    ultimos_pacientes_atendidos = profesional_salud.ultimos_pacientes_atendidos

    if request.method == 'GET':
        ulimos_pacientes_aux = []
        for lista in ultimos_pacientes_atendidos:
            #ulimos_pacientes_aux.append({"rut" : lista.rut})

            paciente = paciente_collection.find_one({"rut": lista.rut})
            paciente = encriptar_or_desencriptar(paciente, "desencriptar")
            if(paciente):
                paciente["_id"] = str(paciente["_id"])
                paciente["fecha"] = lista.fecha
                paciente.pop('profesionales_que_atendieron')
                paciente.pop('sesiones_medica')

                ulimos_pacientes_aux.append(paciente)
                ##print(paciente)

        return Response({"ultimos_pacientes_atendidos": ulimos_pacientes_aux})

    if request.method == 'PUT':
        ultimos_pacientes_atendidos_actualizados = request.data['ultimos_pacientes_atendidos']
        #print(ultimos_pacientes_atendidos_actualizados)
        my_listas = []
        for lista in ultimos_pacientes_atendidos_actualizados:

            my_listas.append(UltimosPacientesAtendidos(rut = lista['rut'], fecha = lista['fecha']))

        profesional_salud.ultimos_pacientes_atendidos = my_listas
        profesional_salud.save()

        return Response({"actualizado" : True})


@api_view(['GET', 'PUT'])
def arquetiposParaUsuarioView(request, pk):

    profesional_salud = ProfesionalSalud.objects.get(id=pk)
    listas_arquetipos =profesional_salud.listas_arquetipos

    if request.method == 'GET':
        #print(listas_arquetipos[0].arquetipos[1].nombre)
        my_listas = []
        for lista in listas_arquetipos:
            my_arquetipos = []
            nombre_lista = lista.nombre_lista
            idioma = lista.idioma
            for arquetipos in lista.arquetipos:
                my_arquetipos.append({"_id":arquetipos._id, "nombre":arquetipos.nombre, "tipo_arquetipo":arquetipos.tipo_arquetipo})
            my_listas.append({"nombre_lista":nombre_lista, "arquetipos":my_arquetipos, "idioma":idioma})

        return Response({"listas_arquetipos" : my_listas})

    if request.method == 'PUT':
        listas_arquetipos_actualizadas = request.data['listas_arquetipos']
        actualizada = True
        
        my_listas = []
        for lista in listas_arquetipos_actualizadas:
            my_arquetipos = []
            for arquetipos in lista['arquetipos']:
                try:
                    arquetipo_id = arquetipos['_id']
                except:
                    arquetipo_id = arquetipos['id']

                my_arquetipos.append(
                    Arquetipo(_id=arquetipo_id, nombre=arquetipos['nombre'], tipo_arquetipo=arquetipos['tipo_arquetipo'])
                )
            lista = ListaArquetipos (
                nombre_lista = lista['nombre_lista'],
                arquetipos = my_arquetipos,
                idioma = lista['idioma']
            )
            my_listas.append(lista)
        
        profesional_salud.listas_arquetipos = my_listas
        profesional_salud.save()

        return Response({"actualizada":actualizada})


@api_view(['GET', 'POST', 'PUT', 'DELETE'])
def paraEditorArquetipos(request, question_id):
    if request.method == 'GET':
        try:
            arquetipoSolicitado = arq_collection.find_one(
                {"_id": ObjectId(question_id)})
            arquetipoSolicitado["_id"] = str(arquetipoSolicitado["_id"])
        except:
            arquetipoSolicitado = arq_collection.find_one({"_id": question_id})
            arquetipoSolicitado["_id"] = str(arquetipoSolicitado["_id"])

        return Response(arquetipoSolicitado)

    if request.method == 'POST':
        result_post = arq_collection.insert_one(request.data).inserted_id
        return Response({"_id": str(result_post)})

    if request.method == 'PUT':
        request.data.pop('_id')
        result_update = arq_collection.update_one(
            {'_id': ObjectId(question_id)}, {'$set': request.data})
        return Response({"result": True})

    if request.method == 'DELETE':
        try:
            eliminar_arquetipo = arq_collection.remove(
                {'_id': ObjectId(question_id)})
        except:
            eliminar_arquetipo = arq_collection.remove({'_id': question_id})
        if eliminar_arquetipo['n'] == 0:  # no lo pudo elinar
            arq_collection.remove({'_id': question_id})

        return Response({"eliminar": True})

# API endpoint that allows users to be viewed or edited.
class UserViewSet(viewsets.ModelViewSet):
    queryset = ProfesionalSalud.objects.all().order_by('-date_joined')
    serializer_class = ProfesionalSaludSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def create(self, request):
        try:
            user_data = request.data["user"]
            profesional_data = request.data
            user = User.objects.create_user(username=user_data["username"], password=user_data["password"],
                                            first_name=user_data["first_name"], last_name=user_data["last_name"], email=user_data["username"], is_staff=False)
            
            """
            arquetipo1 = Arquetipo(_id="qazwsx1", nombre="Medir presion", tipo="CLUSTER")
            arquetipo2 = Arquetipo(_id="qazwsx2", nombre="Resfriado", tipo="OBSERVATION")
            arquetipo3 = Arquetipo(_id="qazwsx3", nombre="Temperatura baja", tipo="CLUSTER")
            arquetipo4 = Arquetipo(_id="qazwsx4", nombre="Bronquitis", tipo="ADMIN_ENTRY")
            arquetipo5 = Arquetipo(_id="qazwsx5", nombre="Virus porcino", tipo="OBSERVATION")
            
            lista1 = ListaArquetipos ( 
                nombre_lista="mySuperList 1", 
                arquetipos=[arquetipo1, arquetipo2] 
            )
            lista2 = ListaArquetipos ( 
                nombre_lista="mySuperList 2", 
                arquetipos=[arquetipo3, arquetipo4, arquetipo5] 
            )
            """
            profesional = ProfesionalSalud(
                user=user, 
                profesion=profesional_data["profesion"], 
                centro_salud=profesional_data["centro_salud"],
                listas_arquetipos=[],#[lista1,lista2]
                ultimos_pacientes_atendidos=[]
            )


            user.save()
            profesional.save()
            id_user_created = User.objects.get(
                username=user_data["username"]).id
            professional_created = ProfesionalSalud.objects.get(
                user_id=int(id_user_created))
            serializer = ProfesionalSaludSerializer(professional_created)
            return Response(serializer.data)

        except KeyError:
            return Response({"detail": "Please write all the fields"})

        except:
            # verificar si existe el usuario:
            myUser = User.objects.get(username=user_data["username"])
            if myUser:
                return Response({"detail": "User already exists"})

            return Response({"detail": "Unexpected error"})

    def list(self, request):
        queryset = ProfesionalSalud.objects.all()
        serializer = ProfesionalSaludSerializer(queryset, many=True)
        return Response(serializer.data)

    def update(self, request, pk=None):

        # Obtengo el usuario que quiero modificar mediante su id
        actual_profesional_data = ProfesionalSalud.objects.get(user_id=pk)
        actual_user_data = User.objects.get(id=pk)
        
        # modifico el usuario
        try:
            # ontengo los nuevos datos del usuario
            user_data = request.data["user"]
            profesional_data = request.data

            if "profesion" in profesional_data:
                actual_profesional_data.profesion = profesional_data["profesion"]
            if "centro_salud" in profesional_data:
                actual_profesional_data.centro_salud = profesional_data["centro_salud"]

            if "username" in user_data:
  
                actual_user_data.email = user_data["username"]
                actual_user_data.username = user_data["username"]

                
            if "password" in user_data:
                actual_user_data.set_password(user_data["password"])
            if "first_name" in user_data:
                actual_user_data.first_name = user_data["first_name"]
            if "last_name" in user_data:
                actual_user_data.last_name = user_data["last_name"]
            
            try:
                actual_user_data.save()
            except:
                return Response({"detail": "User already exists"})
                
            actual_profesional_data.save()
            

            professional_updated = ProfesionalSalud.objects.get(user_id=pk)

            serializer = ProfesionalSaludSerializer(professional_updated)
            return Response(serializer.data)
            # return Response({"user updated":True})

        except KeyError:
            return Response({"detail": "Please write all the fields"})

    def destroy(self, request, pk=None):
        try:
            user_data = User.objects.get(id=pk).delete()  # elimina en cascada
            #profesional_data = ProfesionalSalud.objects.get(user_id=pk).delete()
            return Response({"user deleted": True})

        except ProfesionalSalud.DoesNotExist:
            return Response({"detail": "Unexpected error"})


class AdminViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)


class CustomAuthToken(ObtainAuthToken):

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        # solu: retornar el id del profesional relacionado a ese usuario
        # obtenemos el profesional
        try:
            profesional = ProfesionalSalud.objects.get(user_id=user.pk)
            user_id = profesional.id
        except:
            user_id = user.id
        #print (profesional.id)

        return Response({
            'token': token.key,
            'user_id': user_id,  # user.pk,
            'usurname': user.username,
            'is_admin': user.is_staff
        })
