import tkinter as tk
from tkinter import ttk
import iconos
import config
import carpetas
import seguridad
import almacenamiento
#COLORES
"#ffa500" #NARANJA PREDETERMINADO
"#0059ff" #COMPLEMENTARIO DEL NARANJA
"#ff2600" #ROJO QUE PEGA CON COSAS RESTRINGIDAS





def crear_ventana():

    ventana=tk.Tk()
    ventana.title("Arca")
    ventana.attributes("-fullscreen", True)
    
    
    return ventana

#//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
#===============================AREA DE INICIO===============================================================================
def crear_P_incio(ventana):
    P_inicio= tk.Frame(ventana, bg="black")
    
    P_inicio.grid_rowconfigure(0, weight=1)
    P_inicio.grid_columnconfigure(0, weight=1)

    P_inicio_top=tk.Frame(P_inicio, bg="black")
    P_inicio_top.grid(row=0, column=0, sticky="nsew")
    P_inicio_top.grid_rowconfigure(0,weight=1)
    P_inicio_top.grid_columnconfigure(0,weight=1)

    P_inicio.grid_rowconfigure(0, weight=1)
    P_inicio.grid_rowconfigure(1, weight=0)
    P_inicio.grid_rowconfigure(2, weight=1)
    
    P_inicio_bottom=tk.Frame(P_inicio, bg="black")
    P_inicio_bottom.grid(row=1, column=0, sticky="nsew")
    P_inicio_bottom.grid_columnconfigure(0, weight=178)
    P_inicio_bottom.grid_columnconfigure(1, weight=0)
    P_inicio_bottom.grid_columnconfigure(2, weight=150)

    P_inicio_superbot=tk.Frame(P_inicio, bg="black")
    P_inicio_superbot.grid(row=2, column=0, sticky="nsew")
    P_inicio_superbot.grid_columnconfigure(0, weight=1)
    P_inicio_superbot.grid_columnconfigure(1, weight=0)
    P_inicio_superbot.grid_columnconfigure(2, weight=1)

    Centro_bottom=tk.Frame(P_inicio_bottom, bg="black") 
    Centro_bottom.grid(row=0, column=1, sticky="nsew")

    Centro_superbot=tk.Frame(P_inicio_superbot, bg="black")
    Centro_superbot.grid(row=0, column=1, sticky="nsew")
   

    return{"panel": P_inicio, "top":P_inicio_top, "bot":P_inicio_bottom,
           "centro":Centro_bottom,"centro_bot":Centro_superbot}

#==================================
def crear_zona_clave(parent):
    Clave_label=tk.Label(parent, text="Clave:", bg="black", fg="orange",
                        font=("Px437 Acer VGA 8x8", 15))
    

    Borde_Clave_Entry=crear_borde(parent,"orange", 2,2)
    

    Clave_Entry=tk.Entry(Borde_Clave_Entry, bg="black", fg="orange",
                        font=("Px437 Acer VGA 8x8", 15), relief="flat", insertwidth=5,
                        insertbackground="orange", borderwidth=10,justify="center")

    
    return {"label":Clave_label,"borde":Borde_Clave_Entry, "entry":Clave_Entry}
    
def crear_boton_ojo(parent,escala=4):

    nombre_icono = "ojo"

    icono= iconos.obtener_icono(nombre_icono,escala)
    icono.imagen = icono

    Boton_ojo=tk.Button(parent, bg="black",fg="orange",relief="flat", image=icono,activebackground="black")

    return {"boton":Boton_ojo,"nombre_icono":nombre_icono}

def cambiar_estado_ojo(Boton_ojo):

    if Boton_ojo["nombre_icono"] == "ojo":
        Boton_ojo["nombre_icono"] = "ojo_cerrado"
    else:
        Boton_ojo["nombre_icono"] = "ojo"

    icono = iconos.obtener_icono(Boton_ojo["nombre_icono"], 4)
    icono.imagen = icono

    Boton_ojo["boton"].configure(image=icono)

