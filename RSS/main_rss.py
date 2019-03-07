import datetime
import json

import feedparser

from Analisis import analisis_ciberseguridad as analisis


def cargar_palabras_ciberseguridad():
    """FUNCIÓN QUE RETORNA EL DICCIONARIO DE FILTROS DE Filtros_FinTech.json"""
    with open("Archivos_JSON/palabras_ciberseguridad.json", 'r', encoding="utf-8") as filtros_file:
        diccionario_filtros = json.load(filtros_file)
        return diccionario_filtros


def cargar_fuentes():
    """FUNCIÓN QUE RETORNA EL DICCIONARIO DE LAS FUENTES DE NOTICIAS DE
    fuentes_rss.json"""
    with open("Archivos_JSON/fuentes_rss.json", 'r', encoding="utf-8") as fuentes_file:
        diccionario_fuentes = json.load(fuentes_file)
        return diccionario_fuentes


def cargar_combinaciones_palabras():
    with open("Archivos_JSON/combinaciones_palabras.json", "r") as combinaciones_file:
        lista_combinaciones = json.load(combinaciones_file)["combinaciones"]
        return lista_combinaciones


def determinar_importancia(titulo, contenido, link, peso_fuente):
    puntaje = 0
    #url_entry_parsed = feedparser.parse(link)
    # Se definen en variables las listas de filtros
    diccionario_filtros = cargar_palabras_ciberseguridad()
    lista_diccionarios_palabras = diccionario_filtros["palabras"]
    # -------------------------------------------------------------------------
    # -------------------------------------------------------------------------
    # Se separan las palabras del titulo y del contenido y se ponen en sus
    # listas respectivas
    lista_palabras_titulo = titulo.strip(",").strip(".").strip("(").strip(")").strip("-").split(" ")
    lista_palabras_contenido = contenido.strip(",").strip(".").strip("(").strip(")").strip("-").split(" ")
    # -------------------------------------------------------------------------
    # -------------------------------------------------------------------------
    # Lista a la que se le agregan las palabras FinTech presentes en el
    # articulo
    lista_palabras_ciberseguridad_presentes = list()
    lista_indices_palabras_ciberseguridad_presentes = list()
    # -------------------------------------------------------------------------
    # -------------------------------------------------------------------------
    """PRIMER FILTRO: DE PRESENCIA DE PALABRAS DE CIBERSEGURIDAD EN EL TITULO
    SE DEBE DAR UN PUNTAJE BASE A LA NOTICIA BAJO ESTE CRITERIO"""
    indice_palabra_titulo = 0
    for palabra_titulo in lista_palabras_titulo:
        for diccionario_palabra in lista_diccionarios_palabras:
            # variable dupla_palabras es para palabras FinTech que se componen
            # de 2 palabras (por ejemplo: "banco central")
            dupla_palabras = ""
            # indice de segunda palabra que compone dupla_palabra no debe ser
            # superior al largo de lista_palabras_titulo
            if indice_palabra_titulo < len(lista_palabras_titulo)-1:
                dupla_palabras = palabra_titulo+" "+lista_palabras_titulo[
                    indice_palabra_titulo+1]
            # se ocupa .lower() para que sea case-insensitive
            if palabra_titulo.lower() == diccionario_palabra["palabra"] or \
                            dupla_palabras.lower() == diccionario_palabra[
                        "palabra"]:
                """**** AQUI VER SI HACER UNA LISTA DE PALABRAS SOLO PARA
                TITULO O DEJARLA COMO ESTÁ, QUE ES EN CONJUNTO CON PALABRAS
                DEL ARTICULO ****"""
                lista_palabras_ciberseguridad_presentes.append(diccionario_palabra[
                                                            "palabra"])
        indice_palabra_titulo += 1
    """Añadimos a lista_palabras_ciberseguridad_presentes las palabras de ciberseguridad que
    están presentes en el contenido de la noticia"""
    indice_palabra_contenido = 0
    for palabra_contenido in lista_palabras_contenido:
        for diccionario_palabra in lista_diccionarios_palabras:
            dupla_palabras = ""
            if indice_palabra_contenido < len(lista_palabras_contenido)-1:
                dupla_palabras = palabra_contenido+" "+\
                                 lista_palabras_contenido[
                    indice_palabra_contenido+1]
            if palabra_contenido.lower() == diccionario_palabra["palabra"] or \
                            dupla_palabras.lower() == diccionario_palabra[
                        "palabra"]:
                lista_palabras_ciberseguridad_presentes.append(
                    diccionario_palabra["palabra"])
                lista_indices_palabras_ciberseguridad_presentes.append(
                    indice_palabra_contenido)
        indice_palabra_contenido += 1

    """SEGUNDO FILTRO: SE LE SUMA UN PUNTAJE ELEVADO A LA NOTICIA SI ES QUE
    MENCIONA CONJUNTOS DE PALABRAS ESPECIFICAS DEFINIDAS EN LA LISTA
    lista_palabras_contenido"""
    # La variable puntaje_conjunto_palabras representa la suma total de
    # puntajes por mención de conjuntos de palabras en el articulo
    puntaje_conjunto_palabras = 0
    lista_combinaciones = cargar_combinaciones_palabras()
    lista_conjunto_palabras_mencionadas = list()
    for conjunto_palabras in lista_combinaciones:
        # En la siguiente linea se revisa si el el conjunto_palabras está en
        # la lista lista_palabras_fintech_presentes
        existe_eje = False
        for elem in conjunto_palabras:
            resultado = all(elem in lista_palabras_ciberseguridad_presentes for elem
                            in conjunto_palabras)
            if resultado:
                # Aqui se le suma un puntaje (**** POR DETERMINAR ****) si el
                # conjunto_palabras está presente en la lista
                # lista_palabras_fintech_presentes
                puntaje_conjunto_palabras += 200
                lista_conjunto_palabras_mencionadas.append(conjunto_palabras)
    puntaje += puntaje_conjunto_palabras
    """FILTRO POR AUTORES (FALTA DEFINIR AUTORES)
    for diccionario_autor in lista_diccionarios_autores:
        if diccionario_autor["nombre"] == autor:
            puntaje += diccionario_autor["peso"]
    """
    """FILTRO POR REPUTACIÓN DE FUENTE"""
    puntaje = puntaje * peso_fuente
    return puntaje, lista_conjunto_palabras_mencionadas


