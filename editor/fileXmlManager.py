#from xml.etree import ElementTree
import xml.etree.ElementTree as ET

#etiquetas
DEFINITION = '{http://schemas.openehr.org/v1}definition'
ATTRIBUTES = '{http://schemas.openehr.org/v1}attributes'
RM_ATTRIBUTE_NAME = '{http://schemas.openehr.org/v1}rm_attribute_name'
ONTOLOGY = '{http://schemas.openehr.org/v1}ontology'
TERM_DEFINITIONS = '{http://schemas.openehr.org/v1}term_definitions'
ITEMS = '{http://schemas.openehr.org/v1}items'
CHILDREN = '{http://schemas.openehr.org/v1}children'
NODE_ID = '{http://schemas.openehr.org/v1}node_id'
RM_TYPE_NAME = '{http://schemas.openehr.org/v1}rm_type_name'
DESCRIPTION = '{http://schemas.openehr.org/v1}description'
DETAILS = '{http://schemas.openehr.org/v1}details'
PURPOSE= '{http://schemas.openehr.org/v1}purpose'
KEYWORDS = '{http://schemas.openehr.org/v1}keywords'
USE = '{http://schemas.openehr.org/v1}use'
MISUSE ='{http://schemas.openehr.org/v1}misuse'
ARCHETYPE_ID = '{http://schemas.openehr.org/v1}archetype_id'
VALUE = '{http://schemas.openehr.org/v1}value'
ORIGINAL_AUTHOR = '{http://schemas.openehr.org/v1}original_author'
OTHER_CONTRIBUTORS = '{http://schemas.openehr.org/v1}other_contributors'
OTHER_DETAILS = '{http://schemas.openehr.org/v1}other_details'
AUTHOR = '{http://schemas.openehr.org/v1}author'
TRANSLATIONS = '{http://schemas.openehr.org/v1}translations'
LANGUAGE = '{http://schemas.openehr.org/v1}language'
CODE_STRING = '{http://schemas.openehr.org/v1}code_string'
UID = '{http://schemas.openehr.org/v1}uid'
COPYRIGHT = '{http://schemas.openehr.org/v1}copyright'
CODE_LIST = '{http://schemas.openehr.org/v1}code_list'
LIST = '{http://schemas.openehr.org/v1}list'
SYMBOL = '{http://schemas.openehr.org/v1}symbol'
DEFINING_CODE = '{http://schemas.openehr.org/v1}defining_code'

#atributos de etiquetas
XSI_TYPE = '{http://www.w3.org/2001/XMLSchema-instance}type'

#funciones
def obtenerNombreArquetipo(root):
    nombre = root.find(ONTOLOGY).find(TERM_DEFINITIONS).find(ITEMS).find(ITEMS).text
    return nombre

def obtenerNombreEstructuras(estructurasPrincipales):
    nombre_estructuras = []
    for estructura in estructurasPrincipales:
        nombre_estructuras.append(estructura.find(RM_ATTRIBUTE_NAME).text)
    return nombre_estructuras

def recolectarHijosForma2(nodo1,nodos_term_definitions, lista_hijos,tipo = 1):
    contenido = []
    #direccion_hijos_tipo_2 = nodo1.find(ATTRIBUTES).find(CHILDREN).find(ATTRIBUTES).find(CHILDREN).findall(CODE_LIST)
    hijos_tipo_2 = {}
    atributos_hijos_comparar = []
    for hijos in lista_hijos:
        if tipo == 2:#si es ordinal
            hijos = hijos.find(SYMBOL).find(DEFINING_CODE).find(CODE_STRING)
        for hijos_comparar in nodos_term_definitions:
            if hijos.text == hijos_comparar.attrib["code"]:
                for items_hijos_comparar in hijos_comparar.findall(ITEMS):
                    if (items_hijos_comparar.attrib["id"] == "text"):
                        hijos_tipo_2["text"] = items_hijos_comparar.text
                                                        
                    if (items_hijos_comparar.attrib["id"] == "description"):
                        hijos_tipo_2["description"] = items_hijos_comparar.text
                                                
                contenido.append(hijos_tipo_2)
                hijos_tipo_2 = {}
    return contenido

