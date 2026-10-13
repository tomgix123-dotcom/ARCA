import os
import tkinter as tk
import config
from config import texto
import seguridad
import ui
from ui import botones_carpetas
from ui import barras_de_progreso
import ctypes
import carpetas
import fonts
import iconos
import almacenamiento
import protocolos
import atexit
from functools import partial
from cryptography.exceptions import InvalidTag
import threading

#///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
#=================================FUNCIONES VARIADAS===========================================================

def aviso_abiertas():

    #Comprobamos cuales estan abiertas y su numero
    cantidad = almacenamiento.cuantas_carpetas_desbloqueadas()

    if cantidad is None:
        return
    
    #eliminamos el aviso anterior
    aviso.grid_remove()

     #elegimos que aviso nuevo aparece segun la cantidad
    if cantidad == 0:
        return

    if cantidad == 1:
        aviso.grid(row=3,column=1,pady= 30)

        aviso.clave_idioma="aviso_carpeta_desbloqueada"
            
            
    elif cantidad > 1:
        aviso.grid(row=3,column=1,pady= 30)

        aviso.clave_idioma="aviso_carpetas_desbloqueadas"

    #configuramos el texto que se mostrara en el aviso, siendo este el que se haya elegido arriba
    aviso.valores_idioma={"cantidad":cantidad}
    aviso.config(text=texto(aviso.clave_idioma,cantidad=cantidad))
    
def mensaje_establecer_maestra():

    if not config.existe_config():

        mensaje=tk.Label(P_inicio["centro_bot"],text=texto("maestra"), font=("Px437 Acer VGA 8x8",12),
                           bg="black", fg="orange")
        mensaje.grid(row=2,column=1,pady= 30)
        mensaje.clave_idioma="maestra"

        return mensaje       

#/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
#=================================VENTANA PRINCIPAL============================================================

ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID("Tomgix.Arca")

ventana=ui.crear_ventana()
ventana.title("Arca")

fonts.cargar_fuentes()

almacenamiento.registrar_icono_arca()

ventana.iconbitmap(carpetas.obtener_ruta("Assets/ARCA.ico"))

#==================================DICCIONARIOS========================================================================

datos={"carpetas":[],"idioma":"Español","protocolos_activos":[]} #DATOS PROVIVISIONALES

llave_config = None

for carpeta in datos["carpetas"]:
        carpeta["sesion_desbloqueada"] = almacenamiento.carpeta_desbloqueada(carpeta)

config.idioma = config.cargar_idioma(datos["idioma"])

#==========[ PROTOCOLOS ACTIVADOS ]===============

#P.[01]
#atexit.register(partial(protocolos.ejecutar_P_01,datos))

#/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
#=================================PANEL DE INCIO======================================================================
P_inicio=ui.crear_P_incio(ventana)
P_inicio["panel"].pack(fill="both", expand=True)

aviso=ui.crear_aviso_abiertas(P_inicio["centro_bot"])
aviso_abiertas()
mensaje=mensaje_establecer_maestra()
#==================================BOTONES BARRA DE TAREAS========================================================

def abrir_popup_bloqueo_en_curso_P_inicio():

    if bloqueos_en_curso:
        ui.destruir_popups(P_carpetas,Salir)

        popup=ui.popup_aviso_bloqueo_en_curso(P_inicio["panel"],"#ffa500",3,"popup_aviso_bloqueo_en_curso")
        

        P_carpetas["popup"] = popup["borde"]
        P_carpetas["popup_boton"] = botones_carpeta["eliminar"]

        def cerrar_popup():
            popup["borde"].destroy()
            Salir.config(state="normal")

        popup["boton_aceptar"].configure(command=cerrar)
        popup["cancelar"].config(command=cerrar_popup)
        popup["x"].config(command=cerrar_popup)

    else:
        ventana.destroy()

def cerrar():
    ventana.destroy()
def minimizar():
    ventana.iconify()

#=============================================================
X=tk.Button(P_inicio["top"],bg="black",fg="orange",text="x",font=("Px437 ACM VGA 8x16",25),relief="flat",
            padx=0,pady=0,activebackground="#6E0000" ,command=abrir_popup_bloqueo_en_curso_P_inicio)
