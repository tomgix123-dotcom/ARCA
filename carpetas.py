import os
import sys
import config
import uuid

#SE USA PONIENDO ruta = utils.obtener_ruta("AQUI DENTRO LA RUTA DE LO QUE NECESITAS ENCONTRAR")
def obtener_ruta(relative_path):
    base_path = getattr(sys, "_MEIPASS", os.path.abspath("."))
    return os.path.join(base_path, relative_path)


#AÑADE UNA NUEVA CARPETA AL DICCIONARIO=====================================
def añadir_carpeta(datos,nombre,clave):
    carpeta= {"nombre":nombre,
              "clave":clave,
              "id":str(uuid.uuid4())}
    
    datos["carpetas"].append(carpeta)

    config.guardar_json(datos)

    return carpeta


#ELIMINA UNA CARPETA DEL DICCIONARIO=====================================
def quitar_carpeta(datos,carpeta):

    datos["carpetas"].remove(carpeta)
    
    config.guardar_json(datos)
































