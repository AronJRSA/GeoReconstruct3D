# -*- coding: utf-8 -*-
def purificar_datos(df):
    if df is None: return None
    
    # 1. El Machete (Drop de basura)
    columns_to_drop = ['ID', 'T', 'URL', 'Metadata']
    df = df.drop(columns=[c for c in columns_to_drop if c in df.columns])
    
    # 2. El Resane (Fillna)
    if 'altitude (m)' in df.columns:
        df['altitude (m)'] = df['altitude (m)'].fillna(0.0)
        
    # 3. La Criba (Filtro lógigo: ni el Everest ni el sótano)
    # Suponiendo que 'altitude (m)' es tu columna Z
    df = df[(df['altitude (m)'] >= 500) & (df['altitude (m)'] <= 2000)]
    
    return df