X.grid(row=0,column=2,sticky="ne")
#=============================================================
Minimizar=tk.Button(P_inicio["top"],bg="black",fg="orange",text="_",font=("Px437 ACM VGA 8x16",25),relief="flat",
            padx=0,pady=0,activebackground="#ffa500", command=minimizar)
Minimizar.grid(row=0,column=1,sticky="ne")
#==========================================================

#===ELEMENTOS DE LA PAGINA===========
def abrir_panel_idiomas():
    
    if panel_idiomas["panel_idiomas"].winfo_ismapped():
        panel_idiomas["panel_idiomas"].grid_remove()
    else:
        panel_idiomas["panel_idiomas"].grid()

def cambiar_idioma(i):

    config.idioma = config.cargar_idioma(i)
    ui.refresh_idiomas(ventana)

    datos["idioma"] = i
    config.guardar_json(datos,llave_config)

panel_idiomas=ui.crear_panel_idioma(P_inicio["top"],cambiar_idioma)
panel_idiomas["panel_idiomas"].grid_configure(row=0,column=1,sticky="nw",pady=11)
panel_idiomas["panel_idiomas"].grid_remove()
    

boton_idioma=ui.crear_boton_idioma(P_inicio["top"])
boton_idioma["boton"].grid(row=0,column=0,sticky="nw")
boton_idioma["boton"].configure(command=abrir_panel_idiomas)
##====================================TITULO========================================================================
Titulo=tk.Label(P_inicio["top"], text=texto("titulo"), bg="black", fg="orange",
                 font=("Kelvinized", 100, "underline"))
Titulo.place(relx=0.5, rely=0.5, anchor="center")
Titulo.clave_idioma="titulo"
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

def establecer_maestra():

    clave_maestra=Zona_Clave["entry"].get()
    Zona_Clave["entry"].delete(0, tk.END)
    mensaje.grid_forget()

    config.preparar_arca(clave_maestra)

def get_clave(Event=None):

    global llave_config

    if not config.existe_config():
        establecer_maestra()
        return

    contraseña_text=Zona_Clave["entry"].get()

    with open(config.ruta_config(),"rb") as archivo:
        archivo.read(5)
        salt= archivo.read(16)
    
        llave_temporal = seguridad.generar_llave(contraseña_text,salt)

    if config.existe_config():
        try:
            datos_leidos= config.leer_json(llave_temporal)

        except InvalidTag:
            incorrect_pass()
            return

        #ESTABLECE DE FORMA PERMANENTE QUE LOS DATOS OBTENIDOS SON CORRECTOS Y QUE SE PUEDE USAR ESTA INFORMACION DURANTE LA SESION
    
        datos.clear()
        datos.update(datos_leidos)

        llave_config = llave_temporal
    
        grant_acces()

def grant_acces():
    P_inicio["panel"].pack_forget()
    P_carpetas["carpetas"].pack(fill="both", expand=True)

    Zona_Clave["entry"].delete(0, tk.END)
    ui.mostrar_carpetas(P_carpetas["left"],P_carpetas["rigth bot"],datos,funcion=selecionar_carpeta)
    

def incorrect_pass():
    Borde_Error=ui.crear_borde(P_inicio["panel"],"#604013",6,6)
    Borde_Error.place(relx=0.5, rely=0.54,anchor="center")
    Error=tk.Label(Borde_Error,text=texto("clave_incorrecta"), font=("OCR-A BT",50),
                   bg="orange", fg="black")
    Error.clave_idioma="clave_incorrecta"
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
bienvenido=ui.crear_bienvenido(P_carpetas["rigth top"],datos)
icono_aprobado=ui.crear_icono_aprobado(P_carpetas["rigth top"])
#====================================


#////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
#=========================================AREA DE CARPETAS===================================================================
seleccion={}

