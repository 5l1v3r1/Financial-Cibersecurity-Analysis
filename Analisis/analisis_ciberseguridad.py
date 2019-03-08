from bs4 import BeautifulSoup
from datetime import date
from collections import Counter
from torrequest import torrequest
from Analisis.stop_words import stop_words
import requests
import json
import re
import nltk
from nltk.stem import WordNetLemmatizer
from nltk.util import ngrams
from nltk.corpus import wordnet
from aylienapiclient import textapi
import six
from google.cloud import language
from google.cloud.language import enums
from google.cloud.language import types
from Analisis.representacion_datos import bar_chart
nltk.download('averaged_perceptron_tagger')
nltk.download('punkt')
nltk.download('wordnet')

AÑO_ACTUAL = ''
MES_ACTUAL = ''

"""CAJAS NEGRAS (APIs)"""


def google_nlp_api(texto):
    client = language.LanguageServiceClient()
    if isinstance(texto, six.binary_type):
        texto = texto.decode('utf-8')
    document = types.Document(
        content=texto,
        type=enums.Document.Type.PLAIN_TEXT)
    entidades = client.analyze_entities(document).entities
    for entity in entidades:
        entity_type = enums.Entity.Type(entity.type)
        dict_entidad = {'nombre': entity.name, 'tipo': entity_type.name,
                        'importancia': entity.salience, 'wikipedia_url':
                            entity.metadata.get('wikipedia_url', '-')}


def aylien_api(texto):
    APP_ID = 'f5ab2b54'
    KEY = 'e3bdf56a159cf5bd244714da46ff3aea'
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

"""-------------------------------------------------------------------------"""


def agregar_noticia(url, titulo, fecha):
    print(titulo, fecha)
    page_response = requests.get(url, timeout=20)
    soup = BeautifulSoup(page_response.content, "html.parser")
    textContent = ""
    for node in soup.findAll('p'):
        textContent += str(node.findAll(text=True))
    regex = r'\b\w+\b'
    palabras = re.findall(regex, textContent)
    texto = " ".join(palabras).lower()
    organizations, lista_conceptos, people, locations = aylien_api(texto)
    dict_noticia = {'organizaciones': organizations, 'conceptos':
        lista_conceptos, 'personas': people, 'lugares': locations, 'fecha':
        fecha}
    agregar_info_json(url, dict_noticia)
    generar_n_grams(texto, fecha)
    with open("titulos.txt", "a") as titulos_file:
        titulos_file.write(titulo+"\n")
    #texto = word_tokenize(texto)
    #contenido_taggeado = nltk.pos_tag(texto)
    #analisis_nltk(contenido_taggeado, texto)


def analisis_nltk(lista_palabras_taggeadas, texto):
    is_noun = lambda pos: pos[:2] == 'NN'
    nouns = [word.lower() for (word, pos) in lista_palabras_taggeadas if
             is_noun(pos)]
    nueva_nouns = {}
    for noun in nouns:
        if noun not in nueva_nouns.keys():
            num = 0
            for noun1 in nouns:
                if noun1 == noun:
                    num += 1
            nueva_nouns[noun] = num
    #dispersion_plot(texto, nouns)


def analisis_mensual():
    pass


def analisis_anual():
    pass


def analisis_total():
    pass


def agregar_info_json(url, dict):
    with open("Analisis/Archivos_JSON/info_noticias.json", "r") as \
            info_noticias_file:
        dict_actual = json.load(info_noticias_file)
    with open("Analisis/Archivos_JSON/info_noticias.json", "w") as \
            info_noticias_actualizado_file:
        dict_actual[url] = dict
        json.dump(dict_actual, info_noticias_actualizado_file)


