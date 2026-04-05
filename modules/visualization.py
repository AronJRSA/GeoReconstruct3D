# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import os

def exportar_3d_interactivo(grid_data, lon_b, lat_b, z_borde, ruta_salida, config_model, config_mun):
    """
    Genera el Modelo 3D INTERACTIVO en HTML con Plotly.
    Incluye curvas de nivel dinámicas sobre la superficie.
    """
    grid_x, grid_y, grid_z = grid_data
    fig = go.Figure()

    # 1. EL TERRENO (Superficie 3D con curvas de nivel integradas)
    fig.add_trace(go.Surface(
        x=grid_x, y=grid_y, z=grid_z,
        colorscale=config_model.get("colorscale", "Earth"),
        name='Relieve Terrestre',
        contours = {
            "z": {
                "show": True, 
                "usecolormap": True, 
                "highlightcolor": "white", 
                "project": {"z": True} # Proyecta las curvas en la base
            }
        },
        colorbar=dict(title="msnm (Altitud)")
    ))

    # 2. EL CONTORNO (La línea del municipio del KML)
    fig.add_trace(go.Scatter3d(
        x=lon_b, y=lat_b, z=z_borde,
        mode='lines',
        line=dict(
            color=config_model.get("contour_color", "red"), 
            width=config_model.get("contour_width", 5)
        ),
        name='Límite KML'
    ))

    # 3. CONFIGURACIÓN DE LA ESCENA
    nombre_mun = config_mun.get('nombre', 'Proyecto Geográfico')
    
    fig.update_layout(
        title=f"📊 Modelado 3D Interactivo - {nombre_mun}",
        template="plotly_dark",
        scene=dict(
            aspectratio=dict(x=1, y=1, z=config_model.get("z_scale", 0.5)),
            xaxis=dict(title="Longitud"),
            yaxis=dict(title="Latitud"),
            zaxis=dict(title="Altitud (m)"),
            bgcolor="black"
        ),
        margin=dict(l=0, r=0, b=0, t=50)
    )

    fig.write_html(ruta_salida)
    print('fin')


def generar_mapa_topografico_2d(grid_data, lon_b, lat_b, ruta_salida, nombre_mun):

    X, Y, Z = grid_data
    
    # Creamos la figura con un tamaño pro
    plt.figure(figsize=(12, 10))
    
    # 1. Dibujar las curvas de nivel (contour)
    # 'levels=40' da mucha precisión al Cerro de la Silla
    curvas = plt.contour(X, Y, Z, levels=40, cmap='viridis', linewidths=0.6)
    
    # 2. Etiquetas de altitud (clabel)
    # Esto pone los numeritos sobre las líneas como en tu foto
    plt.clabel(curvas, inline=True, fontsize=7, fmt='%1.0f', colors='black')
    
    # 3. El contorno del municipio
    plt.plot(lon_b, lat_b, color='black', linewidth=2.5, label='Límite KML')
    
    # 4. Estética de plano técnico
    plt.title(f"Mapa de Curvas de Nivel - {nombre_mun}", fontsize=16, pad=20)
    plt.xlabel("Longitud (Grados)")
    plt.ylabel("Latitud (Grados)")
    plt.grid(True, linestyle=':', alpha=0.6)
    
    # IMPORTANTE: Mantener la proporción real del terreno
    plt.gca().set_aspect('equal', adjustable='box')
    
    # Añadir barra de colores para referencia rápida
    cbar = plt.colorbar(curvas)
    cbar.set_label('Elevación (msnm)')

    # Guardado en alta resolución
    plt.savefig(ruta_salida, dpi=300, bbox_inches='tight')
    plt.close()