def selecionar_carpeta(c):
    ui.destruir_popups(P_carpetas,Salir)

    seleccion["carpeta"]=c

    for barra_progreso in barras_de_progreso.values():
        ui.ocultar_barra_progreso(barra_progreso)

    id_carpeta = c["id"]
    barra_progreso = barras_de_progreso[id_carpeta]

    bienvenido.place_forget()
    panel_info["entry_contenido"].delete(0, tk.END)
    ui.actulizar_panel_info(panel_info,c)

    

    # Si la carpeta se está bloqueando, mostrar su barra
    if id_carpeta in bloqueos_en_curso:
        ui.ocultar_botones_carpeta(botones_carpeta)
        ui.ocultar_candado(candado)
        ui.ocultar_icono_aprobado(icono_aprobado)
        ui.mostrar_barra_progreso(barra_progreso)
        return

    else:

        if almacenamiento.carpeta_desbloqueada(c):
            candado.place_forget()
            ui.mostrar_botones_carpeta(botones_carpeta)
            panel_info["seccion_clave"].place_forget()
            ui.mostrar_icono_aprobado(icono_aprobado)


        else:
            botones_carpeta["frame"].pack_forget()
            ui.mostrar_candado_carpeta(candado)
            ui.ocultar_icono_aprobado(icono_aprobado)
            panel_info["seccion_clave"].place(relx=0.5,rely=0.5,anchor="center")
        
def informar_progreso(id_carpeta,progreso):

    barra_progreso = barras_de_progreso[id_carpeta]

    ventana.after(0,ui.actulizar_progreso,barra_progreso,progreso)

def abrir_popup_bloqueo_en_curso():

    if bloqueos_en_curso:
        ui.destruir_popups(P_carpetas,Salir)

        Salir.config(state="disabled")
        popup=ui.popup_aviso_bloqueo_en_curso(P_carpetas["carpetas"],"#ffa500",3,"popup_aviso_bloqueo_en_curso")
        

        P_carpetas["popup"] = popup["borde"]
        P_carpetas["popup_boton"] = botones_carpeta["eliminar"]

        def cerrar_popup():
            popup["borde"].destroy()
            Salir.config(state="normal")

        popup["boton_aceptar"].configure(command=cerrar)
        popup["cancelar"].config(command=cerrar_popup)
        popup["x"].config(command=cerrar_popup)

    else:
        ventana.destroy()

#//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
#================================AREA DE INFORMACION DE CARPETAS================================================
ui.mostrar_bienvenido(bienvenido)

desbloqueos_en_curso=set()
def iniciar_control_acceso(Event=None):

    carpeta = seleccion["carpeta"]
    id_carpeta = carpeta["id"]

    if id_carpeta in desbloqueos_en_curso:
        return

    desbloqueos_en_curso.add(id_carpeta)   

    hilo=threading.Thread(target=control_acceso,args=(carpeta,),daemon=True)
    hilo.start()

def control_acceso(Event=None):
    contraseña=seguridad.crear_hash(panel_info["entry_contenido"].get())

    carpeta = seleccion["carpeta"]
    id_carpeta = carpeta["id"]

    barra_progreso = barras_de_progreso[id_carpeta]

    hash= carpeta["clave"]

    if seguridad.check_hash(contraseña,hash) is True:

        try:
            ventana.after(0,ui.ocultar_candado(candado))
            ventana.after(0,ui.mostrar_barra_progreso(barra_progreso))
            almacenamiento.crear_carpeta_temp(carpeta,lambda progreso:informar_progreso(id_carpeta,progreso))
            
            if id_carpeta == seleccion["carpeta"]["id"]:

                candado.place_forget()
                ventana.after(0,ui.ocultar_barra_progreso(barra_progreso))
                ventana.after(0,ui.mostrar_botones_carpeta(botones_carpeta))
                panel_info["seccion_clave"].place_forget()
                ventana.after(0,ui.mostrar_icono_aprobado(icono_aprobado))
                panel_info["entry_contenido"].delete(0, tk.END)
                

        finally:
            desbloqueos_en_curso.discard(id_carpeta)

        icono=iconos.obtener_icono("aprobado",6)
        icono_pulsado=iconos.obtener_icono("aprobado_pulsado",6)

        boton = botones_carpetas[id_carpeta]
        boton.configure(image=icono)
        boton.image = icono

        boton.bind("<ButtonPress-1>", lambda e: boton.config(image=icono_pulsado))
        boton.bind("<ButtonRelease-1>", lambda e: boton.config(image=icono))

panel_info["entry_contenido"].bind("<Return>", iniciar_control_acceso)

#/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
#===================================BOTONES DE LAS CARPETAS===============================
#=========================================BOTON OJO========================================================
def alternar_visibilidad_contraseña_carpeta():

    ui.cambiar_estado_ojo(panel_info["boton_ojo_carpeta"])
    if panel_info["boton_ojo_carpeta"]["nombre_icono"] == "ojo":
        panel_info["entry_contenido"].configure(show="")

    elif panel_info["boton_ojo_carpeta"]["nombre_icono"] == "ojo_cerrado":
        panel_info["entry_contenido"].configure(show="*")

