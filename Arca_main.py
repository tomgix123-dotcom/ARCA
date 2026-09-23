from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.utils import simpleSplit
import os
import msvcrt
import sys
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import pygame
from pathlib import Path
import hashlib
import json
import hashlib
import config
import seguridad
import ui
import ctypes
import carpetas
import fonts
import iconos
import almacenamiento
import uuid
pygame.mixer.init()

#///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
#=================================FUNCIONES VARIADAS===========================================================

def aviso_abiertas():

    abiertas=almacenamiento.sesiones_abiertas(datos)
    cantidad=len(abiertas)

    icono= iconos.obtener_icono("aviso",6)
    aviso=tk.Label(P_inicio["centro_bot"],text=f"AVISO HAY {cantidad} CARPETA DESBLOQUEADA", font=("Px437 Acer VGA 8x8",12),
                   bg="black", fg="orange", image=icono,compound="left")
    aviso.image=icono

    if cantidad == 1:
        aviso.grid(row=2,column=0,pady= 30)
        
    elif cantidad > 1:
        aviso.config(text=f"AVISO HAY {cantidad} CARPETAS DESBLOQUEADAS")
        aviso.grid(row=2,column=0,pady= 30)

def mensaje_establecer_maestra():

    if datos["clave_maestra"] == "":

        mensaje=tk.Label(P_inicio["centro_bot"],text="-Establece una clave maestra para acceder-", font=("Px437 Acer VGA 8x8",12),
                           bg="black", fg="orange")
        mensaje.grid(row=2,column=1,pady= 30)

        return mensaje       

    
#/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
#=================================VENTANA PRINCIPAL============================================================
ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID("Tomgix.Arca")
ventana=ui.crear_ventana()
ventana.title("Arca")
fonts.cargar_fuentes()
iconos.cargar_iconos()
almacenamiento.registrar_icono_arca()
ventana.iconbitmap(carpetas.obtener_ruta("Assets/ARCA.ico"))
#===================================CREAR JSON===================================================================
config.preparar_arca()

#==================================DICCIONARIOS========================================================================
datos=config.leer_json()
for carpeta in datos["carpetas"]:
    carpeta["sesion_recuperada"] = almacenamiento.carpeta_desbloqueada(carpeta)

hash= datos["clave_maestra"]
seleccion={}


#/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
#=================================PANEL DE INCIO======================================================================
P_inicio=ui.crear_P_incio(ventana)
P_inicio["panel"].pack(fill="both", expand=True)

aviso_abiertas()
mensaje=mensaje_establecer_maestra()
#==================================BOTONES BARRA DE TAREAS========================================================
def cerrar():
    ventana.destroy()
def minimizar():
    ventana.iconify()

X=tk.Button(P_inicio["top"],bg="black",fg="orange",text="x",font=("Px437 ACM VGA 8x16",25),relief="flat",
            padx=0,pady=0, command=cerrar)
X.grid(row=0,column=1,sticky="ne")

Minimizar=tk.Button(P_inicio["top"],bg="black",fg="orange",text="_",font=("Px437 ACM VGA 8x16",25),relief="flat",
            padx=0,pady=0, command=minimizar)
Minimizar.grid(row=0,column=0,sticky="ne")

##====================================TITULO========================================================================
Titulo=tk.Label(P_inicio["top"], text="Arca", bg="black", fg="orange",
                 font=("Kelvinized", 100, "underline"))
Titulo.place(relx=0.5, rely=0.5, anchor="center")

##=====================================CLAVE======================================================================
def alternar_visibilidad_contraseña():

    ui.cambiar_estado_ojo(Boton_ojo)
    if Boton_ojo["nombre_icono"] == "ojo":
        Zona_Clave["entry"].configure(show="")

    elif Boton_ojo["nombre_icono"] == "ojo_cerrado":
        Zona_Clave["entry"].configure(show="*")

Boton_ojo = ui.crear_boton_ojo(P_inicio["centro"])
Boton_ojo["boton"].grid(row=1,column=2,padx=20)
Boton_ojo["boton"].configure(command=alternar_visibilidad_contraseña)


#===============================================
Zona_Clave = ui.crear_zona_clave(P_inicio["centro"])
Zona_Clave["label"].grid(row=0,column=1)
Zona_Clave["borde"].grid(row=1, column=1)
Zona_Clave["entry"].pack()

def get_clave(Event=None):
    contraseña_text=Zona_Clave["entry"].get()
    contraseña_hash=seguridad.crear_hash(contraseña_text)

    if datos["clave_maestra"] == "":
    
        datos["clave_maestra"]=contraseña_hash
        config.guardar_json(datos)
        Zona_Clave["entry"].delete(0, tk.END)
        mensaje.grid_forget()

    elif seguridad.check_hash(contraseña_hash, datos["clave_maestra"]):
        grant_acces()
    else: incorrect_pass()
   
