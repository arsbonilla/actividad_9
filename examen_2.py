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
#implementacion de las funciones que implementaran la ruta actual de los archivos
def abririmagen():
    filepathimage= filedialog.askopenfilename(filetypes=[("Zip Files", "*.zip")])
    Text1.insert(0,filepathimage)
    return (filepathimage)
def abrircapa():
    filepathcapa=filedialog.askopenfilename(filetypes=[("Shape File", "*.shp")])
    Text2.insert(0,filepathcapa)
    return (filepathcapa)


def preproceso():
    path_to_sentinel_data = Text1.get()
    product = ProductIO.readProduct(path_to_sentinel_data)
    
    #Leer y mostrar la informaciónd de la imagen
    width = product.getSceneRasterWidth()
    print("Width: {} px".format(width))
    height = product.getSceneRasterHeight()
    print("Height: {} px".format(height))
    name = product.getName()
    print("Name: {}".format(name))
    band_names = product.getBandNames()
    print("Band names: {}".format(", ".join(band_names)))
    ##Aplicar correccion orbital
    parameters = HashMap()
    GPF.getDefaultInstance().getOperatorSpiRegistry().loadOperatorSpis()
    parameters.put('orbitType', 'Sentinel Precise (Auto Download)')
    parameters.put('polyDegree', '3')
    parameters.put('continueOnFail', 'false')
    apply_orbit_file = GPF.createProduct('Apply-Orbit-File', parameters, product)
    
    ##Recortar la imagen
    r = shapefile.Reader(Text2.get())
    g=[]
    for s in r.shapes():
        g.append(pygeoif.geometry.as_shape(s))
    m = pygeoif.MultiPoint(g)
    wkt = str(m.wkt).replace("MULTIPOINT", "POLYGON(") + ")"
    
    #Usar el shapefile para cortar la imagen
    SubsetOp = snappy.jpy.get_type('org.esa.snap.core.gpf.common.SubsetOp')
    bounding_wkt = wkt
    geometry = WKTReader().read(bounding_wkt)
    HashMap = snappy.jpy.get_type('java.util.HashMap')
    GPF.getDefaultInstance().getOperatorSpiRegistry().loadOperatorSpis()
    parameters = HashMap()
    parameters.put('copyMetadata', True)
    parameters.put('geoRegion', geometry)
    product_subset = snappy.GPF.createProduct('Subset', parameters, apply_orbit_file)
    
    #Mostrar las dimensiones de la imagen
    width = product_subset.getSceneRasterWidth()
    print("Width: {} px".format(width))
    height = product_subset.getSceneRasterHeight()
    print("Height: {} px".format(height))
    band_names = product_subset.getBandNames()
    print("Band names: {}".format(", ".join(band_names)))
    band = product_subset.getBand(band_names[0])
    print(band.getRasterSize())
    plotBand(product_subset, "Intensity_VV", 0, 100000)
    
    ##Aplicar la calibracion de la imagen
    parameters = HashMap()
    parameters.put('outputSigmaBand', True)
    parameters.put('sourceBands', 'Intensity_VV')
    parameters.put('selectedPolarisations', "VV")
    parameters.put('outputImageScaleInDb', False)
    product_calibrated = GPF.createProduct("Calibration", parameters, product_subset)
    plotBand(product_calibrated, "Sigma0_VV", 0, 1)
    
    ##Aplicar el filtro Speckle
    filterSizeY = '5'
    filterSizeX = '5'
    parameters = HashMap()
    parameters.put('sourceBands', 'Sigma0_VV')
    parameters.put('filter', 'Lee')
    parameters.put('filterSizeX', filterSizeX)
    parameters.put('filterSizeY', filterSizeY)
    parameters.put('dampingFactor', '2')
    parameters.put('estimateENL', 'true')
    parameters.put('enl', '1.0')
    parameters.put('numLooksStr', '1')
    parameters.put('targetWindowSizeStr', '3x3')
    parameters.put('sigmaStr', '0.9')
    parameters.put('anSize', '50')
    speckle_filter = snappy.GPF.createProduct('Speckle-Filter', parameters, product_calibrated)
    plotBand(speckle_filter, 'Sigma0_VV', 0, 1)
    
    ##Aplicar la correccion del terreno
    parameters = HashMap()
    parameters.put('demName', 'SRTM 3Sec')
    parameters.put('pixelSpacingInMeter', 10.0)
    parameters.put('sourceBands', 'Sigma0_VV')
    speckle_filter_tc = GPF.createProduct("Terrain-Correction", parameters, speckle_filter)
    plotBand(speckle_filter_tc, 'Sigma0_VV', 0, 0.1)
   
    
lbl1=   tkinter.Label(ventana, text="¿En donde se encuentra la imagen?").pack()
boton1= tkinter.Button(ventana, text="Abrir Imagen", command=abririmagen).pack()
Text1= tkinter.Text(ventana,width=50,height=1).pack()
boton2= tkinter.Button(ventana, text="Abrir Capa", command=abrircapa).pack()
Text2= tkinter.Text(ventana,width=50,height=1).pack()


boton3=tkinter.Button(ventana, text="Procesar Imagen", command=preproceso).pack()
lbl2=tkinter.Label(ventana, text="Defina umbral para mascara de agua").pack()
Text3= tkinter.Text(ventana,width=50,height=1).pack()



ventana.mainloop()


 
    
   