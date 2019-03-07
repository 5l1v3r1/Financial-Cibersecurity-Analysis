import os
import json
import re
from collections import Counter


def cargar_palabras_ciberseguridad():
    """FUNCIÓN QUE RETORNA EL DICCIONARIO DE FILTROS DE Filtros_FinTech.json"""
    with open("Archivos_JSON/palabras_ciberseguridad.json", 'r', encoding=
    "utf-8") as filtros_file:
        diccionario_filtros = json.load(filtros_file)
        return diccionario_filtros


def cargar_malos_conceptos_ciberseguridad():
    """FUNCIÓN QUE RETORNA EL DICCIONARIO DE FILTROS DE Filtros_FinTech.json"""
    with open("Analisis/Archivos_TXT/malos_datos_AYLIEN/"
              "malos_conceptos_ciberseguridad.txt", 'r', encoding="utf-8") as \
            malos_concepto_file:
        lista_conceptos = list()
        for linea in malos_concepto_file:
            lista_conceptos.append(linea.strip("\n"))
        return lista_conceptos


def recorrer_directorio():
    for file_name in os.listdir("Analisis/Archivos_JSON/Resultados_AYLIEN/"
                                ):
        nuevo_dict = dict()
        with open("Analisis/Archivos_JSON/Resultados_AYLIEN/{}".format(
                file_name), "r") as elems_file:
            dict_elems = json.load(elems_file)
            for key, value in dict_elems.items():
                if len(key) > 2:
                    nuevo_dict[key.lower()] = value
        with open(
            "Analisis/Archivos_JSON/Resultados_AYLIEN/{}".format(file_name),
            "w") as elems_file1:
            json.dump(nuevo_dict, elems_file1, indent=4,
                  separators=(',', ': '), sort_keys=True)


def limpiar_concepts():
    dict_palabras = cargar_palabras_ciberseguridad()
    lista_malos_conceptos = cargar_malos_conceptos_ciberseguridad()
    with open("Analisis/Archivos_TXT/conceptos_total.json.txt", "r") as \
            conceptos_file:
        diccionario_conceptos_ciberseguridad = dict()
        for linea in conceptos_file:
            regex = r'\b\w+\b'
            palabras = re.findall(regex, linea)
            nombre = " ".join(palabras[:len(palabras)-1])
            menciones = int(palabras[-1])
            if nombre in dict_palabras["palabras"]:
                if nombre not in lista_malos_conceptos:
                    diccionario_conceptos_ciberseguridad[nombre] = menciones
    with open("Analisis/Archivos_JSON/Resultados_AYLIEN_limpios/conceptos_"
              "ciberseguridad_total.json",
              "w") as conceptos_file:
        json.dump(diccionario_conceptos_ciberseguridad, conceptos_file,
                  indent=4, separators=(',', ': '), sort_keys=True)
    with open("Analisis/Archivos_TXT/conceptos_anual.json.txt", "r") as \
            conceptos_file:
        diccionario_conceptos_ciberseguridad = dict()
        for linea in conceptos_file:
            regex = r'\b\w+\b'
            palabras = re.findall(regex, linea)
            nombre = " ".join(palabras[:len(palabras)-1])
            menciones = int(palabras[-1])
            if nombre in dict_palabras["palabras"]:
                if nombre not in lista_malos_conceptos:
                    diccionario_conceptos_ciberseguridad[nombre] = menciones
    with open("Analisis/Archivos_JSON/Resultados_AYLIEN_limpios/conceptos_"
              "ciberseguridad_anual.json",
              "w") as conceptos_file:
        json.dump(diccionario_conceptos_ciberseguridad, conceptos_file,
                  indent=4, separators=(',', ': '), sort_keys=True)
    with open("Analisis/Archivos_TXT/conceptos_mensual.json.txt", "r") as \
            conceptos_file:
        diccionario_conceptos_ciberseguridad = dict()
        for linea in conceptos_file:
            regex = r'\b\w+\b'
            palabras = re.findall(regex, linea)
            nombre = " ".join(palabras[:len(palabras)-1])
            menciones = int(palabras[-1])
            if nombre in dict_palabras["palabras"]:
                if nombre not in lista_malos_conceptos:
                    diccionario_conceptos_ciberseguridad[nombre] = menciones
    with open("Analisis/Archivos_JSON/Resultados_AYLIEN_limpios/conceptos_"
              "ciberseguridad_mensual.json",
              "w") as conceptos_file:
        json.dump(diccionario_conceptos_ciberseguridad, conceptos_file,
                  indent=4, separators=(',', ': '), sort_keys=True)


def quitar_fuentes():
    lista_terminos_junk = ["economy", "business", "finance", "technology",
                           "wealth", "money", "economics", "tecnología",
                           "economía", "finanzas", "ideas"]
    lista_fuentes_includias = list()
    with open("Archivos_JSON/fuentes_rss.json", "r") as fuentes_file:
        dict_fuentes = json.load(fuentes_file)
        lista_total = dict_fuentes["fuentes_generales"]
        lista_total.extend(dict_fuentes["fuentes_especificas"])
        lista_nombres_fuentes = []
        for elem in lista_total:
            nombre = elem["nombre"].lower()
            elems_nombre = nombre.split(" ")
            indice_elems_nombre = 0
            for elem_nom in elems_nombre:
                if elem_nom in lista_terminos_junk:
                    del elems_nombre[indice_elems_nombre]
                indice_elems_nombre += 1
            if " ".join(elems_nombre) not in lista_fuentes_includias:
                lista_fuentes_includias.append(" ".join(elems_nombre))
                lista_nombres_fuentes.append(" ".join(elems_nombre))
        return lista_nombres_fuentes


def obtener_top():
    for file_name in os.listdir(
            "Analisis/Archivos_JSON/Resultados_AYLIEN/"):
        with open("Analisis/Archivos_JSON/Resultados_AYLIEN/{}".format(
                file_name), "r") as elems_file:
            dict_elems = json.load(elems_file)
            top = Counter(dict_elems).most_common()[:]
            with open("Analisis/Archivos_TXT/{}.txt".format(
                file_name), "w") as top_file:
                for elem in top:
                    top_file.write(str(elem)+"\n")


if __name__ == '__main__':
    limpiar_concepts()