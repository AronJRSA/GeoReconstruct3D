
# -*- coding: utf-8 -*-
"""
Created on Sat Apr  4 23:40:00 2026
@author: asron (The Insaciable)
Main - Sistema de Reconstrucción 3D Interactiva
"""
# -*- coding: utf-8 -*-
"""
Created on Sat Apr  4 23:55:00 2026
@author: asron
Main - Sistema de Reconstrucción de Terreno Pro
"""

import os
import simplekml
import shapely.geometry as geom
from modules import ingestion, modeling, visualization
from config import settings

def run_pipeline():
    # 1. INGESTIÓN DE KML (Área y Contorno)
    df_poligono = ingestion.procesar_kml(settings.INPUT_KML)
    
    if df_poligono is None:
        return

    # Extraemos vértices para el contorno y la geometría
    lon_b = df_poligono['Longitud_X'].tolist()
    lat_b = df_poligono['Latitud_Y'].tolist()
    poligono_area = geom.Polygon(list(zip(lon_b, lat_b)))

    # 2. MONTE CARLO (Nube de puntos para la WEB)
    nube_puntos = modeling.generar_nube_puntos(poligono_area, settings.N_PUNTOS)
    
    # --- GUARDAR KML PARA LA WEB (Puntos Verdes) ---
    kml_web = simplekml.Kml()
    for lon, lat in nube_puntos:
        pnt = kml_web.newpoint(name="", coords=[(lon, lat)])
        pnt.style.iconstyle.icon.href = 'http://maps.google.com/mapfiles/kml/shapes/placemark_circle.png'
        pnt.style.iconstyle.color = 'ff00ff00'  # Verde
        pnt.style.iconstyle.scale = 0.15
    
    ruta_kml_web = "data/output/Mty_simulacion.kml"
    kml_web.save(ruta_kml_web)
    # 3. CARGA DE ALTITUDES (El archivo manual TXT)
    df_gps = ingestion.cargar_datos_gps(settings.INPUT_TXT)
    
    if df_gps is None:
        print('genere el .txt')
        return

    # 4. MODELADO 3D (Interpolación Perra)
    grid_data = modeling.interpolar_terreno(df_gps, settings.RESOLUCION)
    
    # Altitud para que la línea roja flote sobre el terreno
    z_borde = [df_gps['altitude (m)'].mean()] * len(lon_b)

    # 5. VISUALIZACIÓN INTERACTIVA (HTML)
    visualization.exportar_3d_interactivo(
        grid_data=grid_data,
        lon_b=lon_b,
        lat_b=lat_b,
        z_borde=z_borde,
        ruta_salida="data/output/Modelo_Interactivo.html",
        config_model=settings.MODEL_CONFIG,
        config_mun=settings.MUNICIPIO_CONFIG
    )
    visualization.generar_mapa_topografico_2d(
        grid_data=grid_data,
        lon_b=lon_b, lat_b=lat_b,
        ruta_salida="data/output/Mapa_Topografico_2D.png",
        nombre_mun=settings.MUNICIPIO_CONFIG["nombre"]
    )
    # Cálculo final de hectáreas
    hectareas = modeling.calcular_area_hectareas(poligono_area)
if __name__ == "__main__":
    # Aseguramos carpetas
    os.makedirs("data/input", exist_ok=True)
    os.makedirs("data/output", exist_ok=True)
    run_pipeline()