from rest_framework.response import Response
from rest_framework.decorators import api_view

from editor.fileXmlManager import procesarXML

from .lista_arquetipos import listaArquetipos, arq_collection

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
