# Archivo: ingestion.py

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
          
                c_text = coords.text.strip().replace('\n', '').replace('\t', '')
                c_list = c_text.split(",")
             )
                datos_puntos.append({
                    "ID": nombre,
                    "Longitud_X": float(c_list[0]),
                    "Latitud_Y": float(c_list[1])
                })
        
        df = pd.DataFrame(datos_puntos)
        
        if df.empty:
            return None
        if not df.iloc[[0]].values.tolist() == df.iloc[[-1]].values.tolist():
            df = pd.concat([df, df.iloc[[0]]], ignore_index=True)
            
        return df
            
    except Exception as e:
        return None

def cargar_datos_gps(ruta_txt):
    try:
   
        df = pd.read_csv(ruta_txt, sep=None, engine='python')
        df.columns = [c.strip() for c in df.columns]
        return df
    except Exception as e:
        print(f"Error al leer: {e}")
        return None
    
