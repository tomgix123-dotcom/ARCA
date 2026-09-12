import ctypes
import os
import carpetas

def cargar_fuentes_wind(ruta):
    fuentes_cargadas = ctypes.windll.gdi32.AddFontResourceExW(ruta, 0x10, 0)

    return fuentes_cargadas > 0
    
def cargar_fuentes():
    carpeta= carpetas.obtener_ruta("Assets/fuentes")
    FUENTES= os.listdir(carpeta)

    for fuente in FUENTES:
        ruta= os.path.join(carpeta,fuente)
        cargar_fuentes_wind(ruta)
   