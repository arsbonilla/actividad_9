# -*- coding: utf-8 -*-
"""
Created on Sun Mar 28 17:32:17 2021

@author: Luna_21
"""
###abrir imagenes

import tkinter
from tkinter import filedialog

ventana= tkinter.Tk()
ventana.geometry("600x600")
#implementacion de las funciones que implementaran la ruta actual de los archivos
def abririmagen():
    filepathimage= filedialog.askopenfilename(filetypes=[("Zip Files", "*.zip")])
    print(filepathimage)
def abrircapa():
    filepathcapa=filedialog.askopenfilename(filetypes=[("Shape File", "*.shp")])
    print(filepathcapa)
    
lbl1=   tkinter.Label(ventana, text="¿En donde se encuentra la imagen?").pack()
boton1= tkinter.Button(ventana, text="Abrir Imagen", command=abririmagen).pack()
Text1= tkinter.Text(ventana,width=50,height=1).pack()
boton2= tkinter.Button(ventana, text="Abrir Capa", command=abrircapa).pack()
Text2= tkinter.Text(ventana,width=50,height=1).pack()

boton3=tkinter.Button(ventana, text="Procesar Imagen", command=preproceso).pack()


ventana.mainloop()

def preproceso():
    