def grant_acces():
    P_inicio["panel"].pack_forget()
    P_carpetas["carpetas"].pack(fill="both", expand=True)

def incorrect_pass():
    Borde_Error=ui.crear_borde(P_inicio["panel"],"#604013",6,6)
    Borde_Error.place(relx=0.5, rely=0.54,anchor="center")
    Error=tk.Label(Borde_Error,text="Clave Incorrecta", font=("OCR-A BT",50),
                   bg="orange", fg="black")
    Error.pack()
    ventana.after(1000, Borde_Error.place_forget)

Zona_Clave["entry"].bind("<Return>", get_clave)

Zona_Clave["entry"].focus_set()


#////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
#==========================================CARPETAS=============================================================================

#===ELEMENTOS DE LA PAGINA===========
P_carpetas=ui.crear_PCarpetas(ventana)
panel_info=ui.crear_panel_info(P_carpetas["rigth top"])
botones_carpeta=ui.crear_botones_carpeta(P_carpetas["rigth bot"])
candado=ui.crear_candado_carpeta(P_carpetas["rigth bot"])
bienvenido=ui.crear_bienvenido(P_carpetas["rigth top"])
icono_aprobado=ui.crear_icono_aprobado(P_carpetas["rigth top"])
#====================================




#////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
#=========================================AREA DE CARPETAS===================================================================

def selecionar_carpeta(c):
    ui.destruir_popups(P_carpetas)

    seleccion["carpeta"]=c
    bienvenido.place_forget()
    panel_info["entry_contenido"].delete(0, tk.END)
    ui.actulizar_panel_info(panel_info,c)


    if not almacenamiento.carpeta_desbloqueada(c):
        botones_carpeta["frame"].pack_forget()
        ui.mostrar_candado_carpeta(candado)
        ui.ocultar_icono_aprobado(icono_aprobado)
    else:
        candado.place_forget()
        ui.mostrar_botones_carpeta(botones_carpeta)
        panel_info["seccion_clave"].place_forget()
        ui.mostrar_icono_aprobado(icono_aprobado)

ui.mostrar_carpetas(P_carpetas["left"],datos,funcion=selecionar_carpeta)


#//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
#================================AREA DE INFORMACION DE CARPETAS================================================
ui.mostrar_bienvenido(bienvenido)


def control_acceso(Event=None):
    contraseña=seguridad.crear_hash(panel_info["entry_contenido"].get())
    hash= seleccion["carpeta"]["clave"]

    if seguridad.check_hash(contraseña,hash) is True:
        almacenamiento.crear_carpeta_temp(seleccion["carpeta"])
        candado.place_forget()
        ui.mostrar_botones_carpeta(botones_carpeta)
        panel_info["seccion_clave"].place_forget()
        ui.mostrar_icono_aprobado(icono_aprobado)
        panel_info["entry_contenido"].delete(0, tk.END)
        
panel_info["entry_contenido"].bind("<Return>", control_acceso)

#/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
#===================================BOTONES DE LAS CARPETAS===============================
#==================BOTON OJO========================================================
def alternar_visibilidad_contraseña_carpeta():

    ui.cambiar_estado_ojo(panel_info["boton_ojo_carpeta"])
    if panel_info["boton_ojo_carpeta"]["nombre_icono"] == "ojo":
        panel_info["entry_contenido"].configure(show="")

    elif panel_info["boton_ojo_carpeta"]["nombre_icono"] == "ojo_cerrado":
        panel_info["entry_contenido"].configure(show="*")

panel_info["boton_ojo_carpeta"]["boton"].configure(command=alternar_visibilidad_contraseña_carpeta)
#===========================================
def bloquear_carpeta(Event=None):
    almacenamiento.guardar_arca(seleccion["carpeta"])
    almacenamiento.eliminar_carpeta_temp(seleccion["carpeta"])
    botones_carpeta["frame"].pack_forget()
    ui.mostrar_candado_carpeta(candado)
    icono_aprobado.place_forget()
    panel_info["seccion_clave"].place(relx=0.5,rely=0.5,anchor="center")

    seleccion["carpeta"]["sesion_recuperada"] = False
    ui.refresh(P_carpetas["left"],datos,selecionar_carpeta)

botones_carpeta["bloquear"].configure(command=bloquear_carpeta)

#==========================================
def eliminar_carpeta(popup):

    carpetas.quitar_carpeta(datos,seleccion["carpeta"])
    almacenamiento.eliminar_carpeta_temp(seleccion["carpeta"])

    ui.refresh(P_carpetas["left"],datos,funcion=selecionar_carpeta)
    ui.ocultar_panel_info(panel_info)
    ui.ocultar_icono_aprobado(icono_aprobado)
    ui.mostrar_bienvenido(bienvenido)

    popup["borde"].destroy()
    botones_carpeta["eliminar"].config(state="normal")
    botones_carpeta["frame"].pack_forget()

