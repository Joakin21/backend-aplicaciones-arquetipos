from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.decorators import api_view

from .lista_arquetipos import paciente_collection, arq_collection
from bson.objectid import ObjectId

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
        """
        request.data.pop('_id')
        result_update = arq_collection.update_one({'_id': question_id}, {'$set': request.data})
        return Response({"result": True})
        """
        request.data.pop('_id')
        try:
            
            """arq_collection.remove({'_id':ObjectId(question_id)})
            resultado = arq_collection.insert_one(request.data)"""
            result_update = arq_collection.update_one({'_id': ObjectId(question_id)}, {'$set': request.data})
        except:
            """arq_collection.remove({'_id':question_id})
            resultado = arq_collection.insert_one(request.data)"""
            result_update = arq_collection.update_one({'_id': question_id}, {'$set': request.data})

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