# Archivo: modeling.py
# -*- coding: utf-8 -*-
import numpy as np
import shapely.geometry as geom
from scipy.interpolate import griddata

def generar_nube_puntos(poligono, n_puntos):

    min_x, min_y, max_x, max_y = poligono.bounds
    puntos_validados = []
    intentos = 0
    max_intentos = n_puntos * 100 

    while len(puntos_validados) < n_puntos and intentos < max_intentos:
        random_x = np.random.uniform(min_x, max_x)
        random_y = np.random.uniform(min_y, max_y)
        punto = geom.Point(random_x, random_y)
        
        if poligono.contains(punto):
            puntos_validados.append((random_x, random_y))
        intentos += 1
    
    return np.array(puntos_validados)

def calcular_area_hectareas(poligono):

    # Obtenemos la latitud media del polígono para el factor de corrección
    lat_media = poligono.centroid.y
    
    # Constantes de conversión (Metros por grado)
    factor_y = 111111 
    factor_x = 111111 * np.cos(np.deg2rad(lat_media))
    
    # Área en m2 = área en grados^2 * factores de corrección
    area_m2 = poligono.area * factor_x * factor_y
    return area_m2 / 10000

def interpolar_terreno(df_gps, resolucion):

    # Extraemos las columnas del DataFrame de GPS
    x = df_gps['longitude'].values
    y = df_gps['latitude'].values
    z = df_gps['altitude (m)'].values

    # 1. Definimos los límites de la malla basados en los datos reales
    xi = np.linspace(x.min(), x.max(), resolucion)
    yi = np.linspace(y.min(), y.max(), resolucion)
    
    # 2. Creamos la cuadrícula (meshgrid)
    X, Y = np.meshgrid(xi, yi)

    # 3. La magia: Interpolación Lineal para unir los puntos GPS

    Z = griddata((x, y), z, (X, Y), method='linear')
    
    # Devolvemos los 3 componentes de la superficie
    return X, Y, Z