def abrir_popup_aviso_eliminar():
    ui.destruir_popups(P_carpetas)

    botones_carpeta["eliminar"].config(state="disable")
    popup=ui.popup_aviso_eliminar(P_carpetas["carpetas"],"orange",3,"Eliminar//")

    P_carpetas["popup"] = popup["borde"]
    P_carpetas["popup_boton"] = botones_carpeta["eliminar"]

    def cerrar():
        popup["borde"].destroy()
        botones_carpeta["eliminar"].config(state="normal")

    popup["boton_aceptar"].configure(command=lambda:eliminar_carpeta(popup))
    popup["cancelar"].config(command=cerrar)
    popup["x"].config(command=cerrar)

botones_carpeta["eliminar"].configure(command=abrir_popup_aviso_eliminar)

#===========================================
def abrir_carpeta(Event=None):
    ruta_carpeta_temp= os.path.join(config.RUTA_SESSIONS,seleccion["carpeta"]["id"])

    ventana.iconify()
    os.startfile(ruta_carpeta_temp)

botones_carpeta["abrir"].configure(command=abrir_carpeta)

#==========================================
def renombrar_carpeta(popup):
    nuevo_nombre=popup["nuevo_nombre"].get()

    if nuevo_nombre:
        seleccion["carpeta"]["nombre"] = nuevo_nombre
        config.guardar_json(datos)    
        ui.refresh(P_carpetas["left"],datos,selecionar_carpeta)
        panel_info["nombre"].config(text=nuevo_nombre)
        popup["borde"].destroy()
        botones_carpeta["renombrar"].config(state="normal")

def abrir_popup_renombrar(Event=None):
    ui.destruir_popups(P_carpetas)

    botones_carpeta["renombrar"].config(state="disabled")
    popup=ui.popup_renombrar(P_carpetas["carpetas"],"orange",3,"Renombrar Carpeta//")

    P_carpetas["popup"] = popup["borde"]
    P_carpetas["popup_boton"] = botones_carpeta["renombrar"]

    def cerrar():
        popup["borde"].destroy()
        botones_carpeta["renombrar"].config(state="normal")

    popup["boton_renombrar"].config(command=lambda:renombrar_carpeta(popup))
    popup["cancelar"].config(command=cerrar)
    popup["x"].config(command=cerrar)

botones_carpeta["renombrar"].configure(command=abrir_popup_renombrar)

#/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
#===============================BOTON PARA AÑADIR CARPETAS============================================================
def abrir_popup_nueva_carpeta():

    ui.destruir_popups(P_carpetas)

    popup=ui.crear_popup_nueva_carpeta(P_carpetas["carpetas"],"orange",3,"Nueva Carpeta//")
    ui.mostrar_popup_nueva_carpeta(popup)
    Añadir.config(state="disabled")

    P_carpetas["popup"] = popup["borde"]
    P_carpetas["popup_boton"] = Añadir

    def cerrar():
        Añadir.config(state="normal")
        popup["borde"].destroy()
    
    def alternar_visibilidad_contraseña():

        ui.cambiar_estado_ojo(popup["boton_ojo_popup"])
        if popup["boton_ojo_popup"]["nombre_icono"] == "ojo":
            popup["clave"].configure(show="")

        elif popup["boton_ojo_popup"]["nombre_icono"] == "ojo_cerrado":
            popup["clave"].configure(show="*")


    popup["crear"].config(command=lambda:nueva_carpeta(popup))
    popup["cancelar"].config(command=cerrar)
    popup["x"].config(command=cerrar)
    popup["boton_ojo_popup"]["boton"].config(command=alternar_visibilidad_contraseña)

def nueva_carpeta(popup):
    nombre=popup["nombre"].get()
    clave=popup["clave"].get()

    if nombre and clave:
        clave=seguridad.crear_hash(clave)
        carpeta=carpetas.añadir_carpeta(datos,nombre,clave)
        almacenamiento.guardar_arca(carpeta)
        ui.refresh(P_carpetas["left"],datos,selecionar_carpeta)
        popup["popup"].destroy()
        Añadir.config(state="normal")

Icono_añadir=iconos.obtener_icono("añadir",2)

Añadir=tk.Button(P_carpetas["bot"], bg="black",fg="orange",image=Icono_añadir,
                 relief="flat",command=abrir_popup_nueva_carpeta)
Añadir.grid(row=0,column=0)


#============================BOTON SALIR DE APLICACION=========================================================================
Icono_salir=iconos.obtener_icono("salir",2)
Salir=tk.Button(P_carpetas["bot"], bg="black",fg="orange",image=Icono_salir,
                 relief="flat",command=lambda:cerrar())
Salir.grid(row=0,column=2)

#AREA BLOQUEADA=========================================================================================
















ventana.mainloop()