def obtenerTipoAndContenidoNodo(nodox, tipo_arquetipo, nodos_term_definitions):
    contenido = []
    tipo_nodo = ""

    primer_tipo_nodo = nodox.find(RM_TYPE_NAME).text
        
    if primer_tipo_nodo == "CLUSTER" or tipo_arquetipo =="SECTION":
        tipo_nodo = primer_tipo_nodo
            
    else:
        cantidad_hijos = len(nodox.find(ATTRIBUTES).findall(CHILDREN))
        if cantidad_hijos > 1:
            tipo_nodo = "CHOICE"
            #extraer hijos tipo 1
            #lista_hijos = nodo1.find(ATTRIBUTES).find(CHILDREN).find(ATTRIBUTES).find(CHILDREN).findall(CODE_LIST) 
            for children in nodox.find(ATTRIBUTES).findall(CHILDREN):
                if children.find(ATTRIBUTES):
                    lista_hijos = children.find(ATTRIBUTES).find(CHILDREN).findall(CODE_LIST)
                    #if(nodo1.find(ATTRIBUTES).find(CHILDREN).find(ATTRIBUTES))
                            
                    #extrae hijos tipo 2 (nodos)
                    contenido = recolectarHijosForma2(nodox,nodos_term_definitions,lista_hijos)

            direccion_hijos_tipo_1 = nodox.find(ATTRIBUTES).findall(CHILDREN)
            hijos_tipo_1 = {}
            for hijos in direccion_hijos_tipo_1:
                hijos_tipo_1["text"] = hijos.find(RM_TYPE_NAME).text
                hijos_tipo_1["description"] = ""
                contenido.append(hijos_tipo_1)
                hijos_tipo_1 = {}

        else:
            tipo_nodo = nodox.find(ATTRIBUTES).find(CHILDREN).find(RM_TYPE_NAME).text
            if tipo_nodo == "DV_CODED_TEXT":
                lista_hijos = nodox.find(ATTRIBUTES).find(CHILDREN).find(ATTRIBUTES).find(CHILDREN).findall(CODE_LIST)
                contenido = recolectarHijosForma2(nodox,nodos_term_definitions,lista_hijos)
                    
            if tipo_nodo == "DV_ORDINAL":
                hijos_tipo_ordinal = {}
                lista_hijos_tipo_ordinal = nodox.find(ATTRIBUTES).find(CHILDREN).findall(LIST)
                #extrae hijos tipo 2 (nodos)
                contenido = recolectarHijosForma2(nodox,nodos_term_definitions,lista_hijos_tipo_ordinal,2)
                #numeros_dv_ordinal  = []
                indice_contenido = 0
                for hijo in lista_hijos_tipo_ordinal:
                    #numeros_dv_ordinal.append(hijo.find(VALUE).text)
                    contenido[indice_contenido]["numero"] = hijo.find(VALUE).text
                    indice_contenido += 1
        
    return contenido, tipo_nodo

