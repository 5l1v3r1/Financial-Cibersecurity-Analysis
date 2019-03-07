import os
import json
from datetime import date
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
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
            if linea[:4] != ["h", "t", "t", "p"]:
                Story.append(Spacer(1, 12))
    doc.build(Story)


def definir_lista_contenido():
    lista_noticias_hoy = list()
    lista_contenido_mes = list()
    lista_contenido_año = list()
    lista_contenido_total = list()
    lista_contenido_definiciones = list()
    lista_contenido_noticias_concepts = list()
    conceptos_ciberseguridad_mes = "Imagenes/{}/Conceptos de Ciberseguridad mas Comunes del Mes".format(date.today())
    img_conceptos_mes = Image(conceptos_ciberseguridad_mes, inch, inch)
    lista_contenido_mes.append(img_conceptos_mes)
    conceptos_ciberseguridad_año = "Imagenes/{}/Conceptos de Ciberseguridad mas Comunes del Ano".format(
        date.today())
    img_conceptos_año = Image(conceptos_ciberseguridad_año, inch, inch)
    lista_contenido_año.append(img_conceptos_año)
    conceptos_ciberseguridad_total = "Imagenes/{}/Conceptos de Ciberseguridad mas Comunes de la Historia".format(
        date.today())
    img_conceptos_total = Image(conceptos_ciberseguridad_total, inch, inch)
    lista_contenido_total.append(img_conceptos_total)
    with open("Analisis/Archivos_JSON/noticias_conceptos/noticias_conceptos_total.json", "r") as noticias_conceptos_total_file:
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
            lista_contenido_mes.append(key+":"+", ".join(value))
    lista_contenido = lista_contenido_mes + lista_contenido_año + lista_contenido_total
    return lista_contenido
