# -*- coding: utf-8 -*-
"""
Created on Sun Mar 28 17:32:17 2021

@author: Luna_21
"""
###abrir imagenes
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.colors as colors
import os
import snappy
from snappy import Product
from snappy import ProductIO
from snappy import ProductUtils
from snappy import WKTReader
from snappy import HashMap
from snappy import GPF
# Para leer shapefiles
import shapefile
import pygeoif
import tkinter
from tkinter import filedialog

ventana= tkinter.Tk()
ventana.geometry("600x600")

def abririmagen():
    filepathimage= filedialog.askopenfilename(filetypes=[("Zip Files", "*.zip")])
    print(filepathimage)
def abrircapa():
    filepathcapa=filedialog.askopenfilename(filetypes=[("Shape File", "*.shp")])
    print(filepathcapa)
    
boton1= tkinter.Button(ventana, text="Abrir Imagen", command=abririmagen)
boton2= tkinter.Button(ventana, text="Abrir Capa", command=abrircapa)

boton1.grid(row=0, column=0)
boton2.grid(row=3, column=0)
ventana.mainloop()

######codigo para procesar la imagen