def filtrar_contenido_general(nombre_fuente, contenido, peso):
    """AQUI SE RETORNA UNA LISTA CON DICCIONARIOS QUE REPRESENTAN Y TIENE
    LOS DETALLES RELEVANTES DE UN ARTICULO DE LA FUENTE ESPECIFICADA"""
    # La variable lista_diccionario_entries es una lista de diccionarios en la
    # cual cada diccionario representa una noticia del día de hoy con las
    # llaves "titulo", "link" y "puntaje"
    lista_diccionarios_entries = list()
    # ------------------------------------------------------------------------
    for entry in contenido.entries:
        """Loop por todos los articulos de la fuente"""
        titulo_noticia = entry.title
        """AQUI EL PROBLEMA"""
        contenido = entry.summary
        """----------------------"""
        link_noticia = entry.link
        fecha_actual = datetime.datetime.now().ctime()
        # Se separa el string de la fecha en sus componentes para asi poder
        # obtener las noticias que han salido sólo el día de hoy
        lista_elementos_fecha_actual = fecha_actual.split(" ")
        """La llave 'published' no siempre existe en el diccionario entregado por
         el RSS feed por lo que se debe tomar en cuenta la llave 'updated'"""
        if "published" in entry.keys():
            lista_elems_fecha_articulo = entry.published.split(" ")
            num_ocurrencias = 0
            for elemento in lista_elementos_fecha_actual:
                for elem in lista_elems_fecha_articulo:
                    if elemento == elem:
                        num_ocurrencias += 1
            if num_ocurrencias == 3:
                """Si es que la fecha de publicación de la noticia es el día de
                 hoy entonces determinar el puntaje de la noticia"""
                puntaje, lista_conjunto_palabras = \
                    determinar_importancia(titulo_noticia, contenido,
                                           link_noticia,
                                                 peso)
                lista_diccionarios_entries.append({"titulo":titulo_noticia,
                                            "link":link_noticia, "puntaje":
                                            puntaje, "conjunto_palabras":
                                            lista_conjunto_palabras})
                continue
        elif "updated" in entry.keys():
            lista_elems_fecha_articulo = entry.updated.split(" ")
            num_ocurrencias = 0
            for elemento in lista_elementos_fecha_actual:
                for elem in lista_elems_fecha_articulo:
                    if elemento == elem:
                        num_ocurrencias += 1
            if num_ocurrencias == 3:
                puntaje, lista_conjunto_palabras = \
                    determinar_importancia(titulo_noticia, contenido,
                                           link_noticia, peso)
                lista_diccionarios_entries.append({"titulo": titulo_noticia,
                                                   "link": link_noticia,
                                                   "puntaje": puntaje,
                                                   "conjunto_palabras":
                                                   lista_conjunto_palabras
                                                   })
    return lista_diccionarios_entries