def crear_jsons_datos_estadisticas():
    """AQUI PROGRAMAR FUNCIONALIDAD PARA CLASIFICAR DATOS EN TRAMOS DE TIEMPO"""
    with open("Analisis/Archivos_JSON/info_noticias.json", "r") as \
            info_noticias_file:
        dict_info = json.load(info_noticias_file)
    organizaciones_total = list()
    lugares_total = list()
    personas_total = list()
    conceptos_total = list()
    organizaciones_anual = list()
    lugares_anual = list()
    personas_anual = list()
    conceptos_anual = list()
    organizaciones_mensual = list()
    lugares_mensual = list()
    personas_mensual = list()
    conceptos_mensual = list()
    fecha_hoy = str(date.today()).split("-")
    año = fecha_hoy[0]
    mes = fecha_hoy[1]
    dia = fecha_hoy[2]
    if "0" in mes:
        mes = mes[1:]
    # [Wed, Feb, 13, 00:00:00, 2019]
    elems_fecha_formato_str = date(int(año), int(mes), int(dia)).ctime().split(
        " ")
    elems_fecha_formato_str = [elem.lower() for elem in
                               elems_fecha_formato_str]
    for url_key in dict_info.keys():
        dict_noticia = dict_info[url_key]
        if dict_noticia['organizaciones']:
            organizaciones_total.extend(dict_noticia['organizaciones'])
        if dict_noticia['lugares']:
            lugares_total.extend(dict_noticia['lugares'])
        if dict_noticia['personas']:
            personas_total.extend(dict_noticia['personas'])
        if dict_noticia['conceptos']:
            conceptos_total.extend(dict_noticia['conceptos'])
        if 'fecha' in dict_noticia.keys():
            fecha = dict_noticia['fecha']
            regex = r'\b\w+\b'
            elems_fecha_articulo = fecha.split(" ")
            elems_fecha_articulo = [" ".join(re.findall(regex, elem)).lower()
                                    for elem in elems_fecha_articulo]
            if año in elems_fecha_articulo:
                if dict_noticia['organizaciones']:
                    organizaciones_anual.extend(dict_noticia['organizaciones'])
                if dict_noticia['lugares']:
                    lugares_anual.extend(dict_noticia['lugares'])
                if dict_noticia['personas']:
                    personas_anual.extend(dict_noticia['personas'])
                if dict_noticia['conceptos']:
                    conceptos_anual.extend(dict_noticia['conceptos'])
                if mes in elems_fecha_articulo or elems_fecha_formato_str[
                    1] in elems_fecha_articulo:
                    if dict_noticia['organizaciones']:
                        organizaciones_mensual.extend(dict_noticia[
                                                          'organizaciones'])
                    if dict_noticia['lugares']:
                        lugares_mensual.extend(dict_noticia['lugares'])
                    if dict_noticia['personas']:
                        personas_mensual.extend(dict_noticia['personas'])
                    if dict_noticia['conceptos']:
                        conceptos_mensual.extend(dict_noticia['conceptos'])
    diccionario_organizaciones_total = obtener_dict_num_menciones(
        organizaciones_total)
    with open(
            "Analisis/Archivos_JSON/Resultados_AYLIEN/"
            "organizaciones_total.json",
            "w") as organizaciones_total_file:
        json.dump(diccionario_organizaciones_total, organizaciones_total_file,
                  indent=4, separators=(',', ': '), sort_keys=True)
    diccionario_lugares_total = obtener_dict_num_menciones(lugares_total)
    with open("Analisis/Archivos_JSON/Resultados_AYLIEN/"
              "lugares_total.json",
              "w") as lugares_total_file:
        json.dump(diccionario_lugares_total, lugares_total_file, indent=4,
                  separators=(',', ': '), sort_keys=True)
    diccionario_personas_total = obtener_dict_num_menciones(personas_total)
    with open("Analisis/Archivos_JSON/Resultados_AYLIEN/"
              "personas_total.json",
              "w") as personas_total_file:
        json.dump(diccionario_personas_total, personas_total_file, indent=4,
                  separators=(',', ': '), sort_keys=True)
    diccionario_conceptos_total = obtener_dict_num_menciones(conceptos_total)
    with open("Analisis/Archivos_JSON/Resultados_AYLIEN/"
              "conceptos_total.json",
              "w") as conceptos_total_file:
        json.dump(diccionario_conceptos_total, conceptos_total_file, indent=4,
                  separators=(',', ': '), sort_keys=True)
    diccionario_organizaciones_anual = obtener_dict_num_menciones(
        organizaciones_anual)
    with open(
            "Analisis/Archivos_JSON/Resultados_AYLIEN/"
            "organizaciones_anual.json",
            "w") as organizaciones_anual_file:
        json.dump(diccionario_organizaciones_anual, organizaciones_anual_file,
                  indent=4, separators=(',', ': '), sort_keys=True)
    diccionario_lugares_anual = obtener_dict_num_menciones(lugares_anual)
    with open("Analisis/Archivos_JSON/Resultados_AYLIEN/"
              "lugares_anual.json",
              "w") as lugares_anual_file:
        json.dump(diccionario_lugares_anual, lugares_anual_file, indent=4,
                  separators=(',', ': '), sort_keys=True)
    diccionario_personas_anual = obtener_dict_num_menciones(personas_anual)
    with open("Analisis/Archivos_JSON/Resultados_AYLIEN/"
              "personas_anual.json",
              "w") as personas_anual_file:
        json.dump(diccionario_personas_anual, personas_anual_file, indent=4,
                  separators=(',', ': '), sort_keys=True)
    diccionario_conceptos_anual = obtener_dict_num_menciones(conceptos_anual)
    with open("Analisis/Archivos_JSON/Resultados_AYLIEN/"
              "conceptos_anual.json",
              "w") as conceptos_anual_file:
        json.dump(diccionario_conceptos_anual, conceptos_anual_file, indent=4,
                  separators=(',', ': '), sort_keys=True)
    diccionario_organizaciones_mensual = obtener_dict_num_menciones(
        organizaciones_mensual)
    with open(
            "Analisis/Archivos_JSON/Resultados_AYLIEN/"
            "organizaciones_mensual.json",
            "w") as organizaciones_mensual_file:
        json.dump(diccionario_organizaciones_mensual,
                  organizaciones_mensual_file,
                  indent=4, separators=(',', ': '), sort_keys=True)
    diccionario_lugares_mensual = obtener_dict_num_menciones(lugares_mensual)
    with open("Analisis/Archivos_JSON/Resultados_AYLIEN/"
              "lugares_mensual.json",
              "w") as lugares_mensual_file:
        json.dump(diccionario_lugares_mensual, lugares_mensual_file, indent=4,
                  separators=(',', ': '), sort_keys=True)
    diccionario_personas_mensual = obtener_dict_num_menciones(personas_mensual)
    with open("Analisis/Archivos_JSON/Resultados_AYLIEN/"
              "personas_mensual.json",
              "w") as personas_mensual_file:
        json.dump(diccionario_personas_mensual, personas_mensual_file,
                  indent=4,
                  separators=(',', ': '), sort_keys=True)
    diccionario_conceptos_mensual = obtener_dict_num_menciones(
        conceptos_mensual)
    with open(
            "Analisis/Archivos_JSON/Resultados_AYLIEN/"
            "conceptos_mensual.json",
            "w") as conceptos_mensual_file:
        json.dump(diccionario_conceptos_mensual, conceptos_mensual_file,
                  indent=4,
                  separators=(',', ': '), sort_keys=True)


