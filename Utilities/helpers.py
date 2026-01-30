import random
import os

def set_db_path():
    path = os.path.join(os.path.dirname(__file__), '..', 'Data', 'roulette_data.db')
    return os.path.abspath(path)

import flet as ft
import flet_charts as fch
from Roulette.Options.crud import get_roulette_items_text

def get_random_color():
    r = random.randint(50, 255)
    g = random.randint(50, 255)
    b = random.randint(50, 255)
    return f"#{r:02X}{g:02X}{b:02X}"

def get_visual_roulette(items: list, size: int = 50):
    default_icon = ft.Icons.PIE_CHART
    default_color = "#CC9038"

    if not items:
        return ft.Icon(default_icon, size=size, color=default_color)

    try:
        mis_secciones = [] 
        
        for item in items:
            nueva_seccion = fch.PieChartSection(
                value=1, 
                color=get_random_color(),
                radius=size / 2,
                title="", 
            )
            mis_secciones.append(nueva_seccion)

        return ft.Container(
            width=size,
            height=size,
            content=fch.PieChart(
                sections=mis_secciones, 
                sections_space=0,
                center_space_radius=0,
                expand=True
            ),
            alignment=ft.Alignment.CENTER
        )

    except Exception as e:
        print(f"Error visualizando ruleta: {e}")
        return ft.Icon(default_icon, size=size, color=default_color)