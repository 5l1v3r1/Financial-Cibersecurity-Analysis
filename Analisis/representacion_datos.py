import numpy as np
import os
from datetime import date
import matplotlib
import matplotlib.pyplot as plt
import plotly.plotly as py
from plotly.offline import iplot, init_notebook_mode
import plotly.io as pio
import plotly.graph_objs as go
matplotlib.use('Agg')


def bar_chart(titulo, nom_x_axis, nom_y_axis, tupla_x_axis, lista_y_axis):
    y_pos = np.arange(len(tupla_x_axis))
    nueva_tupla_x_axis = list()
    for tupla_ngram in tupla_x_axis:
        elems_tupla = tupla_ngram.strip("(").strip(")").split(",")
        str_ngram = ""
        for elem in elems_tupla:
            str_ngram += (elem.strip("'").strip(" ")+" ")
        nueva_tupla_x_axis.append(str_ngram)
    nueva_tupla_x_axis = tuple(nueva_tupla_x_axis)
    plt.bar(y_pos, lista_y_axis, align='center', alpha=0.5)
    plt.xticks(y_pos, nueva_tupla_x_axis)
    plt.xlabel(nom_x_axis)
    plt.ylabel(nom_y_axis)
    plt.title(titulo)
    plt.xticks(rotation=90)
    plt.tight_layout()
    newpath = r'Imagenes/{}'.format(date.today())
    if not os.path.exists(newpath):
        os.makedirs(newpath)
    plt.savefig("{}/{}".format(newpath, titulo))
    plt.clf()


def tabla(titulo, lista_atributos, lista_listas_columnas):
    init_notebook_mode(connected=True)
    trace = go.Table(
        header=dict(values=lista_atributos),
        cells=dict(values=lista_listas_columnas)
    )
    data = [trace]
    newpath = r'../Imagenes/{}'.format(date.today())
    if not os.path.exists(newpath):
        os.makedirs(newpath)
    pio.write_image(data, "{}/{}.png".format(newpath, titulo))