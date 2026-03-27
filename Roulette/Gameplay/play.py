import flet as ft
import random
import asyncio
import math
from Roulette.Options.crud import get_roulette_items_text
from Utilities.helpers import get_visual_roulette

def view_play_roulette(page: ft.Page, user_id, r_id, r_name, on_back):
    page.clean()
    page.window.icon = "favicon.png"
    page.title = "Drife: Draw your Life"
    page.bgcolor = "#000000"
    
    current_items = get_roulette_items_text(r_id)
    
    roulette_container_ref = ft.Ref()
    winner_text_ref = ft.Ref()

    async def spin_roulette(e):
        if not current_items:
            page.show_snack_bar(ft.SnackBar(ft.Text("¡La ruleta está vacía! Agrega opciones en el menú.")))
            return

        winner_text_ref.current.value = "Girando..."
        winner_text_ref.current.color = "yellow"
        winner_text_ref.current.size = 20
        page.update()

        winner = random.choice(current_items)
        winner_index = current_items.index(winner)
        total_items = len(current_items)
        # C. Calcular Ángulo (Matemática Exacta)
        
        # 1. ¿Cuántos grados ocupa cada rebanada?
        angle_per_item = 360 / total_items
        
        # 2. El centro geométrico del item ganador en la imagen original
        # (Matplotlib empieza a dibujar a 90° y va hacia la izquierda)
        item_center_deg = (winner_index * angle_per_item) + (angle_per_item / 2)
        
        # Le sumamos un "poquito" al azar para que la flecha no caiga SIEMPRE 
        # en el centro milimétrico de la rebanada (le da realismo)
        variation = random.uniform(-0.4, 0.4) * angle_per_item
        destination_angle_deg = item_center_deg + variation
        
        # 3. Leer ángulo actual (Flet lo devuelve en radianes, lo pasamos a grados)
        current_angle_rad = roulette_container_ref.current.rotate.angle
        current_angle_deg = math.degrees(current_angle_rad)
        
        # 4. Calcular cuánto nos falta girar (delta)
        current_base_deg = current_angle_deg % 360
        delta_deg = destination_angle_deg - current_base_deg
        
        # Si el cálculo da negativo, sumamos 360 para que nunca gire hacia atrás
        if delta_deg <= 0:
            delta_deg += 360
            
        # 5. Agregamos vueltas completas de "emoción" (ej. 6 vueltas extra)
        emotion_turns = 360 * random.randint(5, 8)
        
        # 6. Rotación final: Lo pasamos a Radianes para que Flet lo entienda
        final_angle_deg = current_angle_deg + delta_deg + emotion_turns
        final_angle_rad = math.radians(final_angle_deg)
        
        # D. Animar
        roulette_container_ref.current.rotate.angle = final_angle_rad
        page.update()

        # E. Esperar de forma inteligente SIN congelar
        await asyncio.sleep(4.1) 
        
        winner_text_ref.current.value = f"¡{winner}!"
        winner_text_ref.current.color = "#00ff00" # Verde Neón
        winner_text_ref.current.size = 50
        page.update()

    header = ft.Row([
        ft.IconButton(ft.Icons.ARROW_BACK, icon_color="#ffffff", on_click=lambda e: on_back())
    ])

    wheel_container = ft.Container(
        ref=roulette_container_ref,
        content=get_visual_roulette(current_items, size=300), 
        width=300, height=300,
        border_radius=150,
        rotate=ft.Rotate(angle=0),
        animate_rotation=ft.Animation(4000, "easeOutQuart"), 
    )

    pointer = ft.Container(
        content=ft.Icon(ft.Icons.ARROW_LEFT, color="#ffffff", size=50),
        right=0, top=145,
    )

    game_area = ft.Stack(
        [ft.Container(content=wheel_container, padding=20), pointer],
        width=360, height=340
    )

    lbl_winner = ft.Text(
        ref=winner_text_ref,
        value="¡Presiona GIRAR!",
        size=20, color="#cccccc", weight="bold",
        text_align="center"
    )

    btn_spin = ft.Container(
        content=ft.Text("GIRAR", size=24, color="white", weight="bold"),
        bgcolor="#27ae60", 
        height=60, width=250,
        border_radius=30,
        alignment=ft.Alignment.CENTER,
        on_click=spin_roulette,
        shadow=ft.BoxShadow(blur_radius=15, color=ft.Colors.with_opacity(0.4, "#27ae60"))
    )

    page.add(
        ft.Column(
            [
                header,
                ft.Container(height=10),
                ft.Text(r_name, size=30, color="#ffffff", weight="bold"),
                ft.Container(height=20),
                ft.Container(content=game_area, alignment=ft.Alignment.CENTER),
                ft.Container(height=10),
                ft.Container(content=lbl_winner, alignment=ft.Alignment.CENTER, height=60),
                ft.Container(height=20),
                btn_spin
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            scroll=ft.ScrollMode.AUTO
        )
    )