def generar_n_grams(texto, fecha):
    with open("Analisis/Archivos_JSON/n_grams_total.json", "r") as \
            n_grams_file:
        dict_n_grams = json.load(n_grams_file)
    tokens = [token for token in texto.split(" ") if token != ""]
    bigrams = list(ngrams(tokens, 2))
    trigrams = list(ngrams(tokens, 3))
    cuatrigrams = list(ngrams(tokens, 4))
    quintigrams = list(ngrams(tokens, 5))
    dict_bigrams = dict_n_grams["bigrams"]
    dict_trigrams = dict_n_grams["trigrams"]
    dict_cuatrigrams = dict_n_grams["cuatrigrams"]
    dict_quintigrams = dict_n_grams["quintigrams"]
    for bigram in bigrams:
        if str(bigram) in dict_bigrams.keys():
            dict_bigrams[str(bigram)] += 1
        else:
            dict_bigrams[str(bigram)] = 1
    for trigram in trigrams:
        if str(trigram) in dict_trigrams.keys():
            dict_trigrams[str(trigram)] += 1
        else:
            dict_trigrams[str(trigram)] = 1
    for cuatrigram in cuatrigrams:
        if str(cuatrigram) in dict_cuatrigrams.keys():
            dict_cuatrigrams[str(cuatrigram)] += 1
        else:
            dict_cuatrigrams[str(cuatrigram)] = 1
    for quintigram in quintigrams:
        if str(quintigram) in dict_quintigrams.keys():
            dict_quintigrams[str(quintigram)] += 1
        else:
            dict_quintigrams[str(quintigram)] = 1
    with open("Analisis/Archivos_JSON/n_grams_total.json", "w") as \
            n_grams_file:
        dict_n_grams = {"bigrams": dict_bigrams, "trigrams": dict_trigrams,
                        "cuatrigrams": dict_cuatrigrams, "quintigrams":
                            dict_quintigrams}
        json.dump(dict_n_grams, n_grams_file, indent=4, separators=(',', ': '),
                  sort_keys=True)
    # [2019, 19, 2]
    fecha_hoy = str(date.today()).split("-")
    año = fecha_hoy[0]
    mes = fecha_hoy[1]
    dia = fecha_hoy[2]
    if "0" in mes:
        mes = mes[1:]
    # [Wed, Feb, 13, 00:00:00, 2019]
    elems_fecha_formato_str = date(int(año), int(mes), int(dia)).ctime().\
        split(" ")
    elems_fecha_formato_str = [elem.lower() for elem in
                               elems_fecha_formato_str]
    regex = r'\b\w+\b'
    elems_fecha_articulo = fecha.split(" ")
    elems_fecha_articulo = [" ".join(re.findall(regex, elem)).lower() for
                            elem in elems_fecha_articulo]
    if año in elems_fecha_articulo:
        with open("Analisis/Archivos_JSON/n_grams_anual.json", "r") as \
                n_grams_file:
            dict_n_grams = json.load(n_grams_file)
        tokens = [token for token in texto.split(" ") if token != ""]
        bigrams = list(ngrams(tokens, 2))
        trigrams = list(ngrams(tokens, 3))
        cuatrigrams = list(ngrams(tokens, 4))
        quintigrams = list(ngrams(tokens, 5))
        dict_bigrams = dict_n_grams["bigrams"]
        dict_trigrams = dict_n_grams["trigrams"]
        dict_cuatrigrams = dict_n_grams["cuatrigrams"]
        dict_quintigrams = dict_n_grams["quintigrams"]
        for bigram in bigrams:
            if str(bigram) in dict_bigrams.keys():
                dict_bigrams[str(bigram)] += 1
            else:
                dict_bigrams[str(bigram)] = 1
        for trigram in trigrams:
            if str(trigram) in dict_trigrams.keys():
                dict_trigrams[str(trigram)] += 1
            else:
                dict_trigrams[str(trigram)] = 1
        for cuatrigram in cuatrigrams:
            if str(cuatrigram) in dict_cuatrigrams.keys():
                dict_cuatrigrams[str(cuatrigram)] += 1
            else:
                dict_cuatrigrams[str(cuatrigram)] = 1
        for quintigram in quintigrams:
            if str(quintigram) in dict_quintigrams.keys():
                dict_quintigrams[str(quintigram)] += 1
            else:
                dict_quintigrams[str(quintigram)] = 1
        with open("Analisis/Archivos_JSON/n_grams_anual.json", "w") as\
                n_grams_file:
            dict_n_grams = {"bigrams": dict_bigrams, "trigrams": dict_trigrams,
                            "cuatrigrams": dict_cuatrigrams, "quintigrams":
                                dict_quintigrams}
            json.dump(dict_n_grams, n_grams_file, indent=4,
                      separators=(',', ': '), sort_keys=True)
        if mes in elems_fecha_articulo or elems_fecha_formato_str[1] in \
                elems_fecha_articulo:
            with open("Analisis/Archivos_JSON/n_grams_mensual.json", "r") \
                    as n_grams_file:
                dict_n_grams = json.load(n_grams_file)
            tokens = [token for token in texto.split(" ") if token != ""]
            bigrams = list(ngrams(tokens, 2))
            trigrams = list(ngrams(tokens, 3))
            cuatrigrams = list(ngrams(tokens, 4))
            quintigrams = list(ngrams(tokens, 5))
            dict_bigrams = dict_n_grams["bigrams"]
            dict_trigrams = dict_n_grams["trigrams"]
            dict_cuatrigrams = dict_n_grams["cuatrigrams"]
            dict_quintigrams = dict_n_grams["quintigrams"]
            for bigram in bigrams:
                if str(bigram) in dict_bigrams.keys():
                    dict_bigrams[str(bigram)] += 1
                else:
                    dict_bigrams[str(bigram)] = 1
            for trigram in trigrams:
                if str(trigram) in dict_trigrams.keys():
                    dict_trigrams[str(trigram)] += 1
                else:
                    dict_trigrams[str(trigram)] = 1
            for cuatrigram in cuatrigrams:
                if str(cuatrigram) in dict_cuatrigrams.keys():
                    dict_cuatrigrams[str(cuatrigram)] += 1
                else:
                    dict_cuatrigrams[str(cuatrigram)] = 1
            for quintigram in quintigrams:
                if str(quintigram) in dict_quintigrams.keys():
                    dict_quintigrams[str(quintigram)] += 1
                else:
                    dict_quintigrams[str(quintigram)] = 1
            with open("Analisis/Archivos_JSON/n_grams_mensual.json", "w") \
                    as n_grams_file:
                dict_n_grams = {"bigrams": dict_bigrams, "trigrams":
                    dict_trigrams, "cuatrigrams":dict_cuatrigrams,
                                "quintigrams": dict_quintigrams}
                json.dump(dict_n_grams, n_grams_file, indent=4,
                          separators=(',', ': '), sort_keys=True)


