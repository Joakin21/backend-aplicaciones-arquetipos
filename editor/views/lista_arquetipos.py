from pymongo import MongoClient

client = MongoClient()
db = client['proyecto4']
arq_collection = db["arquetipos"]
paciente_collection = db["historial_paciente"]

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
        client.close()
    return aArquetipos