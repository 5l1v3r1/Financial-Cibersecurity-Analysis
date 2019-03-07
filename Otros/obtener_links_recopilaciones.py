import os
import json


def recopilar_recopilaciones():
    lista_recopilaciones = list()
    for recopilacion_file in os.listdir("../Recopilaciones"):
            lista_urls = obtener_urls("../Recopilaciones/{}".format(recopilacion_file))
            fecha = recopilacion_file[:-4]
            lista_recopilaciones.append({fecha: lista_urls})
    diccionario_json_recopilaciones = {'recopilaciones': lista_recopilaciones}
    escribir_urls(diccionario_json_recopilaciones)


def obtener_urls(url):
    temas_ejes = ["DLT\n", "Criptoactivos\n", "Ciberseguridad\n",
                  "Pagos Digitales\n", "Monitoreo Tecnológico\n", "Big Data\n"
        , "CBDC\n", "Banca Abierta\n", "Otro\n"]
    with open("{}".format(url), "r", errors='ignore') as recopilacion_file:
        contenido = recopilacion_file.readlines()
        lista_lineas = list()
        lista_indices = list()
        indice = 0
        for linea in contenido:
            lista_lineas.append(linea)
            if linea == "Ciberseguridad\n":
                lista_indices.append(indice)
                indice += 1
                continue
            if len(lista_indices) > 0:
                if linea not in temas_ejes:
                    lista_indices.append(indice)
                else:
                    break
            indice += 1
        lista_urls = list()
        for indice in lista_indices:
            linea = lista_lineas[indice]
            lista_letras_linea = list(linea)
            if lista_letras_linea[:4] == ["h", "t", "t", "p"]:
                link = ""
                for letra in lista_letras_linea:
                    if letra != "\n":
                        link += letra
                    else:
                        lista_urls.append(link)
    return lista_urls


def escribir_urls(diccionario_recopilaciones):
    with open("../Analisis/urls_ciberseguridad.json", "w") as urls_ciberseguridad_file:
        json.dump(diccionario_recopilaciones, urls_ciberseguridad_file)


if __name__ == '__main__':
    recopilar_recopilaciones()