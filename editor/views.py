from django.shortcuts import render

from rest_framework.decorators import api_view
from rest_framework import generics
from rest_framework.response import Response

#-------------------------para el login-------------------------------------
#from django.contrib.auth.models import User
from editor.models import usuario
from rest_framework import viewsets
from rest_framework import permissions
from editor.serializers import UserSerializer
#---------------------------------------------------------------------------

from editor.fileXmlManager import procesarXML
from pymongo import MongoClient
from bson.objectid import ObjectId
import pprint

client = MongoClient()
db = client['proyecto4']
arq_collection = db["arquetipos"]

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

@api_view(['GET', 'PUT', 'DELETE'])
def paraEditorArquetipos(request, question_id):
    if request.method == 'GET':


        try:
            arquetipoSolicitado = arq_collection.find_one({"_id": ObjectId(question_id)})
            arquetipoSolicitado["_id"]= str(arquetipoSolicitado["_id"])
        except:
            arquetipoSolicitado = arq_collection.find_one({"_id": question_id})
            arquetipoSolicitado["_id"]= str(arquetipoSolicitado["_id"])

        return Response(arquetipoSolicitado)

    if request.method == 'PUT':
        #print (request.data)
        
        #borro el arquetipo en la db
        try:
            arq_collection.remove({'_id':ObjectId(question_id)})
            resultado = arq_collection.insert_one(request.data)
        except:
            arq_collection.remove({'_id':question_id})
            resultado = arq_collection.insert_one(request.data)

        #inserto el nuevo arquetipo
        

        #print("id con el que viene: ",question_id)
        
        return Response({"respuestra":True})
    
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
    queryset = usuario.objects.all()
    serializer_class = UserSerializer
    #permission_classes = [permissions.IsAuthenticated]
