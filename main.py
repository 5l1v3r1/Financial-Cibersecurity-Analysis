from Analisis import analisis_ciberseguridad, escribir_documento, crear_contenido, limpiar_datos_AYLIEN
from Seguimiento_Noticias import manejar_seguimientos
from RSS import main_rss as main_rss
import time
from apscheduler.schedulers.blocking import BlockingScheduler


def proceso():
    main_rss.consultas_feed()
    analisis_ciberseguridad.manejar_n_grams()
    #manejar_seguimientos.crear_seguimientos()
    limpiar_datos_AYLIEN.recorrer_directorio()
    limpiar_datos_AYLIEN.obtener_top()
    limpiar_datos_AYLIEN.limpiar_concepts()
    crear_contenido.obtener_conceptos()
    lista_contenido = escribir_documento.definir_lista_contenido()
    escribir_documento.escribir_documento_pdf(lista_contenido)

if __name__ == '__main__':
    scheduler = BlockingScheduler()
    scheduler.add_job(proceso)
    scheduler.add_job(proceso, 'interval', days=5)
    scheduler.start()