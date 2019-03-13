import os
import json
from datetime import date
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from Analisis.crear_contenido import obtener_conceptos
from reportlab.lib.enums import TA_JUSTIFY


def escribir_documento_pdf(lista_contenido):
    doc = SimpleDocTemplate(
        "Informes/{}.pdf".format(date.today()), pagesize=letter)
    width, height = letter
    Story = []
    logo = "Imagenes/logo_bcch.png"
    im = Image(logo, inch, inch)
    Story.append(im)
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name='Justify', alignment=TA_JUSTIFY))
    titulo = "Informe de Ciberseguridad {}".format(date.today())
    ptext = '<font size=22>%s</font>' % titulo
    Story.append(Paragraph(ptext, styles["Normal"]))
    Story.append(Spacer(1, 12))
    for linea in lista_contenido:
        if isinstance(linea, Image):
            Story.append(linea)
            continue
        else:
            ptext = '<font size=12>%s</font>' % linea
            Story.append(Paragraph(ptext, styles["Normal"]))
    doc.build(Story)


def definir_lista_contenido():
    lista_info_conceptos = obtener_conceptos()
    lista_noticias_hoy = list()
    lista_contenido_mes = list()
    lista_contenido_año = list()
    lista_contenido_total = list()
    lista_contenido_definiciones = list()
    lista_contenido_noticias_concepts = list()
    conceptos_ciberseguridad_mes = "Imagenes/{}/Conceptos_Ciberseguridad_del_Mes.png".format(date.today())
    img_conceptos_mes = Image(conceptos_ciberseguridad_mes, 3*inch, 3*inch)
    lista_contenido_mes.append(img_conceptos_mes)
    conceptos_ciberseguridad_año = "Imagenes/{}/Conceptos_Ciberseguridad_en_el_Ano.png".format(
        date.today())
    img_conceptos_año = Image(conceptos_ciberseguridad_año, 3*inch, 3*inch)
    lista_contenido_año.append(img_conceptos_año)
    conceptos_ciberseguridad_total = "Imagenes/{}/Conceptos_Ciberseguridad_en_la_Historia.png".format(
        date.today())
    img_conceptos_total = Image(conceptos_ciberseguridad_total, 3*inch, 3*inch)
    lista_contenido_total.append(img_conceptos_total)
    """with open("Analisis/Archivos_JSON/noticias_conceptos/noticias_conceptos_total.json", "r") as noticias_conceptos_total_file:
        dict_noticias_conceptos = json.load(noticias_conceptos_total_file)
        for key, value in dict_noticias_conceptos.items():
            lista_contenido_total.append(key+":"+", ".join(value))
    with open("Analisis/Archivos_JSON/noticias_conceptos/noticias_conceptos_año.json", "r") as noticias_conceptos_año_file:
        dict_noticias_conceptos = json.load(noticias_conceptos_año_file)
        for key, value in dict_noticias_conceptos.items():
            lista_contenido_año.append(key+":"+", ".join(value))
    with open("Analisis/Archivos_JSON/noticias_conceptos/noticias_conceptos_mes.json", "r") as noticias_conceptos_mes_file:
        dict_noticias_conceptos = json.load(noticias_conceptos_mes_file)
        for key, value in dict_noticias_conceptos.items():
            lista_contenido_mes.append(key+":"+", ".join(value))"""
    lista_contenido = lista_contenido_mes + lista_contenido_año + lista_contenido_total
    for concepto in lista_info_conceptos:
        if concepto is not None:
            palabra = concepto[0]
            resumen = concepto[1]
            link = concepto[2]
            print(palabra+": "+resumen)
            lista_contenido.append("{}: {} \n {}".format(palabra, resumen, link))
    return lista_contenido