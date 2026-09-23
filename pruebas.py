import ui
import tkinter as tk
import config
import iconos
import fonts
datos=config.leer_json()
ventana=ui.crear_ventana()
iconos.cargar_iconos()
fonts.cargar_fuentes()
P_carpetas=ui.crear_PCarpetas(ventana)
P_carpetas["carpetas"].pack(fill="both", expand=True)

ui.mostrar_carpetas(P_carpetas["left"],P_carpetas["rigth top"],datos)

Borde_ventana_carpeta=ui.crear_borde(P_carpetas["carpetas"],"orange",2,2)
popup=ui.crear_popup(P_carpetas["carpetas"],"orange",2,"Nueva Carpeta")





ventana.mainloop()