#mientras (atributos_nodo_hijo.attrib[XSI_TYPE] == "C_MULTIPLE_ATTRIBUTE") then
def solucion(nodos_en_la_estructura, actual_dic, nodos_term_definitions,tipo_arquetipo):
    cont = 1
    #LO MISMO QUE ARRIBA
    for nodox in nodos_en_la_estructura:
        actual_dic["nodo"+str(cont)] = {}
        id_nodox = nodox.find(NODE_ID).text

        atributos_nodox = nodox.find(ATTRIBUTES)
        if(atributos_nodox):#si tiene atributos
            if(atributos_nodox.attrib[XSI_TYPE] == "C_MULTIPLE_ATTRIBUTE"):
                nodos_en_la_estructura = nodox.find(ATTRIBUTES).findall(CHILDREN)
                solucion(nodos_en_la_estructura,actual_dic["nodo"+str(cont)],nodos_term_definitions, tipo_arquetipo)

        for nodox2 in nodos_term_definitions:
            if id_nodox == nodox2.attrib["code"]:

                items_nodo = nodox2.findall(ITEMS)
                for item in items_nodo:
                    if item.attrib["id"] == "text":
                        actual_dic["nodo"+str(cont)]["text"] = item.text

                    if item.attrib["id"] == "description":
                        actual_dic["nodo"+str(cont)]["description"] = item.text

                    if item.attrib["id"] == "comment":
                        actual_dic["nodo"+str(cont)]["comment"] = item.text

                    if item.attrib["id"] == "source":
                        actual_dic["nodo"+str(cont)]["source"] = item.text

                contenido, tipo_nodo = obtenerTipoAndContenidoNodo(nodox, tipo_arquetipo, nodos_term_definitions)

                actual_dic["nodo"+str(cont)]["tipo"] = tipo_nodo
                actual_dic["nodo"+str(cont)]["contenido"] = contenido

                cont += 1




