import os
import sys
import tkinter as tk
from tkinter import ttk
import carpetas

I={}

def cargar_iconos():
    ruta=carpetas.obtener_ruta("Assets/iconos")
    Iconos= os.listdir(ruta)

    for icono in Iconos:
        nombre,_= os.path.splitext(icono)
        ruta_icono=os.path.join(ruta,icono)
        imagen=tk.PhotoImage(file=ruta_icono)
        I[nombre]=imagen

def obtener_icono(icono,escala=1):

    return I[icono].subsample(escala,escala)