def manejar_n_grams():
    with open("Analisis/Archivos_JSON/n_grams_total.json", "r") as \
            n_grams_file:
        dict_n_grams_total = json.load(n_grams_file)
        bigrams_total = dict_n_grams_total["bigrams"]
        trigrams_total = dict_n_grams_total["trigrams"]
        cuatrigrams_total = dict_n_grams_total["cuatrigrams"]
        quintigrams_total = dict_n_grams_total["quintigrams"]
    with open("Analisis/Archivos_JSON/n_grams_anual.json", "r") as \
            n_grams_file:
        dict_n_grams_anual = json.load(n_grams_file)
        bigrams_anual = dict_n_grams_anual["bigrams"]
        trigrams_anual = dict_n_grams_anual["trigrams"]
        cuatrigrams_anual = dict_n_grams_anual["cuatrigrams"]
        quintigrams_anual = dict_n_grams_anual["quintigrams"]
    with open("Analisis/Archivos_JSON/n_grams_mensual.json", "r") as \
            n_grams_file:
        dict_n_grams_mensual = json.load(n_grams_file)
        bigrams_mensual = dict_n_grams_mensual["bigrams"]
        trigrams_mensual = dict_n_grams_mensual["trigrams"]
        cuatrigrams_mensual = dict_n_grams_mensual["cuatrigrams"]
        quintigrams_mensual = dict_n_grams_mensual["quintigrams"]
    top_10_bigram_total = Counter(bigrams_total).most_common()[:100]
    top_10_trigram_total = Counter(trigrams_total).most_common()[:len(
        trigrams_total)//20]
    top_10_cuatrigram_total = Counter(cuatrigrams_total).most_common()[
                           :len(cuatrigrams_total) // 20]
    top_10_quintigram_total = Counter(quintigrams_total).most_common()[
                              :len(quintigrams_total) // 20]
    top_10_bigram_total, top_10_trigram_total, top_10_cuatrigram_total, \
    top_10_quintigram_total = limpiar_ngrams(top_10_bigram_total,
                                             top_10_trigram_total,
                                             top_10_cuatrigram_total,
                                             top_10_quintigram_total)
    top_10_bigram_anual = Counter(bigrams_anual).most_common()[:100]
    top_10_trigram_anual = Counter(trigrams_anual).most_common()[:len(
        trigrams_anual)//20]
    top_10_cuatrigram_anual = Counter(cuatrigrams_anual).most_common()[
                              :len(cuatrigrams_anual) // 20]
    top_10_quintigram_anual = Counter(quintigrams_anual).most_common()[
                              :len(quintigrams_anual) // 20]
    top_10_bigram_anual, top_10_trigram_anual, top_10_cuatrigram_anual, \
    top_10_quintigram_anual = limpiar_ngrams(top_10_bigram_anual,
                                             top_10_trigram_anual,
                                             top_10_cuatrigram_anual,
                                             top_10_quintigram_anual)
    top_10_bigram_mensual = Counter(bigrams_mensual).most_common()[:100]
    top_10_trigram_mensual = Counter(trigrams_mensual).most_common()[:len(
        trigrams_mensual)//20]
    top_10_cuatrigram_mensual = Counter(cuatrigrams_mensual).most_common()[
                              :len(cuatrigrams_mensual) // 20]
    top_10_quintigram_mensual = Counter(quintigrams_mensual).most_common()
    top_10_bigram_mensual, top_10_trigram_mensual, top_10_cuatrigram_mensual, \
    top_10_quintigram_mensual = limpiar_ngrams(top_10_bigram_mensual,
                                               top_10_trigram_mensual,
                                               top_10_cuatrigram_mensual,
                                               top_10_quintigram_mensual)
    trigram_context(top_10_trigram_total, top_10_trigram_anual,
                    top_10_trigram_mensual)
    cuatrigram_context(top_10_cuatrigram_total, top_10_cuatrigram_anual,
                       top_10_cuatrigram_mensual)
    quintigram_context(top_10_quintigram_total, top_10_quintigram_anual,
                       top_10_quintigram_mensual)
    """top_10_bigram_total = top_10_bigram_total[:10]
    top_10_trigram_total = top_10_trigram_total[:10]
    top_10_bigram_anual = top_10_bigram_anual[:10]
    top_10_trigram_anual = top_10_trigram_anual[:10]
    top_10_bigram_mensual = top_10_bigram_mensual[:10]
    top_10_trigram_mensual = top_10_trigram_mensual[:10]
    valores_top_10_bigram_total = [bigrams_total[elem] for elem in
                                   top_10_bigram_total]
    valores_top_10_trigram_total = [trigrams_total[elem] for elem in
                                   top_10_trigram_total]
    valores_top_10_bigram_anual = [bigrams_anual[elem] for elem in
                                   top_10_bigram_anual]
    valores_top_10_trigram_anual = [trigrams_anual[elem] for elem in
                                   top_10_trigram_anual]
    valores_top_10_bigram_mensual = [bigrams_mensual[elem] for elem in
                                   top_10_bigram_mensual]
    valores_top_10_trigram_mensual = [trigrams_mensual[elem] for elem in
                                   top_10_trigram_mensual]
    bar_chart("Bigramas en Toda la Historia", "Bigramas", "Nº menciones",
              top_10_bigram_total, valores_top_10_bigram_total)
    bar_chart("Trigramas en toda la Historia", "Trigramas", "Nº menciones",
              top_10_trigram_total, valores_top_10_trigram_total)
    bar_chart("Bigramas durante el año {}".format(str(date.today()).split(
        "-")[0]), "Bigramas", "Nº menciones", top_10_bigram_anual,
              valores_top_10_bigram_anual)
    bar_chart("Trigramas durante el año {}".format(str(date.today()).split(
        "-")[0]), "Trigramas", "Nº menciones", top_10_trigram_anual,
              valores_top_10_trigram_anual)
    bar_chart("Bigramas durante {} de {}".format(str(date.today()).split(
        "-")[1], str(date.today()).split(
        "-")[0]), "Bigramas", "Nº menciones",
              top_10_bigram_mensual, valores_top_10_bigram_mensual)
    bar_chart("Trigramas durante {} de {}".format(str(date.today()).split(
        "-")[1], str(date.today()).split(
        "-")[0]), "Trigramas", "Nº menciones",
              top_10_trigram_mensual, valores_top_10_trigram_mensual)"""


def trigram_context(top_trigram_total, top_trigram_anual, top_trigram_mensual):
    dict_context_total = dict()
    for tupla_trigram_total in top_trigram_total:
        cantidad = int(tupla_trigram_total[1])
        elems_trigram_total = tupla_trigram_total[0].strip("'").strip().strip(
            "(").strip(
            ")").split(",")
        bigram_contexto = "".join(elems_trigram_total[:2]).replace("'", "")
        palabra = "".join(elems_trigram_total[-1]).replace("'", "").strip(" ")
        if bigram_contexto not in dict_context_total.keys():
            dict_context_total[bigram_contexto] = {palabra: cantidad}
        else:
            if palabra not in dict_context_total[bigram_contexto].keys():
                dict_context_total[bigram_contexto][palabra] = cantidad
    keys_deleted = []
    for bigram_context in dict_context_total.keys():
        if len(dict_context_total[bigram_context].keys()) < 3:
            keys_deleted.append(bigram_context)
    for context_delete in keys_deleted:
        del dict_context_total[context_delete]
    dict_context_anual = dict()
    for tupla_trigram_anual in top_trigram_anual:
        cantidad = int(tupla_trigram_anual[1])
        elems_trigram_anual = tupla_trigram_anual[0].strip("'").strip().strip(
            "(").strip(
            ")").split(",")
        bigram_contexto = "".join(elems_trigram_anual[:2]).replace("'", "")
        palabra = "".join(elems_trigram_anual[-1]).replace("'", "").strip(" ")
        if bigram_contexto not in dict_context_anual.keys():
            dict_context_anual[bigram_contexto] = {palabra: cantidad}
        else:
            if palabra not in dict_context_anual[bigram_contexto].keys():
                dict_context_anual[bigram_contexto][palabra] = cantidad
            else:
                dict_context_anual[bigram_contexto][palabra] += 1
    keys_deleted = []
    for bigram_context in dict_context_anual.keys():
        if len(dict_context_anual[bigram_context].keys()) < 3:
            keys_deleted.append(bigram_context)
    for context_delete in keys_deleted:
        del dict_context_anual[context_delete]
    dict_context_mensual = dict()
    for tupla_trigram_mensual in top_trigram_mensual:
        cantidad = int(tupla_trigram_mensual[1])
        elems_trigram_mensual = tupla_trigram_mensual[0].strip("'").strip()\
            .strip(
            "(").strip(
            ")").split(",")
        bigram_contexto = "".join(elems_trigram_mensual[:2]).replace("'", "")
        palabra = "".join(elems_trigram_mensual[-1]).replace("'", "").strip(
            " ")
        if bigram_contexto not in dict_context_mensual.keys():
            dict_context_mensual[bigram_contexto] = {palabra: cantidad}
        else:
            if palabra not in dict_context_mensual[bigram_contexto].keys():
                dict_context_mensual[bigram_contexto][palabra] = cantidad
            else:
                dict_context_mensual[bigram_contexto][palabra] += 1
    keys_deleted = []
    for bigram_context in dict_context_mensual.keys():
        if len(dict_context_mensual[bigram_context].keys()) < 3:
            keys_deleted.append(bigram_context)
    for context_delete in keys_deleted:
        del dict_context_mensual[context_delete]
    with open("Analisis/Archivos_JSON/filtered_n_grams/bigrams.json", "w") \
            as filtered_bigrams_file:
        json.dump({"total": dict_context_total, "anual": dict_context_anual,
                   "mensual": dict_context_mensual}, filtered_bigrams_file,
                  indent=4, separators=(',', ': '), sort_keys=True)


def cuatrigram_context(top_cuatrigram_total, top_cuatrigram_anual,
                       top_cuatrigram_mensual):
    dict_context_total = dict()
    for tupla_cuatrigram_total in top_cuatrigram_total:
        cantidad = int(tupla_cuatrigram_total[1])
        elems_cuatrigram_total = tupla_cuatrigram_total[0].strip("'").strip()\
            .strip("(").strip(
            ")").split(",")
        trigram_contexto = "".join(elems_cuatrigram_total[:3]).replace("'", "")
        palabra = "".join(elems_cuatrigram_total[-1]).replace("'", "")\
            .strip(" ")
        if trigram_contexto not in dict_context_total.keys():
            dict_context_total[trigram_contexto] = {palabra: cantidad}
        else:
            if palabra not in dict_context_total[trigram_contexto].keys():
                dict_context_total[trigram_contexto][palabra] = cantidad
    keys_deleted = []
    for trigram_context in dict_context_total.keys():
        if len(dict_context_total[trigram_context].keys()) < 2:
            keys_deleted.append(trigram_context)
    for context_delete in keys_deleted:
        del dict_context_total[context_delete]
    dict_context_anual = dict()
    for tupla_cuatrigram_anual in top_cuatrigram_anual:
        cantidad = int(tupla_cuatrigram_anual[1])
        elems_cuatrigram_anual = tupla_cuatrigram_anual[0].strip("'").strip()\
            .strip("(").strip(
            ")").split(",")
        trigram_contexto = "".join(elems_cuatrigram_anual[:3]).replace("'", "")
        palabra = "".join(elems_cuatrigram_anual[-1]).replace("'", "")\
            .strip(" ")
        if trigram_contexto not in dict_context_anual.keys():
            dict_context_anual[trigram_contexto] = {palabra: cantidad}
        else:
            if palabra not in dict_context_anual[trigram_contexto].keys():
                dict_context_anual[trigram_contexto][palabra] = cantidad
            else:
                dict_context_anual[trigram_contexto][palabra] += 1
    keys_deleted = []
    for trigram_context in dict_context_anual.keys():
        if len(dict_context_anual[trigram_context].keys()) < 2:
            keys_deleted.append(trigram_context)
    for context_delete in keys_deleted:
        del dict_context_anual[context_delete]
    dict_context_mensual = dict()
    for tupla_cuatrigram_mensual in top_cuatrigram_mensual:
        cantidad = int(tupla_cuatrigram_mensual[1])
        elems_cuatrigram_mensual = tupla_cuatrigram_mensual[0].strip("'")\
            .strip().strip(
            "(").strip(
            ")").split(",")
        trigram_contexto = "".join(elems_cuatrigram_mensual[:3])\
            .replace("'", "")
        palabra = "".join(elems_cuatrigram_mensual[-1]).replace("'", "")\
            .strip(" ")
        if trigram_contexto not in dict_context_mensual.keys():
            dict_context_mensual[trigram_contexto] = {palabra: cantidad}
        else:
            if palabra not in dict_context_mensual[trigram_contexto].keys():
                dict_context_mensual[trigram_contexto][palabra] = cantidad
            else:
                dict_context_mensual[trigram_contexto][palabra] += 1
    keys_deleted = []
    for trigram_context in dict_context_mensual.keys():
        if len(dict_context_mensual[trigram_context].keys()) < 2:
            keys_deleted.append(trigram_context)
    for context_delete in keys_deleted:
        del dict_context_mensual[context_delete]
    with open("Analisis/Archivos_JSON/filtered_n_grams/trigrams.json", "w") \
            as filtered_trigrams_file:
        json.dump({"total": dict_context_total, "anual": dict_context_anual,
                   "mensual": dict_context_mensual}, filtered_trigrams_file,
                  indent=4, separators=(',', ': '), sort_keys=True)


def quintigram_context(top_quintigram_total, top_quintigram_anual,
                       top_quintigram_mensual):
    dict_context_total = dict()
    for tupla_quintigram_total in top_quintigram_total:
        cantidad = int(tupla_quintigram_total[1])
        elems_quintigram_total = tupla_quintigram_total[0].strip("'").strip()\
            .strip("(").strip(
            ")").split(",")
        cuatrigram_contexto = "".join(elems_quintigram_total[:4])\
            .replace("'", "")
        palabra = "".join(elems_quintigram_total[-1]).replace("'", "")\
            .strip(" ")
        if cuatrigram_contexto not in dict_context_total.keys():
            dict_context_total[cuatrigram_contexto] = {palabra: cantidad}
        else:
            if palabra not in dict_context_total[cuatrigram_contexto].keys():
                dict_context_total[cuatrigram_contexto][palabra] = cantidad
    keys_deleted = []
    for cuatrigram_context in dict_context_total.keys():
        lista_valores = dict_context_total[cuatrigram_context].values()
        estado_valores = False
        for valor in lista_valores:
            if int(valor) > 20:
                estado_valores = True
        if not estado_valores:
            keys_deleted.append(cuatrigram_context)
    for context_delete in keys_deleted:
        del dict_context_total[context_delete]
    dict_context_anual = dict()
    for tupla_quintigram_anual in top_quintigram_anual:
        cantidad = int(tupla_quintigram_anual[1])
        elems_quintigram_anual = tupla_quintigram_anual[0].strip("'")\
            .strip().strip("(").strip(
            ")").split(",")
        cuatrigram_contexto = "".join(elems_quintigram_anual[:4])\
            .replace("'", "")
        palabra = "".join(elems_quintigram_anual[-1]).replace("'", "")\
            .strip(" ")
        if cuatrigram_contexto not in dict_context_anual.keys():
            dict_context_anual[cuatrigram_contexto] = {palabra: cantidad}
        else:
            if palabra not in dict_context_anual[cuatrigram_contexto].keys():
                dict_context_anual[cuatrigram_contexto][palabra] = cantidad
            else:
                dict_context_anual[cuatrigram_contexto][palabra] += 1
    keys_deleted = []
    for cuatrigram_context in dict_context_anual.keys():
        lista_valores = dict_context_anual[cuatrigram_context].values()
        estado_valores = False
        for valor in lista_valores:
            if int(valor) > 20:
                estado_valores = True
        if not estado_valores:
            keys_deleted.append(cuatrigram_context)
    for context_delete in keys_deleted:
        del dict_context_anual[context_delete]
    dict_context_mensual = dict()
    for tupla_quintigram_mensual in top_quintigram_mensual:
        cantidad = int(tupla_quintigram_mensual[1])
        elems_quintigram_mensual = tupla_quintigram_mensual[0].strip("'")\
            .strip().strip(
            "(").strip(
            ")").split(",")
        cuatrigram_contexto = "".join(elems_quintigram_mensual[:4])\
            .replace("'", "")
        palabra = "".join(elems_quintigram_mensual[-1]).replace("'", "")\
            .strip(" ")
        if cuatrigram_contexto not in dict_context_mensual.keys():
            dict_context_mensual[cuatrigram_contexto] = {palabra: cantidad}
        else:
            if palabra not in dict_context_mensual[cuatrigram_contexto].keys():
                dict_context_mensual[cuatrigram_contexto][palabra] = cantidad
            else:
                dict_context_mensual[cuatrigram_contexto][palabra] += 1
    keys_deleted = []
    for cuatrigram_context in dict_context_mensual.keys():
        lista_valores = dict_context_mensual[cuatrigram_context].values()
        estado_valores = False
        for valor in lista_valores:
            if int(valor) > 20:
                estado_valores = True
        if not estado_valores:
            keys_deleted.append(cuatrigram_context)
    for context_delete in keys_deleted:
        del dict_context_mensual[context_delete]
    with open("Analisis/Archivos_JSON/filtered_n_grams/cuatrigrams.json", "w") \
            as filtered_cuatrigrams_file:
        json.dump({"total": dict_context_total, "anual": dict_context_anual,
                   "mensual": dict_context_mensual}, filtered_cuatrigrams_file,
                  indent=4, separators=(',', ': '), sort_keys=True)


def obtener_dict_num_menciones(lista_datos):
    wordnet_lemmatizer = WordNetLemmatizer()
    diccionario_datos = dict()
    for dato in lista_datos:
        if wordnet_lemmatizer.lemmatize(dato) not in diccionario_datos.keys():
            num_mencion = 0
            for dato1 in lista_datos:
                if wordnet_lemmatizer.lemmatize(dato) == \
                        wordnet_lemmatizer.lemmatize(dato1):
                    num_mencion += 1
            if num_mencion > 1:
                diccionario_datos[wordnet_lemmatizer.lemmatize(dato)] = \
                    num_mencion
    return diccionario_datos


def escribir_json_noticias_ya_recopiladas():
    with open("Analisis/Archivos_JSON/urls_ciberseguridad.json", "r") as \
            recopilaciones_file:
        diccionario_recopilaciones = json.load(recopilaciones_file)
        for dict_fecha in diccionario_recopilaciones['recopilaciones']:
            fecha = dict_fecha.keys()
            for fhc in fecha:
                fecha = fhc
            urls = dict_fecha[fecha]
            if len(urls) > 0:
                for url in urls:
                    agregar_noticia(url, fecha)


def limpiar_ngrams(lista_bigrams, lista_trigrams, lista_cuatrigrams,
                   lista_quintigrams):
    nueva_lista_bigrams = list()
    nouns = {x.name().split('.', 1)[0] for x in wordnet.all_synsets('n')}
    with open("Analisis/Archivos_JSON/malos_bigrams.json", "r") as \
            junk_bigrams_file:
        dict_junk_bigrams = json.load(junk_bigrams_file)
        for tupla_bigram in lista_bigrams:
            if tupla_bigram[0] not in dict_junk_bigrams["bigrams"]:
                elems_tupla = tupla_bigram[0].strip("'").strip().strip("(")\
                    .strip(")").split(",")
                estado = False
                indice_elem = 0
                estado_noun = False
                for elem in elems_tupla:
                    elem = elem.replace("'", "").strip(" ")
                    if elem in dict_junk_bigrams["conjuntos_letras"]:
                        estado = True
                    """
                    if indice_elem == 1 and elem in stop_words:
                        estado = True"""
                    if not wordnet.synsets(elem):
                        estado = True
                    if elem in nouns:
                        estado_noun = True
                    indice_elem += 1
                if not estado and estado_noun:
                    nueva_lista_bigrams.append(tupla_bigram)
    nueva_lista_trigrams = list()
    with open("Analisis/Archivos_JSON/malos_trigrams.json", "r") as \
            junk_trigrams_file:
        dict_junk_trigrams = json.load(junk_trigrams_file)
        for tupla_trigram in lista_trigrams:
            if tupla_trigram[0] not in dict_junk_trigrams["trigrams"]:
                elems_tupla = tupla_trigram[0].strip("'").strip().strip("(")\
                    .strip(
                    ")").split(",")
                estado = False
                indice_elem = 0
                estado_noun = False
                for elem in elems_tupla:
                    elem = elem.replace("'", "").strip(" ")
                    if elem in dict_junk_trigrams["conjuntos_letras"]:
                        estado = True
                    """if indice_elem == 1 and elem in stop_words:
                        estado = True"""
                    if not wordnet.synsets(elem):
                        estado = True
                    if elem in nouns:
                        estado_noun = True
                    indice_elem += 1
                if not estado and estado_noun:
                    nueva_lista_trigrams.append(tupla_trigram)
    nueva_lista_cuatrigrams = list()
    with open("Analisis/Archivos_JSON/malos_cuatrigrams.json",
              "r") as junk_cuatrigrams_file:
        dict_junk_cuatrigrams = json.load(junk_cuatrigrams_file)
        for tupla_cuatrigram in lista_cuatrigrams:
            if tupla_cuatrigram[0] not in dict_junk_cuatrigrams["cuatrigrams"]:
                elems_tupla = tupla_cuatrigram[0].strip("'").strip().strip(
                    "(").strip(
                    ")").split(",")
                estado = False
                indice_elem = 0
                estado_noun = False
                for elem in elems_tupla:
                    elem = elem.replace("'", "").strip(" ")
                    if elem in dict_junk_cuatrigrams["conjuntos_letras"]:
                        estado = True
                    """if indice_elem == 2 and elem in stop_words:
                        estado = True"""
                    if not wordnet.synsets(elem):
                        estado = True
                    if elem in nouns:
                        estado_noun = True
                    indice_elem += 1
                if not estado and estado_noun:
                    nueva_lista_cuatrigrams.append(tupla_cuatrigram)
    nueva_lista_quintigrams = list()
    with open("Analisis/Archivos_JSON/malos_quintigrams.json",
              "r") as junk_quintigrams_file:
        dict_junk_quintigrams = json.load(junk_quintigrams_file)
        for tupla_quintigram in lista_quintigrams:
            if tupla_quintigram[0] not in dict_junk_quintigrams["quintigrams"]:
                elems_tupla = tupla_quintigram[0].strip("'").strip().strip(
                    "(").strip(
                    ")").split(",")
                estado = False
                indice_elem = 0
                estado_noun = False
                for elem in elems_tupla:
                    elem = elem.replace("'", "").strip(" ")
                    if elem in dict_junk_quintigrams["conjuntos_letras"]:
                        estado = True
                    """if indice_elem == 3 and elem in stop_words:
                        estado = True"""
                    if not wordnet.synsets(elem):
                        estado = True
                    if elem in nouns:
                        estado_noun = True
                    indice_elem += 1
                if not estado and estado_noun:
                    nueva_lista_quintigrams.append(tupla_quintigram)
    return nueva_lista_bigrams, nueva_lista_trigrams, nueva_lista_cuatrigrams,\
           nueva_lista_quintigrams


def output_mvp():
    """Entidades, organizaciones y conceptos en tramos de tiempo.
    Noticias más importantes del tramo de tiempo.
    Concept summary.
    """
    pass


if __name__ == '__main__':
    manejar_n_grams()