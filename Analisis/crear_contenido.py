import json
import wikipedia
import re
from collections import Counter
from Analisis.representacion_datos import bar_chart
from datetime import date


def cargar_terminos_symantec():
    """FUNCIÓN QUE RETORNA EL DICCIONARIO DE FILTROS DE Filtros_FinTech.json"""
    with open("Archivos_JSON/terminos_symantec.json", 'r', encoding="utf-8") as terminos_symantec__file:
        diccionario_terminos = json.load(terminos_symantec__file)
        return diccionario_terminos


def obtener_conceptos():
    with open("Analisis/Archivos_JSON/Resultados_AYLIEN_limpios/conceptos_"
              "ciberseguridad_total.json",
              "r") as conceptos_file:
        dict_conceptos_total = json.load(conceptos_file)
        if len(dict_conceptos_total.keys()) >= 10:
            conceptos_mas_comunes_total = Counter(dict_conceptos_total).most_common()[:10]
        else:
            conceptos_mas_comunes_total = Counter(
                dict_conceptos_total).most_common()[:len(dict_conceptos_total.keys())]
        tupla_x_axis = tuple()
        lista_y_axis = list()
        lista_conceptos = list()
        for tupla_conceptos in conceptos_mas_comunes_total:
            lista_conceptos.append(tupla_conceptos[0])
            tupla_x_axis += (tupla_conceptos[0],)
            lista_y_axis.append(tupla_conceptos[1])
        bar_chart("Conceptos de Ciberseguridad mas Comunes de la Historia",
                  "Conceptos", "Nº de Menciones", tupla_x_axis, lista_y_axis)
        obtener_noticias(lista_conceptos, "total")
    with open("Analisis/Archivos_JSON/Resultados_AYLIEN_limpios/conceptos_"
              "ciberseguridad_anual.json",
              "r") as conceptos_file:
        dict_conceptos_anual = json.load(conceptos_file)
        if len(dict_conceptos_anual.keys()) >= 10:
            conceptos_mas_comunes_año = Counter(dict_conceptos_anual).most_common()[:10]
        else:
            conceptos_mas_comunes_año = Counter(
                dict_conceptos_anual).most_common()[:len(dict_conceptos_anual.keys())]
        tupla_x_axis = tuple()
        lista_y_axis = list()
        for tupla_conceptos in conceptos_mas_comunes_año:
            tupla_x_axis += (tupla_conceptos[0],)
            lista_y_axis.append(tupla_conceptos[1])
        bar_chart("Conceptos de Ciberseguridad mas Comunes del Ano",
                  "Conceptos", "Nº de Menciones", tupla_x_axis, lista_y_axis)
        obtener_noticias(lista_conceptos, "año")
    with open("Analisis/Archivos_JSON/Resultados_AYLIEN_limpios/conceptos_"
              "ciberseguridad_mensual.json",
              "r") as conceptos_file:
        dict_conceptos_mensual = json.load(conceptos_file)
        if len(dict_conceptos_mensual.keys()) >= 10:
            conceptos_mas_comunes_mes = Counter(dict_conceptos_mensual).most_common()[:10]
        else:
            conceptos_mas_comunes_mes = Counter(
                dict_conceptos_mensual).most_common()[:len(dict_conceptos_mensual.keys())]
        tupla_x_axis = tuple()
        lista_y_axis = list()
        for tupla_conceptos in conceptos_mas_comunes_mes:
            tupla_x_axis += (tupla_conceptos[0],)
            lista_y_axis.append(tupla_conceptos[1])
        bar_chart("Conceptos de Ciberseguridad mas Comunes del Mes",
                  "Conceptos", "Nº de Menciones", tupla_x_axis, lista_y_axis)
        obtener_noticias(lista_conceptos, "mes")


def obtener_noticias(lista_conceptos, tramo_tiempo):
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
    with open("Analisis/Archivos_JSON/info_noticias.json", "r") as info_noticias_file:
        dict_info_noticias = json.load(info_noticias_file)
    if tramo_tiempo == "total":
        dict_conceptos_noticias = dict()
        for concepto in lista_conceptos:
            dict_conceptos_noticias[concepto] = list()
            for link, value in dict_info_noticias.items():
                if concepto in value["conceptos"]:
                    dict_conceptos_noticias[concepto].append(link.strip("\n"))
        with open("Analisis/Archivos_JSON/noticias_conceptos/noticias_conceptos_total.json", "w") as noticias_conceptos_total_file:
            json.dump(dict_conceptos_noticias, noticias_conceptos_total_file)
    elif tramo_tiempo == "año":
        dict_conceptos_noticias = dict()
        for concepto in lista_conceptos:
            dict_conceptos_noticias[concepto] = list()
            for link, value in dict_info_noticias.items():
                if 'fecha' in value.keys():
                    fecha = value['fecha']
                    regex = r'\b\w+\b'
                    elems_fecha_articulo = fecha.split(" ")
                    elems_fecha_articulo = [
                        " ".join(re.findall(regex, elem)).lower()
                        for elem in elems_fecha_articulo]
                    if año in elems_fecha_articulo:
                        if concepto in value["conceptos"]:
                            dict_conceptos_noticias[concepto].append(link.strip("\n"))
        with open("Analisis/Archivos_JSON/noticias_conceptos/noticias_conceptos_año.json", "w") as noticias_conceptos_año_file:
            json.dump(dict_conceptos_noticias, noticias_conceptos_año_file)
    elif tramo_tiempo == "mes":
        dict_conceptos_noticias = dict()
        for concepto in lista_conceptos:
            dict_conceptos_noticias[concepto] = list()
            for link, value in dict_info_noticias.items():
                if 'fecha' in value.keys():
                    fecha = value['fecha']
                    regex = r'\b\w+\b'
                    elems_fecha_articulo = fecha.split(" ")
                    elems_fecha_articulo = [
                        " ".join(re.findall(regex, elem)).lower()
                        for elem in elems_fecha_articulo]
                    if año in elems_fecha_articulo:
                        if mes in elems_fecha_articulo or elems_fecha_formato_str[1] in elems_fecha_articulo:
                            if concepto in value["conceptos"]:
                                dict_conceptos_noticias[concepto].append(link.strip("\n"))
        with open("Analisis/Archivos_JSON/noticias_conceptos/noticias_conceptos_mes.json", "w") as noticias_conceptos_mes_file:
            json.dump(dict_conceptos_noticias, noticias_conceptos_mes_file)


def obtener_contexto_ngrams():
    pass


def obtener_info_palabra(palabra):
    dict_terminos_symantec = cargar_terminos_symantec()
    if palabra in dict_terminos_symantec.keys():
        link = dict_terminos_symantec[palabra]["link"]
        tipo = dict_terminos_symantec[palabra]["tipo"]
        return tipo, link
    else:
        pagina = wikipedia.page(palabra)
        link = palabra.url
        wikipedia.set_lang("es")
        resumen = wikipedia.summary(palabra, sentences=3)
        if not resumen:
            wikipedia.set_lang("en")
            resumen = wikipedia.summary(palabra, sentences=3)
            if not resumen:
                return link
            else:
                return resumen, link
        else:
            return resumen, link


if __name__ == '__main__':
    obtener_conceptos()