def construirArquetipo(root):
    tipo_arquetipo = root.find(DEFINITION).find(RM_TYPE_NAME).text
    nodos_term_definitions = root.find(ONTOLOGY).find(TERM_DEFINITIONS).findall(ITEMS)

    todos_nodos_term_definitions = root.find(ONTOLOGY).findall(TERM_DEFINITIONS)
    for term_definitions in todos_nodos_term_definitions:
        if term_definitions.attrib["language"] == "en":
            nodos_term_definitions = term_definitions

    arquetipo = {}
    arquetipo["text"] = obtenerNombreArquetipo(root)
    arquetipo["tipo"] = "base"
    arquetipo["tipo_arquetipo"] = tipo_arquetipo

    definition = root.find(DEFINITION)
    estructurasPrincipales = definition.findall(ATTRIBUTES)#2 estructuras


        
    #agrego las estructuras que le faltan a OBSERVATION
    if(tipo_arquetipo=="OBSERVATION"):
        resto_estructuras = definition.find(ATTRIBUTES).find(CHILDREN).find(ATTRIBUTES).find(CHILDREN).findall(ATTRIBUTES)
        print(len(resto_estructuras))
        for estructura in resto_estructuras:
            estructurasPrincipales.append(estructura)

    numero_de_estructuras = len(estructurasPrincipales)
    nombre_estructuras = obtenerNombreEstructuras(estructurasPrincipales) 

    for i in range(len(estructurasPrincipales)):
        arquetipo["estructura"+str(i+1)] = {}
        arquetipo["estructura"+str(i+1)]["text"] = nombre_estructuras[i]
        arquetipo["estructura"+str(i+1)]["tipo"] = "estructural"
        #arquetipo["estructura"+str(i+1)]["X"] = i

        if(tipo_arquetipo=="ACTION"):
            if(i==0):
                nodos_hijos_definition = estructurasPrincipales[i].findall(CHILDREN)
            else:
                nodos_hijos_definition = estructurasPrincipales[i].find(CHILDREN).find(ATTRIBUTES).findall(CHILDREN)

        if(tipo_arquetipo=="EVALUATION" or tipo_arquetipo=="COMPOSITION" or tipo_arquetipo=="INSTRUCTION" or tipo_arquetipo=="ADMIN_ENTRY" or tipo_arquetipo=="OBSERVATION"):
            nodos_hijos_definition = estructurasPrincipales[i].find(CHILDREN).find(ATTRIBUTES).findall(CHILDREN) # todos los nodos de definition
        if(tipo_arquetipo=="CLUSTER" or tipo_arquetipo=="SECTION"):
            nodos_hijos_definition = estructurasPrincipales[i].findall(CHILDREN)
        cont = 1
        for nodo1 in nodos_hijos_definition:
            arquetipo["estructura"+str(i+1)]["nodo"+str(cont)] = {}
            id_nodo_hijo = nodo1.find(NODE_ID).text
            atributos_nodo_hijo = nodo1.find(ATTRIBUTES)
            if(atributos_nodo_hijo):#si tiene atributos
                if(atributos_nodo_hijo.attrib[XSI_TYPE] == "C_MULTIPLE_ATTRIBUTE"):

                    nodos_en_la_estructura = nodo1.find(ATTRIBUTES).findall(CHILDREN)
                    solucion(nodos_en_la_estructura, arquetipo["estructura"+str(i+1)]["nodo"+str(cont)],nodos_term_definitions,tipo_arquetipo)
                    
            
            for nodo2 in nodos_term_definitions:
                if id_nodo_hijo == nodo2.attrib["code"]:

                    items_nodo = nodo2.findall(ITEMS)
                    for item in items_nodo:
                        if item.attrib["id"] == "text":
                            arquetipo["estructura"+str(i+1)]["nodo"+str(cont)]["text"] = item.text
                        if item.attrib["id"] == "description":
                            arquetipo["estructura"+str(i+1)]["nodo"+str(cont)]["description"] = item.text
                        if item.attrib["id"] == "comment":
                            arquetipo["estructura"+str(i+1)]["nodo"+str(cont)]["comment"] = item.text
                        if item.attrib["id"] == "source":
                            arquetipo["estructura"+str(i+1)]["nodo"+str(cont)]["source"] = item.text

                    #extrae contenido que tienen algunos nodos
                    contenido, tipo_nodo = obtenerTipoAndContenidoNodo(nodo1, tipo_arquetipo, nodos_term_definitions)
                                  
                    arquetipo["estructura"+str(i+1)]["nodo"+str(cont)]["tipo"] = tipo_nodo
                    arquetipo["estructura"+str(i+1)]["nodo"+str(cont)]["contenido"] = contenido

                    cont += 1

    #DESCRIPTION

    #encuentra los datos
    details = root.find(DESCRIPTION).find(DETAILS) #primer idioma que encuentra
    todos_details = root.find(DESCRIPTION).findall(DETAILS) #Intenta encontrarlos en ingles
    for deta in todos_details:
        if deta.find(LANGUAGE).find(CODE_STRING).text == "en":
            details = deta

    concept_description = root.find(ONTOLOGY).find(TERM_DEFINITIONS).find(ITEMS).findall(ITEMS)[1].text
    proposito = details.find(PURPOSE).text
    palabras_clave = details.findall(KEYWORDS)
    atributos_palabras_clave = []
    for atrib in palabras_clave:
        atributos_palabras_clave.append(atrib.text)
    uso = details.find(USE).text
    misuse = details.find(MISUSE).text
    #references
    detalles = root.find(DESCRIPTION).findall(OTHER_DETAILS)
    references = ""
    for atrib in detalles:
        if atrib.attrib["id"] == "references":
            references = atrib.text

    print(atributos_palabras_clave)

    #arma la estructura json
    arquetipo["estructura"+str(numero_de_estructuras+1)] = {}
    arquetipo["estructura"+str(numero_de_estructuras+1)]["text"]="description"
    arquetipo["estructura"+str(numero_de_estructuras+1)]["tipo"] = "estructural"
    arquetipo["estructura"+str(numero_de_estructuras+1)]["nodo1"]={}
    arquetipo["estructura"+str(numero_de_estructuras+1)]["nodo1"]["text"] = "concept description"
    arquetipo["estructura"+str(numero_de_estructuras+1)]["nodo1"]["value"] = concept_description
    arquetipo["estructura"+str(numero_de_estructuras+1)]["nodo1"]["tipo"] = "info"
    arquetipo["estructura"+str(numero_de_estructuras+1)]["nodo2"]={}
    arquetipo["estructura"+str(numero_de_estructuras+1)]["nodo2"]["text"] = "purpose"
    arquetipo["estructura"+str(numero_de_estructuras+1)]["nodo2"]["value"] = proposito
    arquetipo["estructura"+str(numero_de_estructuras+1)]["nodo2"]["tipo"] = "info"
    arquetipo["estructura"+str(numero_de_estructuras+1)]["nodo3"]={}
    arquetipo["estructura"+str(numero_de_estructuras+1)]["nodo3"]["text"] = "use"
    arquetipo["estructura"+str(numero_de_estructuras+1)]["nodo3"]["value"] = uso
    arquetipo["estructura"+str(numero_de_estructuras+1)]["nodo3"]["tipo"] = "info"
    arquetipo["estructura"+str(numero_de_estructuras+1)]["nodo4"]={}
    arquetipo["estructura"+str(numero_de_estructuras+1)]["nodo4"]["text"] = "misuse"
    arquetipo["estructura"+str(numero_de_estructuras+1)]["nodo4"]["value"] = misuse
    arquetipo["estructura"+str(numero_de_estructuras+1)]["nodo4"]["tipo"] = "info"
    arquetipo["estructura"+str(numero_de_estructuras+1)]["nodo5"]={}
    arquetipo["estructura"+str(numero_de_estructuras+1)]["nodo5"]["text"] = "keywords"
    arquetipo["estructura"+str(numero_de_estructuras+1)]["nodo5"]["value"] = atributos_palabras_clave
    arquetipo["estructura"+str(numero_de_estructuras+1)]["nodo5"]["tipo"] = "info"
    arquetipo["estructura"+str(numero_de_estructuras+1)]["nodo6"]={}
    arquetipo["estructura"+str(numero_de_estructuras+1)]["nodo6"]["text"] = "references"
    arquetipo["estructura"+str(numero_de_estructuras+1)]["nodo6"]["value"] = references
    arquetipo["estructura"+str(numero_de_estructuras+1)]["nodo6"]["tipo"] = "info"

    #ATTRIBUTION
    id_arquetipo = root.findall(ARCHETYPE_ID)[0].find(VALUE).text

    original_author = root.find(DESCRIPTION).findall(ORIGINAL_AUTHOR)
    atributos_originalAuthor= []
    for atrib in original_author:
        atributos_originalAuthor.append(atrib.text) 

    contribuidores = root.find(DESCRIPTION).findall(OTHER_CONTRIBUTORS)
    atributos_contribuidores = []
    for atrib in contribuidores:
        atributos_contribuidores.append(atrib.text)
    
    #para other identefication
    
    major_version_id = root.find(UID).find(VALUE).text
    canonical_md5 = ""
    custodian_organisation = ""#para current custodian
    custodian_namespace = ""#para current custodian
    current_contact = ""#para current custodian
    mylicence = ""#para licencing
    for atrib in detalles:
        if atrib.attrib["id"] == "MD5-CAM-1.0.1":
            canonical_md5 = atrib.text
        if atrib.attrib["id"] == "custodian_organisation":
            custodian_organisation = atrib.text
        if atrib.attrib["id"] == "custodian_namespace":
            custodian_namespace = atrib.text
        if atrib.attrib["id"] == "current_contact":
            current_contact = atrib.text
        if atrib.attrib["id"] == "licence":
            mylicence = atrib.text
            

    atributos_other_identefication = [major_version_id, canonical_md5]

    #para current custodian
    atributos_current_custodian = [custodian_organisation, custodian_namespace, current_contact]

    #para licencing
    mycopyright = details.find(COPYRIGHT).text
    atributos_licencing = [mycopyright, mylicence]

    
    arquetipo["estructura"+str(numero_de_estructuras+2)] = {}
    arquetipo["estructura"+str(numero_de_estructuras+2)]["text"]="attribution"
    arquetipo["estructura"+str(numero_de_estructuras+2)]["tipo"] = "estructural"
    arquetipo["estructura"+str(numero_de_estructuras+2)]["nodo1"]={}
    arquetipo["estructura"+str(numero_de_estructuras+2)]["nodo1"]["text"] = "archetype ID"
    arquetipo["estructura"+str(numero_de_estructuras+2)]["nodo1"]["value"] = id_arquetipo
    arquetipo["estructura"+str(numero_de_estructuras+2)]["nodo1"]["tipo"] = "info"
    arquetipo["estructura"+str(numero_de_estructuras+2)]["nodo2"]={}
    arquetipo["estructura"+str(numero_de_estructuras+2)]["nodo2"]["text"] = "other identefication"
    arquetipo["estructura"+str(numero_de_estructuras+2)]["nodo2"]["value"] = atributos_other_identefication
    arquetipo["estructura"+str(numero_de_estructuras+2)]["nodo2"]["tipo"] = "info"
    arquetipo["estructura"+str(numero_de_estructuras+2)]["nodo3"]={}
    arquetipo["estructura"+str(numero_de_estructuras+2)]["nodo3"]["text"] = "original author"
    arquetipo["estructura"+str(numero_de_estructuras+2)]["nodo3"]["value"] = atributos_originalAuthor
    arquetipo["estructura"+str(numero_de_estructuras+2)]["nodo3"]["tipo"] = "info"
    arquetipo["estructura"+str(numero_de_estructuras+2)]["nodo4"]={}
    arquetipo["estructura"+str(numero_de_estructuras+2)]["nodo4"]["text"] = "current custodian"
    arquetipo["estructura"+str(numero_de_estructuras+2)]["nodo4"]["value"] = atributos_current_custodian
    arquetipo["estructura"+str(numero_de_estructuras+2)]["nodo4"]["tipo"] = "info"
    arquetipo["estructura"+str(numero_de_estructuras+2)]["nodo5"]={}
    arquetipo["estructura"+str(numero_de_estructuras+2)]["nodo5"]["text"] = "other contributors"
    arquetipo["estructura"+str(numero_de_estructuras+2)]["nodo5"]["value"] = atributos_contribuidores
    arquetipo["estructura"+str(numero_de_estructuras+2)]["nodo5"]["tipo"] = "info"
    arquetipo["estructura"+str(numero_de_estructuras+2)]["nodo6"]={}
    arquetipo["estructura"+str(numero_de_estructuras+2)]["nodo6"]["text"] = "licencing"
    arquetipo["estructura"+str(numero_de_estructuras+2)]["nodo6"]["value"] = atributos_licencing
    arquetipo["estructura"+str(numero_de_estructuras+2)]["nodo6"]["tipo"] = "info"
    if (root.find(TRANSLATIONS)):
        traductor = root.find(TRANSLATIONS).find(AUTHOR).text
        arquetipo["estructura"+str(numero_de_estructuras+2)]["nodo7"]={}
        arquetipo["estructura"+str(numero_de_estructuras+2)]["nodo7"]["text"] = "translators"
        arquetipo["estructura"+str(numero_de_estructuras+2)]["nodo7"]["value"] = traductor
        arquetipo["estructura"+str(numero_de_estructuras+2)]["nodo7"]["tipo"] = "info"


    return arquetipo

def procesarXML(arq_collection,file):#Procesa el archivo xml importado
    tree = ET.parse(file)
    root = tree.getroot() 

    estructuraProcesada = construirArquetipo(root)

    #inserto estructura a mongo (para luego obtenerlo desde el editor y creador de arquetipos) y obtengo id
    idArq = arq_collection.insert_one(estructuraProcesada).inserted_id


    #devuelvo nombre del arquetipo, tipo y su id a lista arquetipos component
    return {"id":str(idArq),"nombre":estructuraProcesada["text"], "tipo_arquetipo": estructuraProcesada["tipo_arquetipo"]} 


