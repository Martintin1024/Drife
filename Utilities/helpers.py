import flet as ft
import random
import os
import io
import base64
import matplotlib
import matplotlib.pyplot as plt

matplotlib.use('Agg')

def set_db_path():
    path = os.path.join(os.path.dirname(__file__), '..', 'Data', 'roulette_data.db')
    return os.path.abspath(path)

def generate_chart_image(items):
    """Genera una imagen PNG con texto truncado si es muy largo"""
    plt.figure(figsize=(4, 4))
    
    sizes = [1] * len(items)
    colors = [f"#{random.randint(50, 230):02X}{random.randint(50, 230):02X}{random.randint(50, 230):02X}" for _ in items]
    
    # --- LOGICA DE CORTE DE TEXTO ---
    labels_safe = []
    for item in items:
        # Si tiene más de 12 letras, cortamos y agregamos "..."
        if len(item) > 12:
            labels_safe.append(item[:10] + "...")
        else:
            labels_safe.append(item)
    
    # Dibujar el gráfico
    plt.pie(
        sizes, 
        labels=labels_safe, # Usamos las etiquetas cortadas
        colors=colors, 
        startangle=90,
        labeldistance=0.6,
        rotatelabels=True,
        textprops={'fontsize': 10, 'color': 'white', 'weight': 'bold', 'ha': 'center', 'va': 'center'}
    )
    
    plt.axis('equal')
    fig = plt.gcf()
    fig.patch.set_alpha(0.0) 
    
    img_buf = io.BytesIO()
    plt.savefig(img_buf, format='png', transparent=True, bbox_inches='tight', pad_inches=0)
    plt.close()
    
    img_buf.seek(0)
    return base64.b64encode(img_buf.read()).decode("utf-8")

def get_visual_roulette(items: list, size: int = 300):
    default_icon = ft.Icons.PIE_CHART
    default_color = "#CC9038"

    if not items:
        return ft.Icon(default_icon, size=size, color=default_color)

    try:
        img_base64 = generate_chart_image(items)
        src_universal = f"data:image/png;base64,{img_base64}"
        
        return ft.Image(
            src=src_universal,
            width=size,
            height=size,
            fit="contain",
            gapless_playback=True 
        )

    except Exception as e:
        print(f"Error generando gráfico: {e}")
        return ft.Icon(default_icon, size=size, color=default_color)