#///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
#=================================AREA DE CARPETAS====================================================================
def crear_PCarpetas(ventana):
    P_carpetas= tk.Frame(ventana, bg="black")

    P_carpetas.grid_columnconfigure(0, weight=1)
    P_carpetas.grid_columnconfigure(1, weight=0)
    P_carpetas.grid_columnconfigure(2, weight=5)

    P_carpetas.grid_rowconfigure(0, weight=1)
    P_carpetas.grid_rowconfigure(1, weight=30)
    P_carpetas.grid_rowconfigure(2, weight=0)
    P_carpetas.grid_rowconfigure(3, weight=1)

    rectangulo=tk.Frame(P_carpetas,bg="orange")
    rectangulo.grid_columnconfigure(1,weight=1)
    rectangulo.grid_columnconfigure(2,weight=0)
    rectangulo.grid_columnconfigure(3,weight=0)
    rectangulo.grid(row=0,column=0,columnspan=3,sticky="news")
    


#=================IZQUIERDA==============================================
    canvas=tk.Canvas(P_carpetas, bg="black",highlightthickness=0)
    canvas.grid(row=1, column=0, sticky="news")
    P_carL=tk.Frame(canvas,bg="black")
    

    ventana_canvas= canvas.create_window((0, 0), window=P_carL, anchor="nw")

    def ajustar_ancho(event):
        canvas.itemconfigure(ventana_canvas,width= event.width)

    canvas.bind("<Configure>",ajustar_ancho)
    P_carL.bind("<Configure>",lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

    def rueda(event):
        canvas.yview_scroll(-event.delta // 120,"units")

    def entrar_canvas(event):
        canvas.bind_all("<MouseWheel>", rueda)
    def salir_canvas(event):
        canvas.unbind_all("<MouseWheel>")

    canvas.bind("<Enter>", entrar_canvas)
    canvas.bind("<Leave>", salir_canvas) 

    Sep_Lvertical=crear_separador(P_carpetas,orientacion="v")
    Sep_Lvertical.grid(row=1, column=1, sticky="ns")

#======================DERECHA============================================
    P_carR=tk.Frame(P_carpetas, bg="black")
    P_carR.grid(row=1, column=2, sticky="wesn")

    P_carR.grid_rowconfigure(0, weight=3)
    P_carR.grid_rowconfigure(1, weight=0)
    P_carR.grid_rowconfigure(2, weight=1)
    P_carR.grid_columnconfigure(0, weight=1)
    P_carR.grid_propagate(False)
#====================DERECHA/ARRIBA===================================
    P_carR_top=tk.Frame(P_carR, bg="black")
    P_carR_top.grid(row=0, column=0, sticky="news")

#=======================SEPARADOR==================================
    sep_Rhorizontal=crear_separador(P_carR)
    sep_Rhorizontal.grid(row=1, column=0, sticky="we")
#======================DERECHA/ABAJO====================================
    P_carR_bot=tk.Frame(P_carR, bg="black")
    P_carR_bot.grid(row=2, column=0, sticky="wesn")

#====================ABAJO=========================================
    sep_CarB=crear_separador(P_carpetas)
    sep_CarB.grid(row=2,column=0, sticky="we", columnspan=3)

    P_car_bot=tk.Frame(P_carpetas, bg="black")
    P_car_bot.grid(row=3, column=0, sticky="ew",columnspan=3)

    

#================RESULTADO===================================================================
    return{"left":P_carL,"rigth":P_carR,"bot":P_car_bot, "carpetas":P_carpetas,
           "rigth top":P_carR_top, "rigth bot":P_carR_bot,"barra_tareas":rectangulo,"popup":None,
           "popup_boton":None}


#DIBUJA LAS CARPETAS EN LA "UBICACION"(FRAME) QUE LE PONGAS, USANDO LOS "DATOS" DEL DICCIONARIO. 
def mostrar_carpetas(ubicacion,datos,funcion):
    for fila,carpeta in enumerate(datos["carpetas"]):

        if carpeta.get("sesion_recuperada",False):
            icono=iconos.obtener_icono("aviso",6)
        else:
            icono=iconos.obtener_icono("carpeta",6)
        
        boton_carpeta=tk.Button(ubicacion,text=carpeta["nombre"], bg="black",fg="orange",
                               relief="flat", font=("Px437 Acer VGA 8x8",16), image=icono,
                               compound="left", padx= 18, command=lambda c=carpeta:funcion(c))
        boton_carpeta.image=icono
        boton_carpeta.grid(row=fila,column=0, padx=10, sticky="w")    
    
#DESTRUYE TODOS LOS WIDGETS DE UN FRAME Y LLAMA A MOSTRAR_CARPETAS PARA VOLVER A DIBUJARLAS
def refresh(ubicacion,datos,funcion):
    
    for widget in ubicacion.winfo_children():
        widget.destroy()
    mostrar_carpetas(ubicacion,datos,funcion)  

#///////////////////////////////////////////////////////////////////////////////////////////////////////////////////
#=================================AREA DEL PANEL INFO===============================================================
def crear_panel_info(ubi_info):

    #Configura columnas para que todo este alineado como necesito.(si algo se mueve raro o no hace lo que quieres comprueba que todo este bien aqui)
    ubi_info.grid_columnconfigure(0,weight=0)
    ubi_info.grid_columnconfigure(1,weight=1)

    #Crea un campo de texto con su respetivo label para colocarlo todo juntito en un frame sin que el grid haga cosas raras con los dos elementos, asi siempre estan juntos.
    def crear_campo(parent,texto):

       Boton_ojo_carpeta= crear_boton_ojo(parent)
       Boton_ojo_carpeta["boton"].grid(row=1,column=1)

       label=tk.Label(parent,bg="black",fg="orange",font=("Px437 Acer VGA 8x8",25),text=texto)
       label.grid(row=0,column=0)

       borde=crear_borde(parent,"orange",2,2)
       entry=tk.Entry(borde,bg="black", fg="orange",
                        font=("Px437 Acer VGA 8x8", 20), relief="flat", insertwidth=5,
                        insertbackground="orange", borderwidth=10,justify="center")
       entry.pack()
       borde.grid(row=1,column=0)

       return {"entry":entry,"boton_ojo_carpeta":Boton_ojo_carpeta}


    #Crea el icono que va junto al nombre.(siempre es el mismo icono, se mantendra asi hasta que Arca funcione y luego mejorare para que cambie segun el estado de la carpeta)
    icono=iconos.obtener_icono("carpeta_estado",2)
    icono_carpeta=tk.Label(ubi_info,image=icono,bg="black")
    icono_carpeta.image=icono
    

    #Crea el nombre de la carpeta seleccionada.
    Nombre=tk.Label(ubi_info,bg="black",fg="orange",font=("Px437 Acer VGA 8x8",25),text="",
                    wraplength=600,justify="left")
    

    #Crea el separador.
    separador=crear_separador(ubi_info,linea="-")
    

   #Crea la zona del entry.
    seccion_clave= tk.Frame(ubi_info,bg="black")
    Entry= crear_campo(seccion_clave,"Clave")
    

    return{"nombre":Nombre,"seccion_clave":seccion_clave,"entry_contenido":Entry["entry"],
           "boton_ojo_carpeta":Entry["boton_ojo_carpeta"],"icono":icono_carpeta,
           "separador":separador}

def mostrar_panel_info(panel_info):
    panel_info["icono"].grid(row=0,column=0,sticky="wn")
    panel_info["nombre"].grid(row=0,column=1,sticky="ws")
    panel_info["seccion_clave"].place(relx=0.5,rely=0.5,anchor="center")
    panel_info["separador"].grid(row=1,column=0,columnspan=2,sticky="ew")

def ocultar_panel_info(panel_info):
    panel_info["icono"].grid_forget()
    panel_info["nombre"].grid_forget()
    panel_info["seccion_clave"].place_forget()
    panel_info["separador"].grid_forget()
    
def actulizar_panel_info(panel_info,carpeta):

    mostrar_panel_info(panel_info)
    panel_info["nombre"].config(text=carpeta["nombre"])

#////////////////////////////////////////////////////////////////////////////////////////////////////////////////////


#==========================BIENVENIDO==================================
def crear_bienvenido(parent):
    bienvenido=tk.Label(parent, text="-Bienvenido, seleccione una carpeta.-", bg="black", fg="orange",
                        font=("Px437 Acer VGA 8x8", 15,))
       

    return bienvenido 

def mostrar_bienvenido(bienvenido):
    bienvenido.place(relx=0.5,rely=0.52,anchor="center")
#======================================================================

def crear_icono_aprobado(parent):
   icono= iconos.obtener_icono("aprobado",1)
   icono_aprobado = tk.Label(parent,image=icono,bg="black")
   icono_aprobado.image=icono

   return icono_aprobado

def mostrar_icono_aprobado(icono_aprobado):
    icono_aprobado.place(relx=0.5,rely=0.6,anchor="center")

def ocultar_icono_aprobado(icono_aprobado):
    icono_aprobado.place_forget()


#/////////////////////////////////////////////////////////////////////////////////////////////////////
#======================LOS BOTONES Y EL CANDADO QUE TIENEN LAS CARPETAS===============================
def crear_botones_carpeta(parent):

    frame = tk.Frame(parent, bg="black")
    frame.grid_columnconfigure(0,weight=1)
    frame.grid_columnconfigure(1,weight=0)
    frame.grid_columnconfigure(2,weight=1)

    frame.grid_rowconfigure(0,weight=1)
    frame.grid_rowconfigure(1,weight=0)
    frame.grid_rowconfigure(2,weight=1)

    frame_centro=tk.Frame(frame,bg="black")
    

    boton_abrir=tk.Button(frame_centro, bg="black",fg="orange",relief="flat", text="Abrir",
                          font=("Px437 Acer VGA 8x8",18))
    boton_renombrar=tk.Button(frame_centro, bg="black",fg="orange",relief="flat", text="Renombrar",
                              font=("Px437 Acer VGA 8x8",18))
    boton_eliminar=tk.Button(frame_centro, bg="black",fg="orange",relief="flat",text="Eliminar",
                             font=("Px437 Acer VGA 8x8",18))
    boton_bloquear=tk.Button(frame_centro, bg="black",fg="orange",relief="flat", text="Bloquear",
                          font=("Px437 Acer VGA 8x8",18))

    

    return {"frame":frame,"frame_centro":frame_centro,"abrir":boton_abrir,"renombrar":boton_renombrar,"eliminar":boton_eliminar,
            "bloquear":boton_bloquear}

def mostrar_botones_carpeta(botones_carpeta):
        botones_carpeta["frame"].pack(fill="both",expand=True)
        botones_carpeta["frame_centro"].grid(row=1,column=1)
        botones_carpeta["abrir"].grid(row=0,column=0,padx=10)
        botones_carpeta["renombrar"].grid(row=0,column=1,padx=10)
        botones_carpeta["eliminar"].grid(row=0,column=2,padx=10)
        botones_carpeta["bloquear"].grid(row=0, column=3,padx=10)

#=========================================================================================================================
def crear_candado_carpeta(parent):
    icono=iconos.obtener_icono("bloqueado",2)
    candado_icono=tk.Label(parent,image=icono,bg="black")
    candado_icono.image =icono

    return candado_icono

def mostrar_candado_carpeta(candado):
    candado.place(relx=0.5,rely=0.5,anchor="center")

def ocultar_candado(candado):
    candado.place_forget()


#////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

  

#CREA UN BORDE RAPIDO ALREDEDOR DE UN SOLO WIDGET. EL WIDGET SE .PACK DENTRO DEL BORDE Y ES EL BORDE
#EL QUE SE PONE COMO SI FUERA EL WIDGET.
def crear_borde(parent,color,x,y):
    Borde=tk.Frame(parent, bg=color, padx=x, pady=y)
    return Borde


#===============GENERA UNA PLANTILLA DE POPUP PARA TRABAJAR CON ELLA=======================
def crear_popup(parent,color,grosor,nombre_ventana):
    borde=tk.Frame(parent,bg=color)

    interior=tk.Frame(borde,bg="black")
    interior.pack(fill="both",expand=True,padx=grosor,pady=grosor)

    interior.grid_columnconfigure(0,weight=1)

    interior.grid_rowconfigure(0,weight=1)
    interior.grid_rowconfigure(1,weight=1)
    interior.grid_rowconfigure(2,weight=1)
    

    top=tk.Frame(interior,bg="black")
    top.grid(row=0,column=0,sticky="news")

    top.grid_columnconfigure(0,weight=1)

    bot=tk.Frame(interior,bg="black")
    bot.grid(row=1,column=0,sticky="news")
    superbot=tk.Frame(interior,bg="black")
    superbot.grid(row=2,column=0,sticky="news")
    
    bot.grid_columnconfigure(0,weight=25)
    bot.grid_columnconfigure(1,weight=0)
    bot.grid_columnconfigure(2,weight=15)
    superbot.grid_columnconfigure(0,weight=1)
    superbot.grid_columnconfigure(1,weight=0)
    superbot.grid_columnconfigure(2,weight=1)

    centro_bot=tk.Frame(bot,bg="black")
    centro_bot.grid(row=0,column=1,sticky="news")
    
    
    nombre=tk.Label(top,bg="black",fg="orange",font=("Px437 Acer VGA 8x8",10),text=nombre_ventana)
    nombre.grid(row=0,column=0,sticky="w")


    X=tk.Button(top,bg="black",fg="orange",text="x",font=("Px437 ACM VGA 8x16",15),relief="flat",
            padx=0,pady=0)
    X.grid(row=0,column=1,sticky="en")

    separador=crear_separador(top)
    separador.grid(row=1,column=0,sticky="ew",columnspan=2)


    borde.place(relx=0.5,rely=0.4,anchor="center",width=700,height=500)

    return{"borde":borde,"interior":interior,"top":top,"bot":bot,"centro":centro_bot,"superbot":superbot,
           "x":X}

def crear_popup_mediano(parent,color,grosor,nombre_ventana):
    borde=tk.Frame(parent,bg=color)

    interior=tk.Frame(borde,bg="black")
    interior.pack(fill="both",expand=True,padx=grosor,pady=grosor)

    interior.grid_columnconfigure(0,weight=1)

    interior.grid_rowconfigure(0,weight=1)
    interior.grid_rowconfigure(1,weight=1)
    interior.grid_rowconfigure(2,weight=1)
    

    top=tk.Frame(interior,bg="black")
    top.grid(row=0,column=0,sticky="news")

    top.grid_columnconfigure(0,weight=1)

    bot=tk.Frame(interior,bg="black")
    bot.grid(row=1,column=0,sticky="news")
    superbot=tk.Frame(interior,bg="black")
    superbot.grid(row=2,column=0,sticky="news")
    
    bot.grid_columnconfigure(0,weight=1)
    bot.grid_columnconfigure(1,weight=0)
    bot.grid_columnconfigure(2,weight=1)
    superbot.grid_columnconfigure(0,weight=1)
    superbot.grid_columnconfigure(1,weight=0)
    superbot.grid_columnconfigure(2,weight=1)

    centro_bot=tk.Frame(bot,bg="black")
    centro_bot.grid(row=0,column=1,sticky="news")
    
    
    nombre=tk.Label(top,bg="black",fg="orange",font=("Px437 Acer VGA 8x8",10),text=nombre_ventana)
    nombre.grid(row=0,column=0,sticky="w")


    X=tk.Button(top,bg="black",fg="orange",text="x",font=("Px437 ACM VGA 8x16",15),relief="flat",
            padx=0,pady=0)
    X.grid(row=0,column=1,sticky="en")

    separador=crear_separador(top)
    separador.grid(row=1,column=0,sticky="ew",columnspan=2)


    borde.place(relx=0.5,rely=0.4,anchor="center",width=700,height=350)

    return{"borde":borde,"interior":interior,"top":top,"bot":bot,"centro":centro_bot,"superbot":superbot,
           "x":X}

def crear_popup_chiquito(parent,color,grosor,nombre_ventana):
    borde=tk.Frame(parent,bg=color)

    interior=tk.Frame(borde,bg="black")
    interior.pack(fill="both",expand=True,padx=grosor,pady=grosor)

    interior.grid_columnconfigure(0,weight=1)

    interior.grid_rowconfigure(0,weight=1)
    interior.grid_rowconfigure(1,weight=1)
    interior.grid_rowconfigure(2,weight=1)
    

    top=tk.Frame(interior,bg="black")
    top.grid(row=0,column=0,sticky="news")

    top.grid_columnconfigure(0,weight=1)

    bot=tk.Frame(interior,bg="black")
    bot.grid(row=1,column=0,sticky="news")
    superbot=tk.Frame(interior,bg="black")
    superbot.grid(row=2,column=0,sticky="news")
    
    bot.grid_columnconfigure(0,weight=1)
    bot.grid_columnconfigure(1,weight=0)
    bot.grid_columnconfigure(2,weight=1)
    superbot.grid_columnconfigure(0,weight=1)
    superbot.grid_columnconfigure(1,weight=0)
    superbot.grid_columnconfigure(2,weight=1)

    centro_bot=tk.Frame(bot,bg="black")
    centro_bot.grid(row=0,column=1,sticky="news")
    
    
    nombre=tk.Label(top,bg="black",fg="orange",font=("Px437 Acer VGA 8x8",10),text=nombre_ventana)
    nombre.grid(row=0,column=0,sticky="w")


    X=tk.Button(top,bg="black",fg="orange",text="x",font=("Px437 ACM VGA 8x16",15),relief="flat",
            padx=0,pady=0)
    X.grid(row=0,column=1,sticky="en")

    separador=crear_separador(top)
    separador.grid(row=1,column=0,sticky="ew",columnspan=2)


    borde.place(relx=0.5,rely=0.4,anchor="center",width=700,height=200)

    return{"borde":borde,"interior":interior,"top":top,"bot":bot,"centro":centro_bot,"superbot":superbot,
           "x":X}

#//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
#===========DEFINE EL POPUP PARA CREAR NUEVAS CARPETAS=====================================
def crear_popup_nueva_carpeta(parent,color,grosor,nombre_ventana):
    popup=crear_popup(parent,color,grosor,nombre_ventana)
    

    def crear_campo(parent,texto):
        
       label=tk.Label(parent,bg="black",fg="orange",font=("Px437 Acer VGA 8x8",18),text=texto)
       label.grid(row=0,column=0)

       borde=crear_borde(parent,"orange",2,2)
       entry=tk.Entry(borde,bg="black", fg="orange",
                        font=("Px437 Acer VGA 8x8", 15), relief="flat", insertwidth=5,
                        insertbackground="orange", borderwidth=10,justify="center")
       entry.pack()
       borde.grid(row=1,column=0)

       return {"entry":entry,"borde":borde}
    #============NOMBRE==========================================================================================
    seccion_nombre=tk.Frame(popup["centro"],bg="black")
    entry_nombre=crear_campo(seccion_nombre,"Nombre")
  
    #==============CLAVE==========================================================================================
    seccion_clave=tk.Frame(popup["centro"],bg="black")
    entry_clave=crear_campo(seccion_clave,"Clave")

    Boton_ojo_popup= crear_boton_ojo(seccion_clave)
    Boton_ojo_popup["boton"].grid(row=1,column=1)
    #===============BOTONES====================================================================================
    seccion_botones=tk.Frame(popup["superbot"],bg="black")

    borde_crear=crear_borde(seccion_botones,"orange",2,2)
    Crear=tk.Button(borde_crear, bg="black",fg="orange",text="Crear Carpeta", font=("Px437 Acer VGA 8x8",15),
                 relief="flat")
    Crear.pack()


    borde_cancelar=crear_borde(seccion_botones,"orange",2,2)
    Cancelar=tk.Button(borde_cancelar, bg="black",fg="orange",text="Cancelar", font=("Px437 Acer VGA 8x8",15),
                 relief="flat")
    Cancelar.pack()
    
    return{"nombre":entry_nombre["entry"],"clave":entry_clave["entry"],"crear":Crear,"popup":popup["borde"],
           "borde_cancelar":borde_cancelar,"borde_crear":borde_crear,"seccion_clave":seccion_clave,
           "seccion_botones":seccion_botones,"seccion_nombre":seccion_nombre,"cancelar":Cancelar,
           "x":popup["x"],"borde":popup["borde"],"boton_ojo_popup":Boton_ojo_popup}    

def mostrar_popup_nueva_carpeta(popup):
    popup["borde_cancelar"].grid(row=0,column=1,pady=40,padx=50)
    popup["borde_crear"].grid(row=0,column=0,pady=40)
    popup["seccion_clave"].grid(row=1,column=0,sticky="news", pady=40)
    popup["seccion_botones"].grid(row=0,column=1)
    popup["seccion_nombre"].grid(row=0,column=0,sticky="news",pady=40)
    
#//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
#===========DEFINE EL POPUP PARA LA FUNCION DE RENOMBRAR======================================
def popup_renombrar(parent,color,grosor,nombre_ventana):
    popup=crear_popup_mediano(parent,color,grosor,nombre_ventana)


    def crear_campo(parent,texto):
    
           label=tk.Label(parent,bg="black",fg="orange",font=("Px437 Acer VGA 8x8",18),text=texto)
           label.grid(row=0,column=0)
    
           borde=crear_borde(parent,"orange",2,2)
           entry=tk.Entry(borde,bg="black", fg="orange",
                            font=("Px437 Acer VGA 8x8", 15), relief="flat", insertwidth=5,
                            insertbackground="orange", borderwidth=10,justify="center")
           entry.pack()
           borde.grid(row=1,column=0)
    
           return entry

    #===================SECCION DE RENOMBRAR================================================
    seccion_renombrar=tk.Frame(popup["centro"],bg="black")
    entry_renombrar=crear_campo(seccion_renombrar,"Renombrar")
    
    seccion_renombrar.grid(row=1,column=0,sticky="news", pady=20)

    #==================SECCION DE BOTONES===================================================
    seccion_botones=tk.Frame(popup["superbot"],bg="black")
    seccion_botones.grid(row=0,column=1)
    
    borde_renombrar=crear_borde(seccion_botones,"orange",2,2)
    boton_renombrar=tk.Button(borde_renombrar, bg="black",fg="orange",text="Renombrar", font=("Px437 Acer VGA 8x8",15),
                     relief="flat")
    boton_renombrar.pack()
    borde_renombrar.grid(row=0,column=0,pady=40)
    
    
    borde_cancelar=crear_borde(seccion_botones,"orange",2,2)
    Cancelar=tk.Button(borde_cancelar, bg="black",fg="orange",text="Cancelar", font=("Px437 Acer VGA 8x8",15),
                     relief="flat")
    Cancelar.pack()
    borde_cancelar.grid(row=0,column=1,pady=40,padx=50)

    return {"boton_renombrar":boton_renombrar,"cancelar":Cancelar,"nuevo_nombre":entry_renombrar,"borde":popup["borde"],
            "x":popup["x"]}

#///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
#=============================POPUP AVISO ANTES DE ELIMINAR===============================================================
def popup_aviso_eliminar(parent,color,grosor,nombre_ventana):
    popup=crear_popup_chiquito(parent,color,grosor,nombre_ventana)

    mensaje_aviso=tk.Label(popup["centro"],bg="black",fg="orange",font=("Px437 Acer VGA 8x8",12),
                   text="¿Seguro que desea eliminar la carpeta?",wraplength=800)
    mensaje_aviso.grid(row=0,column=0)

    borde_aceptar=crear_borde(popup["superbot"],"orange",2,2)
    boton_aceptar=tk.Button(borde_aceptar, bg="black",fg="orange",text="Aceptar", font=("Px437 Acer VGA 8x8",12),
                     relief="flat")
    boton_aceptar.pack()
    borde_aceptar.grid(row=0,column=0,padx=50)


    borde_cancelar=crear_borde(popup["superbot"],"orange",2,2)
    Cancelar=tk.Button(borde_cancelar, bg="black",fg="orange",text="Cancelar", font=("Px437 Acer VGA 8x8",12),
                         relief="flat")
    Cancelar.pack()
    borde_cancelar.grid(row=0,column=1)

    return{"boton_aceptar":boton_aceptar,"borde":popup["borde"],"cancelar":Cancelar,"x":popup["x"]}

#/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
#===================================DESTRUYE TODOS LOS POPUPS==============================================================
def destruir_popups(P_carpetas):
    popup = P_carpetas["popup"]

    if popup is not None:
        popup.destroy()

        P_carpetas["popup_boton"].config(state="normal")

        P_carpetas["popup"] = None
        P_carpetas["popup_boton"] = None



#CREA UN SEPARADOR QUE PUEDES COLOCAR COMO UN WIDGET, SE PUEDE ELEGIR LA LINEA PERO NO CREO QUE FUNCIONE EN VERTICAL.
def crear_separador(frame,linea="=",orientacion="h"):
    
     if orientacion == "h":
        canvas = tk.Canvas(frame,height=10,bg="black", highlightthickness=0,bd=0)
        def redibujar(event):
            canvas.delete("all")
            ancho=event.width
            cantidad=ancho//9 +2
            canvas.create_text(0,5,anchor="w",text=linea*cantidad,font=("Courier New",15),fill="orange")
        canvas.bind("<Configure>",redibujar)
        return canvas
     else:
         canvas = tk.Canvas(frame,width=10,bg="black", highlightthickness=0,bd=0)
         def redibujar(event):
             canvas.delete("all")
             alto=event.height
             cantidad=alto//16+2
             
             canvas.create_text(5,0,anchor="n",text=("║"+"\n")*cantidad,font=("Courier New",15),fill="orange")
         canvas.bind("<Configure>",redibujar)
         return canvas
         

    



    
