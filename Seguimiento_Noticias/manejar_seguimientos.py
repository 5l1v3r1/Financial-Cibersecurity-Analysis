import json
import re
import nltk
from nltk.stem.cistem import Cistem
from nltk.corpus import stopwords
nltk.download('stopwords')


def crear_seguimientos():
    dict_titulos = dict()
    with open("Seguimiento_Noticias/titulos.txt", "r") as titulos_noticias_file:
        lista_titulos = list()
        for linea in titulos_noticias_file:
            lista_titulos.append(linea)
    titulos_seguimientos = list()
    for titulo in lista_titulos:
        titulo.strip("\n")
        if dict_titulos.keys():
            existe = False
            if titulo in titulos_seguimientos:
                existe = True
            if not existe:
                dict_titulos[titulo.strip("\n")] = []
                titulos_seguimientos.append(titulo.strip("\n"))
                for titulo1 in lista_titulos:
                    titulo1.strip("\n")
                    if titulo1 != titulo:
                        if determinar_seguimiento(titulo, titulo1):
                            titulos_seguimientos.append(titulo1.strip("\n"))
                            dict_titulos[titulo.strip("\n")].append(titulo1.strip("\n"))
        else:
            dict_titulos[titulo.strip("\n")] = []
            titulos_seguimientos.append(titulo.strip("\n"))
            for titulo1 in lista_titulos:
                titulo1.strip("\n")
                if titulo1 != titulo:
                    if determinar_seguimiento(titulo, titulo1):
                        titulos_seguimientos.append(titulo1.strip("\n"))
                        dict_titulos[titulo.strip("\n")].append(titulo1.strip("\n"))
    with open("Seguimiento Noticias o Temas/seguimientos.json", "w") as seguimientos_file:
        lista_llaves_vacias = list()
        for key, value in dict_titulos.items():
            if len(value) == 0:
                lista_llaves_vacias.append(key)
        for key in lista_llaves_vacias:
            dict_titulos.pop(key, None)
        json.dump(dict_titulos, seguimientos_file)


def determinar_seguimiento(titulo_principal, titulo_querella):
    stemmer = Cistem()
    regex = r'\b\w+\b'
    palabras_titulo_principal = [stemmer.stem("".join(re.findall(regex, palabra.lower()))) for palabra in titulo_principal.split(" ") if palabra not in stopwords.words('english')]
    palabras_titulo_querella = [stemmer.stem("".join(re.findall(regex, palabra.lower()))) for palabra in titulo_querella.split(" ") if palabra not in stopwords.words('english')]
    """AQUI SE DEBEN INCLUIR CONSULTAS A API'S DE NLP PARA OBTENER ENTIDADES
    Y CONCEPTOS"""
    porcentaje_coincidencia = 0
    for palabra_titulo_querella in palabras_titulo_querella:
        if palabra_titulo_querella in palabras_titulo_principal:
            porcentaje_coincidencia += 1
    porcentaje_coincidencia /= len(palabras_titulo_principal)
    if porcentaje_coincidencia >= 0.4:
        return True
    else:
        return False

def aylien_api(texto):
    APP_ID = 'cc29690e'
    KEY = '68898df5f1df83a89c294498c3c5925a'
    ENDPOINT = 'https://api.aylien.com/api/v1'
    client = textapi.Client(APP_ID, KEY)
    entities = client.Entities({"text": texto})
    diccionario_entities = dict()
    """for type, values in entities['entities']:
        diccionario_entities[type] = values"""
    organizations = None
    locations = None
    people = None
    if 'organization' in entities['entities'].keys():
        organizations = entities['entities']['organization']
    if 'location' in entities['entities'].keys():
        locations = entities['entities']['location']
    if 'person' in entities['entities'].keys():
        people = entities['entities']['person']
    concepts = client.Concepts({"text": texto})
    lista_conceptos = list()
    for link_key in concepts['concepts'].keys():
        concept = concepts['concepts'][link_key]['surfaceForms'][0]['string']
        lista_conceptos.append(concept)
    return organizations, lista_conceptos, people, locations


if __name__ == '__main__':
    crear_seguimientos()