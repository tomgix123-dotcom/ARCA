import os
import sys
import tkinter as tk
from tkinter import ttk
import carpetas

I={}


def obtener_icono(nombre,escala=1):

    icono= (nombre,escala)

    # Si ya tenemos esta versión, la reutilizamos
    if icono in I:
        return I[icono]

    # Si no, buscamos el archivo
    ruta=carpetas.obtener_ruta("Assets/iconos")
    ruta_icono=os.path.join(ruta,nombre + ".png")

    # Lo cargamos
    imagen = tk.PhotoImage(file=ruta_icono)

    # Aplicamos la escala
    imagen = imagen.subsample(escala, escala)

    # Guardamos la imagen para futuras llamadas
    I[icono] = imagen
    

    return imagen



