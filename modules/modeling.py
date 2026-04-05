# Archivo: modeling.py
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
    lat_media = poligono.centroid.y
    factor_y = 111111 
    factor_x = 111111 * np.cos(np.deg2rad(lat_media))
    area_m2 = poligono.area * factor_x * factor_y
    return area_m2 / 10000

def interpolar_terreno(df_gps, resolucion):
    x = df_gps['longitude'].values
    y = df_gps['latitude'].values
    z = df_gps['altitude (m)'].values
    xi = np.linspace(x.min(), x.max(), resolucion)
    yi = np.linspace(y.min(), y.max(), resolucion)
    X, Y = np.meshgrid(xi, yi)
    Z = griddata((x, y), z, (X, Y), method='linear')
    
    return X, Y, Z
