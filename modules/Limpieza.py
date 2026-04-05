# -*- coding: utf-8 -*-
def purificar_datos(df):
    if df is None: return None
    columns_to_drop = ['ID', 'T', 'URL', 'Metadata']
    df = df.drop(columns=[c for c in columns_to_drop if c in df.columns])
    if 'altitude (m)' in df.columns:
        df['altitude (m)'] = df['altitude (m)'].fillna(0.0)
    df = df[(df['altitude (m)'] >= MIN_ALTITUDE) & (df['altitude (m)'] <= MAX_ALTITUDE)]
    
    return df
