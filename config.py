import os
import json
import sys
import seguridad


#===================JSON/CONFIG.DAT===============================================
def ruta_config():
    return os.path.join(RUTA_CONFIG, "config.dat")

def existe_config():
    return os.path.exists(ruta_config())

def existe_arca():

    if not os.path.exists(RUTA_DATA):
        return

    if any(archivo.endswith(".arca") for archivo in os.listdir(RUTA_DATA)):
        return True
        
    
def crear_json(clave_maestra):
    datos={ "carpetas":[],
            "idioma":"Español",
            "protocolos_activos":[]}

    if existe_config():
        return
    
    datos_json = json.dumps(datos, ensure_ascii=False).encode("utf-8")

    salt=seguridad.generar_salt()
    llave=seguridad.generar_llave(clave_maestra,salt)

    iv,datos_cifrados=seguridad.cifrar_bytes(datos_json,llave)

    with open(ruta_config(), "wb") as archivo:
        archivo.write(b"ARCF")
        archivo.write(b"\x01")
        archivo.write(salt)
        archivo.write(iv)
        archivo.write(datos_cifrados)

def guardar_json(datos,llave_config):

    #DESCIFRA JSON
    with open(ruta_config(),"rb") as archivo:
        firma=archivo.read(4)
        version=archivo.read(1)
        salt=archivo.read(16)

    # CONVERTIR EL DICCIONARIO A BYTES
    datos_json = json.dumps(datos, ensure_ascii=False).encode("utf-8")

    #CIFRA DE NUEVO EL JSON
    iv,datos_cifrados=seguridad.cifrar_bytes(datos_json,llave_config)
    
    with open(ruta_config(), "wb") as archivo:
        archivo.write(b"ARCF")
        archivo.write(b"\x01")
        archivo.write(salt)
        archivo.write(iv)
        archivo.write(datos_cifrados)

def leer_json(llave_config):

    #DESCIFRA JSON
    with open(ruta_config(),"rb") as archivo:
        firma=archivo.read(4)
        version=archivo.read(1)
        salt=archivo.read(16)
        iv=archivo.read(12)
        datos_cifrados=archivo.read()
    
    datos_json=seguridad.descifrar_bytes(datos_cifrados,iv,llave_config)

    #CARGA LOS DATOS A LA VARIABLE QUE LO LEE
    return json.loads(datos_json.decode("utf-8"))

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

def preparar_arca(clave_maestra):
    os.makedirs(RUTA_CONFIG, exist_ok=True)
    os.makedirs(RUTA_DATA, exist_ok=True)
    os.makedirs(RUTA_SESSIONS, exist_ok=True)

    crear_json(clave_maestra)


if getattr(sys, "frozen", False):
    BASE = os.path.dirname(sys.executable)
    BASE_RECURSOS = sys._MEIPASS
else:
    BASE = os.path.dirname(os.path.abspath(__file__))
    BASE_RECURSOS = BASE

RUTA_DATA = os.path.join(BASE, "Data")
RUTA_CONFIG = os.path.join(BASE, "Config")
RUTA_SESSIONS = os.path.join(BASE, "Sessions")

RUTA_ASSETS = os.path.join(BASE_RECURSOS, "Assets")
RUTA_IDIOMAS = os.path.join(RUTA_ASSETS, "idiomas")




        
        




    


    