def crear_recopilación_top_noticias(diccionario_fuentes_noticias_generales,
                                diccionario_fuentes_noticias_ciberseguridad):
    """FUNCIÓN QUE ESCRIBE EN UN DOCUMENTO .txt LAS MEJORES NOTICIAS DEL DÍA"""
    with open("Recopilaciones/{}.txt".format(datetime.datetime.now().date()),
              "w") as recopilacion_del_dia_file:
        lista_todas_las_noticias = list()
        for fuente in diccionario_fuentes_noticias_generales.keys():
            # Se ordena la lista de noticias respectiva a cada fuente según su
            # puntaje
            for noticia in diccionario_fuentes_noticias_generales[fuente]:
                lista_todas_las_noticias.append(noticia)
        lista_ordenada_todas_las_noticias = sorted(lista_todas_las_noticias,
                                            key=lambda k: int(k['puntaje']))
        top_noticias = [n for n in lista_ordenada_todas_las_noticias if n[
            'puntaje'] > 0]
        lista_links_noticias_incluidas = list()
        indice_lista_top = 0
        for fuente in diccionario_fuentes_noticias_ciberseguridad.keys():
            for noticia in diccionario_fuentes_noticias_ciberseguridad[fuente]:
                top_noticias.append(noticia)
        for noticia in top_noticias:
            if noticia["link"] not in lista_links_noticias_incluidas:
                del top_noticias[indice_lista_top]
                lista_links_noticias_incluidas.append(noticia["link"])
                recopilacion_del_dia_file.write(noticia["titulo"]+"\n"+
                                                noticia["link"]+"\n"+"\n")
                analisis.agregar_noticia(noticia["link"], noticia["titulo"], datetime.datetime.now().ctime())
                indice_lista_top += 1


def obtener_historial_contenido_especifico():
    diccionario_fuentes = cargar_fuentes()
    diccionario_noticias_fuentes_ciberseguridad = dict()
    for diccionario_fuente in diccionario_fuentes["fuentes_especificas"]:
        nombre = diccionario_fuente["nombre"]
        print(nombre)
        url = diccionario_fuente["url"]
        url_content = feedparser.parse(url)
        lista_diccionarios_entries = list()
        for entry in url_content.entries:
            titulo_noticia = entry.title
            link_noticia = entry.link
            if "published" in entry.keys():
                lista_diccionarios_entries.append(
                    {"titulo": titulo_noticia,
                     "link": link_noticia,
                     "fecha": entry.published
                     })
                continue
            elif "updated" in entry.keys():
                lista_diccionarios_entries.append(
                    {"titulo": titulo_noticia,
                     "link": link_noticia,
                     "fecha": entry.updated
                     })
        diccionario_noticias_fuentes_ciberseguridad[nombre] = lista_diccionarios_entries
    for fuente in diccionario_noticias_fuentes_ciberseguridad.keys():
        for noticia in diccionario_noticias_fuentes_ciberseguridad[fuente]:
            analisis.agregar_noticia(noticia["link"], noticia["titulo"] ,
                                     noticia["fecha"])


