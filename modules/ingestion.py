# Archivo: ingestion.py
# -*- coding: utf-8 -*-
import pandas as pd
import xml.etree.ElementTree as ET
import os

def procesar_kml(ruta_kml):
    try:
        if not os.path.exists(ruta_kml):
            return None

        tree = ET.parse(ruta_kml)
        root = tree.getroot()
        ns = {"kml": "http://www.opengis.net/kml/2.2"}
        
        datos_puntos = []
        for pm in root.findall(".//kml:Placemark", ns):
            nombre = pm.find("kml:name", ns).text if pm.find("kml:name", ns) is not None else "Vertice"
            coords = pm.find(".//kml:coordinates", ns)
            
            if coords is not None:
                # Limpieza profunda de strings (quitar saltos de línea y espacios raros)
                c_text = coords.text.strip().replace('\n', '').replace('\t', '')
                c_list = c_text.split(",")
                
                # Guardamos Longitud (X) y Latitud (Y)
                datos_puntos.append({
                    "ID": nombre,
                    "Longitud_X": float(c_list[0]),
                    "Latitud_Y": float(c_list[1])
                })
        
        df = pd.DataFrame(datos_puntos)
        
        if df.empty:
            return None

        # --- REGLA DE ORO: CERRAR EL POLÍGONO ---
        # Si el primer punto no es igual al último, lo duplicamos para cerrar el área
        if not df.iloc[[0]].values.tolist() == df.iloc[[-1]].values.tolist():
            df = pd.concat([df, df.iloc[[0]]], ignore_index=True)
            
        return df
            
    except Exception as e:
        return None

def cargar_datos_gps(ruta_txt):
    try:
        # ... (código anterior de carga)
        df = pd.read_csv(ruta_txt, sep=None, engine='python')
        df.columns = [c.strip() for c in df.columns]

        # EL TRUCO MAESTRO:
        if 'altitude (m)' in df.columns:
            # Reemplaza los NaN por 0.0 (Nivel del mar)
            df['altitude (m)'] = df['altitude (m)'].fillna(0.0)
            
            # Opcional: Si hay valores negativos raros por error de sensor
            # df.loc[df['altitude (m)'] < 0, 'altitude (m)'] = 0.0
            
        return df
    except Exception as e:
        return None
    