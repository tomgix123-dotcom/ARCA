import os
import json
import sys


#===================JSON===============================================
def ruta_config():
    return os.path.join(RUTA_CONFIG, "config.json")

def existe_json():
    return os.path.exists(ruta_config())
   
def crear_json():
    datos={ "clave_maestra":"",
            "carpetas":[],
            "idioma":"Español"}

    
    if existe_json() is False:
        with open(ruta_config(), "w") as Json:
            json.dump(datos,Json)
        
def guardar_json(datos):
    with open(ruta_config(), "w") as archivo:
        json.dump(datos, archivo)

def leer_json():
    with open(ruta_config(), "r") as archivo:
        return json.load(archivo)

#============IDIOMAS====================================================
idioma={}

def cargar_idioma(idioma):
    ruta = os.path.join(RUTA_IDIOMAS, f"{idioma}.json")

    with open(ruta, "r", encoding="utf-8") as archivo:
        return json.load(archivo)

def texto(clave,**valores):
    traduccion=idioma.get(clave, f"[{clave}]")

    return traduccion.format(**valores)

#============================CONSTRUIR RUTAS=============================================

def preparar_arca():
    os.makedirs(RUTA_CONFIG, exist_ok=True)
    os.makedirs(RUTA_DATA, exist_ok=True)
    os.makedirs(RUTA_SESSIONS, exist_ok=True)

    crear_json()


if getattr(sys, "frozen", False):
    BASE = os.path.dirname(sys.executable)
else:
    BASE = os.path.dirname(os.path.abspath(__file__))


RUTA_DATA= os.path.join(BASE,"Data")
RUTA_CONFIG=os.path.join(BASE,"Config")
RUTA_SESSIONS=os.path.join(BASE,"Sessions")
RUTA_ASSETS=os.path.join(BASE,"Assets")
RUTA_IDIOMAS=os.path.join(RUTA_ASSETS,"idiomas")





        
        




    


    
