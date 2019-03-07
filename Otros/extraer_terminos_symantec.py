import re
import os
import json


def limpiar_html(raw_html):
    cleanr = re.compile('<.*?>')
    cleantext = re.sub(cleanr, ' ', raw_html)
    cleantext = cleantext.split("\n")
    diccionario_terminos = dict()
    linea_anterior = ''
    termino_anterior = ''
    for linea in cleantext:
        elems_linea = linea.split(" ")
        if len(linea_anterior) < len(linea):
            del elems_linea[:5]
            if elems_linea[0] == '':
                del elems_linea[:3]
            elems_linea = elems_linea[:len(elems_linea)-4]
            if len(elems_linea) > 2:
                del elems_linea[1]
            if elems_linea[:24] == ['Feed', 'Symantec', 'Corp.', '', 'The',
                                    'Threat', 'Explorer', 'is', 'a',
                                    'comprehensive', 'resource', 'for',
                                    'daily,', 'accurate', 'and', 'up-to-date',
                                    'information', 'on', 'the', 'latest',
                                    'threats,', 'risks', 'and',
                                    'vulnerabilities.']:
                del elems_linea[:27]
            if len(elems_linea) > 1:
                diccionario_terminos[elems_linea[0]] = {'link': elems_linea[1],
                                                        'tipo':''}
                termino_anterior = elems_linea[0]
        else:
            if termino_anterior in diccionario_terminos.keys():
                tipo = " ".join(elems_linea)
                diccionario_terminos[termino_anterior]['tipo'] = tipo
        linea_anterior = linea
    return diccionario_terminos


def recorrer_directorio():
    dict_terminos_total = dict()
    for file_name in os.listdir("RSS Symantec"):
        with open("RSS Symantec/{}".format(file_name), "r") as terminos_file:
            texto_file = ""
            for linea in terminos_file:
                elems_linea = linea.split()
                del elems_linea[0:]
                texto_file += linea
            dict_terminos = limpiar_html(texto_file)
            dict_terminos_total = {**dict_terminos_total, **dict_terminos}
    with open("terminos_symantec.json", "w") as terminos_symantec_file:
        json.dump(dict_terminos_total, terminos_symantec_file,
                  indent=4, separators=(',', ': '), sort_keys=True)


def crear_dict_cib():
    lista_terms = list()
    with open("Archivos_JSON/terminos_symantec.json", "r") as terminos_symantec_file:
        dict_symantec = json.load(terminos_symantec_file)
        for nombre in dict_symantec.keys():
            if "." in nombre:
                dict_nombre = {"palabra": nombre}
                nombre = nombre.split(".")[-1]
                dict_nombre1 = {"palabra": nombre}
                lista_terms.append(dict_nombre)
                lista_terms.append(dict_nombre1)
            else:
                dict_nombre = {"palabra": nombre}
                lista_terms.append(dict_nombre)
    with open("Archivos_JSON/palabras_ciberseguridad.json", "r") as palabras_file:
        dict_actual = json.load(palabras_file)
        dict_actual["palabras"].extend(lista_terms)
    with open("Archivos_JSON/palabras_ciberseguridad.json", "w") as palabras_file1:
        json.dump(dict_actual, palabras_file1,
                  indent=4, separators=(',', ': '), sort_keys=True)


def limpiar_terminos():
    palabras_dict = {"palabras":{}}
    nuevo_dict = {"palabras":[]}
    with open("Archivos_JSON/palabras_ciberseguridad.json", "r") as palabras_file:
        dict_palabras_cib = json.load(palabras_file)
        palabras = dict_palabras_cib["palabras"]
        for palabra in palabras:
            palabras_dict["palabras"][palabra["palabra"]] = ''
        for palabra_k in palabras_dict["palabras"].keys():
            if len(palabra_k) > 2:
                nuevo_dict["palabras"].append(palabra_k.lower())
    with open("Archivos_JSON/palabras_ciberseguridad.json", "w") as palabras_file1:
        json.dump(nuevo_dict, palabras_file1)


if __name__ == '__main__':
    limpiar_terminos()