panel_info["boton_ojo_carpeta"]["boton"].configure(command=alternar_visibilidad_contraseña_carpeta)
#============================[ BLOQUEAR ]===================================

def iniciar_bloquear_all_carpetas():

    hilo = threading.Thread(target=bloquear_all_carpetas)
    hilo.start()

def bloquear_all_carpetas(Event=None):

    for carpeta in datos["carpetas"]:
        if almacenamiento.carpeta_desbloqueada(carpeta):
            almacenamiento.guardar_arca(carpeta,informar_progreso=None)
            almacenamiento.eliminar_carpeta_temp(carpeta)

    botones_carpeta["frame"].pack_forget()
    ui.mostrar_candado_carpeta(candado)
    icono_aprobado.place_forget()
    panel_info["seccion_clave"].place(relx=0.5,rely=0.5,anchor="center")

    ui.refresh(P_carpetas["left"],datos,selecionar_carpeta)

bloqueos_en_curso=set()
def iniciar_bloquear_carpeta(Event=None):

    carpeta = seleccion["carpeta"]
    id_carpeta = carpeta["id"]

    if id_carpeta in bloqueos_en_curso:
        return

    bloqueos_en_curso.add(id_carpeta)

    hilo =threading.Thread(target=bloquear_carpeta,args=(carpeta,),daemon=True)
    hilo.start()

def bloquear_carpeta(carpeta):

    ui.destruir_popups(P_carpetas,Salir)

    id_carpeta = carpeta["id"]
    barra_progreso = barras_de_progreso[id_carpeta]

    try:

        ventana.after(0,botones_carpeta["frame"].pack_forget())
        ventana.after(0,ui.mostrar_barra_progreso(barra_progreso))
        
        almacenamiento.guardar_arca(carpeta,lambda progreso:informar_progreso(id_carpeta,progreso))
        almacenamiento.eliminar_carpeta_temp(carpeta)

        ventana.after(0,ui.ocultar_barra_progreso(barra_progreso))

        if seleccion["carpeta"]["id"] == id_carpeta:
            ventana.after(0,panel_info["seccion_clave"].place(relx=0.5,rely=0.5,anchor="center"))

            icono_aprobado.place_forget()
            
            ui.mostrar_candado_carpeta(candado)
            ui.ocultar_barra_progreso(barra_progreso)
    finally:
        bloqueos_en_curso.discard(id_carpeta)
        
    

    icono= iconos.obtener_icono("carpeta",6)
    boton = botones_carpetas[id_carpeta]
    boton.configure(image=icono)
    boton.image = icono

botones_carpeta["bloquear"].configure(command=iniciar_bloquear_carpeta)
#=======================[ ELIMINAR ]===========================================
def eliminar_carpeta(popup):

    carpetas.quitar_carpeta(datos,seleccion["carpeta"],llave_config)
    almacenamiento.eliminar_carpeta_temp(seleccion["carpeta"])
    almacenamiento.eliminar_arca(seleccion["carpeta"])

    ui.refresh(P_carpetas["left"],datos,funcion=selecionar_carpeta)
    ui.ocultar_panel_info(panel_info)
    ui.ocultar_icono_aprobado(icono_aprobado)
    ui.mostrar_bienvenido(bienvenido)

    popup["borde"].destroy()
    botones_carpeta["eliminar"].config(state="normal")
    botones_carpeta["frame"].pack_forget()

def abrir_popup_aviso_eliminar():
    ui.destruir_popups(P_carpetas,Salir)

    botones_carpeta["eliminar"].config(state="disable")
    popup=ui.popup_aviso_eliminar(P_carpetas["carpetas"],"orange",3,"popup_eliminar")
    

    P_carpetas["popup"] = popup["borde"]
    P_carpetas["popup_boton"] = botones_carpeta["eliminar"]

    def cerrar():
        popup["borde"].destroy()
        botones_carpeta["eliminar"].config(state="normal")

    popup["boton_aceptar"].configure(command=lambda:eliminar_carpeta(popup))
    popup["cancelar"].config(command=cerrar)
    popup["x"].config(command=cerrar)