def obtener_contenido_especifico(nombre, contenido, peso):
    """AQUI SE RETORNA UNA LISTA CON DICCIONARIOS QUE REPRESENTAN Y TIENE
      LOS DETALLES RELEVANTES DE UN ARTICULO DE LA FUENTE ESPECIFICADA"""
    # La variable lista_diccionario_entries es una lista de diccionarios en la
    # cual cada diccionario representa una noticia del día de hoy con las
    # llaves "titulo", "link" y "puntaje"
    lista_diccionarios_entries = list()
    # ------------------------------------------------------------------------
    for entry in contenido.entries:
        """Loop por todos los articulos de la fuente"""
        titulo_noticia = entry.title
        """AQUI EL PROBLEMA"""
        contenido = entry.summary
        """----------------------"""
        link_noticia = entry.link
        fecha_actual = datetime.datetime.now().ctime()
        # Se separa el string de la fecha en sus componentes para asi poder
        # obtener las noticias que han salido sólo el día de hoy
        lista_elementos_fecha_actual = fecha_actual.split(" ")
        """La llave 'published' no siempre existe en el diccionario entregado por
         el RSS feed por lo que se debe tomar en cuenta la llave 'updated'"""
        if "published" in entry.keys():
            lista_elems_fecha_articulo = entry.published.split(" ")
            num_ocurrencias = 0
            for elemento in lista_elementos_fecha_actual:
                for elem in lista_elems_fecha_articulo:
                    if elemento == elem:
                        num_ocurrencias += 1
            if num_ocurrencias == 3:
                """Si es que la fecha de publicación de la noticia es el día de
                 hoy entonces determinar el puntaje de la noticia"""
                lista_diccionarios_entries.append({"titulo":titulo_noticia,
                                            "link":link_noticia})
                continue
        elif "updated" in entry.keys():
            lista_elems_fecha_articulo = entry.updated.split(" ")
            num_ocurrencias = 0
            for elemento in lista_elementos_fecha_actual:
                for elem in lista_elems_fecha_articulo:
                    if elemento == elem:
                        num_ocurrencias += 1
            if num_ocurrencias == 3:
                lista_diccionarios_entries.append({"titulo": titulo_noticia,
                                                   "link": link_noticia
                                                   })
    return lista_diccionarios_entries


def consultas_feed():
    diccionario_fuentes = cargar_fuentes()
    # La variable diccionario_noticias_fuentes es un diccionario en el que cada
    # key es el nombre de una fuente y cada valor respectivo a una key es una
    # lista de noticias que tienen un determinado puntaje ( > 0 o un top número
    # de noticias)
    diccionario_noticias_fuentes_generales = dict()
    diccionario_noticias_fuentes_ciberseguridad = dict()
    # ------------------------------------------------------------------------
    for diccionario_fuente in diccionario_fuentes["fuentes_generales"]:
        nombre = diccionario_fuente["nombre"]
        print(nombre)
        url = diccionario_fuente["url"]
        peso = diccionario_fuente["peso"]
        url_content = feedparser.parse(url)
        lista_entries = filtrar_contenido_general(nombre, url_content, peso)
        diccionario_noticias_fuentes_generales[nombre] = lista_entries
    for diccionario_fuente in diccionario_fuentes["fuentes_especificas"]:
        nombre = diccionario_fuente["nombre"]
        print(nombre)
        url = diccionario_fuente["url"]
        peso = diccionario_fuente["peso"]
        url_content = feedparser.parse(url)
        lista_entries = obtener_contenido_especifico(nombre, url_content, peso)
        diccionario_noticias_fuentes_ciberseguridad[nombre] = lista_entries
    crear_recopilación_top_noticias(diccionario_noticias_fuentes_generales, diccionario_noticias_fuentes_ciberseguridad)

