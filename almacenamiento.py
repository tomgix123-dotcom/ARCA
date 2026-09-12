import os
import shutil
import zipfile      
import config
import shutil
import io
import seguridad


#====================SECCION DE ADMINISTRACION DE .ARCA===============================================

def carpeta_a_zip(ruta):

    memoria=io.BytesIO()

    with zipfile.ZipFile(memoria,"w",zipfile.ZIP_DEFLATED) as archivo_zip:

        for raiz, directorios, archivos in os.walk(ruta):
            for directorio in directorios:
                ruta_completa=os.path.join(raiz,directorio)
                ruta_relativa=os.path.relpath(ruta_completa,ruta)

                archivo_zip.writestr(ruta_relativa + "/","")

            for archivo in archivos:
                ruta_completa= os.path.join(raiz,archivo)
                ruta_relativa = os.path.relpath(ruta_completa, ruta)

                archivo_zip.write(ruta_completa,ruta_relativa)

    return memoria.getvalue()

def guardar_arca(carpeta):
    id=carpeta["id"]
    contraseña= carpeta["clave"]

    ruta_zip= os.path.join(config.RUTA_SESSIONS,str(id))
    
    #==========ENCRIPTAN EL CONTENIDO==========================================
    zip_bytes=carpeta_a_zip(ruta_zip)
    salt=seguridad.generar_salt()
    llave=seguridad.generar_llave(contraseña,salt)
    iv,datos_cifrados=seguridad.cifrar_bytes(zip_bytes,llave)

    #========CONTRUYE EL .ARCA=================================================
    ruta_arca= os.path.join(config.RUTA_DATA,f"{id}.arca")
    with open(ruta_arca,"wb") as arca:
        arca.write(b"ARCA")
        arca.write(b"\x01")
        arca.write(salt)
        arca.write(iv)
        arca.write(datos_cifrados)

def eliminar_arca(carpeta):
    id=carpeta["id"]

    ruta= os.path.join(config.RUTA_DATA,f"{id}.arca")

    os.remove(ruta)

   
#==================SECCION DE ADMINISTRACION DE CARPETA TEMP=========================================

def crear_carpeta_temp(carpeta):
    
    id=carpeta["id"]
    ruta_arca=os.path.join(config.RUTA_DATA,f"{id}.arca")
    #==========LECTOR DE .ARCA==============================
    with open(ruta_arca,"rb") as arca:
        firma=arca.read(4)
        version=arca.read(1)
        salt=arca.read(16)
        iv=arca.read(12)
        datos_cifrados=arca.read()

    #===========SECCION DE DESCIFRADO=======================
    contraseña= carpeta["clave"]

    llave=seguridad.generar_llave(contraseña,salt)

    datos_descifrados=seguridad.descifrar_bytes(datos_cifrados,iv,llave)

    #===========SECCION DE CREACION DE CARPETA TEMP==========
    memoria=io.BytesIO(datos_descifrados)

    ruta_carpeta_temp= os.path.join(config.RUTA_SESSIONS,id)

    with zipfile.ZipFile(memoria,"r") as zip:
        os.makedirs(ruta_carpeta_temp, exist_ok=True)
        zip.extractall(ruta_carpeta_temp)


def eliminar_carpeta_temp(carpeta):
    id=carpeta["id"]
    ruta_carpeta_temp= os.path.join(config.RUTA_SESSIONS,id)

    shutil.rmtree(ruta_carpeta_temp)
    

def carpeta_desbloqueada(carpeta):

    ruta= os.path.join(config.RUTA_SESSIONS,carpeta["id"])

    return os.path.exists(ruta)


def sesiones_abiertas(datos):

    abiertas=[]

    for carpeta in datos["carpetas"]:

        if carpeta_desbloqueada(carpeta):

            abiertas.append(carpeta)

    return abiertas




