botones_carpeta["eliminar"].configure(command=abrir_popup_aviso_eliminar)
#=========================[ ABRIR ]============================================
def abrir_carpeta(Event=None):
    ruta_carpeta_temp= os.path.join(config.RUTA_SESSIONS,seleccion["carpeta"]["id"])

    ventana.iconify()
    os.startfile(ruta_carpeta_temp)

botones_carpeta["abrir"].configure(command=abrir_carpeta)
#==========================[ RENOMBRAR ]===========================================
def renombrar_carpeta(popup):
    nuevo_nombre=popup["nuevo_nombre"].get()

    if nuevo_nombre:
        seleccion["carpeta"]["nombre"] = nuevo_nombre
        config.guardar_json(datos,llave_config)    
        ui.refresh(P_carpetas["left"],P_carpetas["rigth bot"],datos,selecionar_carpeta)
        panel_info["nombre"].config(text=nuevo_nombre)
        popup["borde"].destroy()
        botones_carpeta["renombrar"].config(state="normal")

        icono = iconos.obtener_icono("aprobado", 6)

        id_carpeta = seleccion["carpeta"]["id"]
        boton = botones_carpetas[id_carpeta]

        boton.configure(image=icono)
        boton.image = icono

        

def abrir_popup_renombrar(Event=None):
    ui.destruir_popups(P_carpetas,Salir)

    botones_carpeta["renombrar"].config(state="disabled")
    popup=ui.popup_renombrar(P_carpetas["carpetas"],"orange", 3,"popup_renombrar")
    

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

    ui.destruir_popups(P_carpetas,Salir)

    popup=ui.crear_popup_nueva_carpeta(P_carpetas["carpetas"],"orange",3,"popup_nueva_carpeta")
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
        carpeta=carpetas.añadir_carpeta(datos,nombre,clave,llave_config)
        almacenamiento.guardar_arca(carpeta,informar_progreso=None)
        ui.refresh(P_carpetas["left"],P_carpetas["rigth bot"],datos,selecionar_carpeta)
        popup["popup"].destroy()
        Añadir.config(state="normal")

Icono_añadir=iconos.obtener_icono("añadir",2)
Icono_añadir_pulsado = iconos.obtener_icono("añadir_pulsado",2)

#===========================================
Añadir=tk.Button(P_carpetas["bot"], bg="black",fg="orange",image=Icono_añadir,
                 relief="flat",command=abrir_popup_nueva_carpeta,activebackground="orange")
Añadir.grid(row=0,column=2)
#===========================================

Añadir.bind("<ButtonPress-1>", lambda e: Añadir.config(image=Icono_añadir_pulsado))
Añadir.bind("<ButtonRelease-1>", lambda e: Añadir.config(image=Icono_añadir))

#============================BOTON SALIR DE APLICACION=========================================================================
Icono_salir=iconos.obtener_icono("salir",2)
Icono_salir_pulsado=iconos.obtener_icono("salir_pulsado",2)

#===========================================
Salir=tk.Button(P_carpetas["bot"], bg="black",fg="orange",image=Icono_salir,
                 relief="flat",command=abrir_popup_bloqueo_en_curso,activebackground="orange")
Salir.grid(row=0,column=3)
#==========================================

Salir.bind("<ButtonPress-1>", lambda e: Salir.config(image=Icono_salir_pulsado))
Salir.bind("<ButtonRelease-1>", lambda e: Salir.config(image=Icono_salir))
#========================================BOTON PARA VOLVER=================================================================
def volver():
    P_carpetas["carpetas"].pack_forget()
    P_inicio["panel"].pack(fill="both", expand=True)
    #iniciar_bloquear_all_carpetas()
    aviso_abiertas()
    Zona_Clave["entry"].delete(0, tk.END)

Icono_volver= iconos.obtener_icono("volver",2)
Icono_volver_pulsado= iconos.obtener_icono("volver_pulsado",2)

#===========================================
Volver=tk.Button(P_carpetas["bot"], bg="black",fg="orange",image=Icono_volver,
                 relief="flat",command=volver,activebackground="orange")
Volver.grid(row=0,column=1)
#===========================================

Volver.bind("<ButtonPress-1>", lambda e: Volver.config(image=Icono_volver_pulsado))
Volver.bind("<ButtonRelease-1>", lambda e: Volver.config(image=Icono_volver))















ventana.mainloop()