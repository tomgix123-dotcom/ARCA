import os
import shutil
import zipfile      
import config
import shutil
import io
import seguridad
import winreg
import sys

#====================SECCION DE ADMINISTRACION DE .ARCA===============================================

def carpeta_a_zip(ruta,informar_progreso=None):

    memoria=io.BytesIO()


    # 1. Calcular el tamaño total de los archivos
    total_bytes = 0

    for raiz, directorios, archivos in os.walk(ruta):
        for archivo in archivos:
            ruta_completa = os.path.join(raiz, archivo)
            total_bytes += os.path.getsize(ruta_completa)

    #Comenzamos a comprimir
    bytes_procesados = 0

    with zipfile.ZipFile(memoria,"w",zipfile.ZIP_STORED) as archivo_zip:

        # Conservar las carpetas vacías
        for raiz, directorios, archivos in os.walk(ruta):
            for directorio in directorios:
                ruta_completa=os.path.join(raiz,directorio)
                ruta_relativa=os.path.relpath(ruta_completa,ruta)

                archivo_zip.writestr(ruta_relativa + "/","")

            # Procesar cada archivo
            for archivo in archivos:
                ruta_completa= os.path.join(raiz,archivo)
                ruta_relativa = os.path.relpath(ruta_completa, ruta)

                # Abrir el archivo original para leerlo
                with open(ruta_completa,"rb") as origen:
                    with archivo_zip.open(ruta_relativa,"w") as destino:

                        while True:

                            # Leer un bloque de hasta 1 MB
                            bloque = origen.read(8*1024*1024)

                            # Si no quedan datos, terminar este archivo
                            if not bloque:
                                break

                            # Escribir el bloque dentro del ZIP
                            destino.write(bloque)

                            #Contar los bytes procesados
                            bytes_procesados += len(bloque)

                            # Calcular y comunicar el progreso
                            if informar_progreso and total_bytes > 0:

                                porcentaje=(bytes_procesados/total_bytes*100)

                                informar_progreso(min(100,porcentaje))


    # 4. Comunicar que la compresión ha terminado
    if informar_progreso:
        informar_progreso(100)

    return memoria.getvalue()

def guardar_arca(carpeta,informar_progreso):
    id=carpeta["id"]
    contraseña= carpeta["clave"]

    ruta_zip= os.path.join(config.RUTA_SESSIONS,str(id))
    
    #==========ENCRIPTAN EL CONTENIDO==========================================
    zip_bytes=carpeta_a_zip(ruta_zip,informar_progreso)
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


def registrar_icono_arca():
    ruta_exe = os.path.abspath(sys.executable)

    # .arca -> ArcaFile
    with winreg.CreateKey(winreg.HKEY_CURRENT_USER, ".arca") as clave:
        
        winreg.SetValueEx(clave, "", 0, winreg.REG_SZ, "ArcaFile")

    # ArcaFile -> DefaultIcon
    with winreg.CreateKey(winreg.HKEY_CURRENT_USER,r"ArcaFile\DefaultIcon") as clave:

        winreg.SetValueEx(clave,"", 0, winreg.REG_SZ, f'"{ruta_exe}",1')
#==================SECCION DE ADMINISTRACION DE CARPETA TEMP=========================================

def crear_carpeta_temp(carpeta,informar_progreso):
    informar_progreso(0)
    
    id=carpeta["id"]
    ruta_arca=os.path.join(config.RUTA_DATA,f"{id}.arca")
    #==========LECTOR DE .ARCA==============================
    with open(ruta_arca,"rb") as arca:
        firma=arca.read(4)
        version=arca.read(1)
        salt=arca.read(16)
        iv=arca.read(12)
        datos_cifrados=arca.read()

    informar_progreso(35)
    #===========SECCION DE DESCIFRADO=======================
    contraseña= carpeta["clave"]

    llave=seguridad.generar_llave(contraseña,salt)

    datos_descifrados=seguridad.descifrar_bytes(datos_cifrados,iv,llave)

    informar_progreso(65)
    #===========SECCION DE CREACION DE CARPETA TEMP==========
    memoria=io.BytesIO(datos_descifrados)

    ruta_carpeta_temp= os.path.join(config.RUTA_SESSIONS,id)

    informar_progreso(85)

    with zipfile.ZipFile(memoria,"r") as zip:
        os.makedirs(ruta_carpeta_temp, exist_ok=True)
        zip.extractall(ruta_carpeta_temp)

    informar_progreso(100)

def eliminar_carpeta_temp(carpeta):
    id=carpeta["id"]
    ruta_carpeta_temp= os.path.join(config.RUTA_SESSIONS,id)

    shutil.rmtree(ruta_carpeta_temp)
    

def carpeta_desbloqueada(carpeta):

    ruta= os.path.join(config.RUTA_SESSIONS,carpeta["id"])

    return os.path.exists(ruta)

def cuantas_carpetas_desbloqueadas():

    if os.path.exists(config.RUTA_SESSIONS):

        ruta= config.RUTA_SESSIONS

        cantidad = len(os.listdir(ruta))

        return cantidad

def sesiones_abiertas(datos):
    abiertas=[]


    for carpeta in datos["carpetas"]:

        if carpeta_desbloqueada(carpeta):

            abiertas.append(carpeta)

    return abiertas


    

    

















