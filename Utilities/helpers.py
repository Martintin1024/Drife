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
    plt.figure(figsize=(4, 4))
    sizes = [1] * len(items)
    colors = [f"#{random.randint(50, 230):02X}{random.randint(50, 230):02X}{random.randint(50, 230):02X}" for _ in items]
    
    labels_safe = []
    for item in items:
        if len(item) > 12:
            labels_safe.append(item[:10] + "...")
        else:
            labels_safe.append(item)
    
    # --- CORRECCIÓN MATEMÁTICA Y DE TEXTO ---
    wedges, texts = plt.pie(
        sizes, 
        labels=labels_safe, 
        colors=colors, 
        startangle=0,        # Obligamos a que empiece a la derecha (0°)
        counterclock=True,   # Giro antihorario asegurado
        labeldistance=0.6,
        textprops={'fontsize': 10, 'color': 'white', 'weight': 'bold'}
    )
    
    # ¡LA MAGIA PARA EL TEXTO (Problema 3)! 
    # Forzamos la rotación del texto desde el centro hacia afuera
    for wedge, text in zip(wedges, texts):
        ang = (wedge.theta2 + wedge.theta1) / 2.0
        text.set_rotation(ang)
        text.set_rotation_mode('anchor')
        text.set_ha('center')
        text.set_va('center')
    
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
    
def create_header(title_text, on_back_func):
    """Crea el encabezado estándar con botón de volver para cualquier menú"""
    return ft.Row([
        ft.IconButton(ft.Icons.ARROW_BACK, icon_color="#ffffff", on_click=on_back_func),
        ft.Text(title_text, size=30, color="#ffffff", weight="bold")
    ], alignment=ft.MainAxisAlignment.START)

def create_action_btn(text, color, icon, on_click_func):
    """Crea un botón ancho estándar (como el de Jugar, Editar, etc.)"""
    return ft.Container(
        content=ft.Row([
            ft.Icon(icon, color="#ffffff"),
            ft.Text(text, size=18, color="#ffffff", weight="bold")
        ], alignment=ft.MainAxisAlignment.CENTER),
        bgcolor=color,
        height=60, width=300,
        border_radius=15,
        alignment=ft.Alignment.CENTER,
        on_click=on_click_func,
        ink=True
    )