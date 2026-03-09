import flet as ft
import random
import time
from Roulette.Options.crud import get_roulette_items_text
from Utilities.helpers import get_visual_roulette

def view_play_roulette(page: ft.Page, user_id, r_id, r_name, on_back):
    page.clean()
    page.title = f"Jugando: {r_name}"
    page.bgcolor = "#000000"
    
    # 1. Cargar Items
    items_actuales = get_roulette_items_text(r_id)
    
    # Referencias
    roulette_container_ref = ft.Ref()
    winner_text_ref = ft.Ref()

    # --- LÓGICA DEL GIRO (Engine) ---
    def spin_roulette(e):
        if not items_actuales:
            page.show_snack_bar(ft.SnackBar(ft.Text("¡La ruleta está vacía! Agrega opciones en el menú.")))
            return

        # A. Reset visual
        winner_text_ref.current.value = "Girando..."
        winner_text_ref.current.color = "yellow"
        winner_text_ref.current.size = 20
        page.update()

        # B. Elegir Ganador (Backend Logic)
        ganador = random.choice(items_actuales)
        indice_ganador = items_actuales.index(ganador)
        total_items = len(items_actuales)
        
        # C. Calcular Ángulo (Physics)
        angulo_por_item = 360 / total_items
        # Ajuste para puntero a la derecha (+90 grados) y vueltas extra (+5 vueltas)
        vueltas_extra = 360 * 5 
        angulo_destino = (indice_ganador * angulo_por_item) + 90 + vueltas_extra
        
        # Calcular delta para siempre girar hacia adelante
        current_angle = roulette_container_ref.current.rotate.angle
        delta = angulo_destino - (current_angle % 360)
        if delta < 0: delta += 360
        
        final_rotation = current_angle + delta + vueltas_extra
        
        # D. Animar
        roulette_container_ref.current.rotate.angle = final_rotation
        page.update()

        # E. Esperar y Mostrar Ganador
        # Nota: time.sleep congela un poco la UI, idealmente usaríamos async/await,
        # pero para mantenerlo simple y compatible con tu estructura actual:
        time.sleep(4.1) 
        
        winner_text_ref.current.value = f"¡{ganador}!"
        winner_text_ref.current.color = "#00ff00" # Verde Neón
        winner_text_ref.current.size = 50
        page.update()

    # --- UI DEL JUEGO ---
    
    # Header
    header = ft.Row([
        ft.IconButton(ft.Icons.ARROW_BACK, icon_color="#ffffff", on_click=lambda e: on_back())
    ])

    # Ruleta
    wheel_container = ft.Container(
        ref=roulette_container_ref,
        content=get_visual_roulette(items_actuales, size=300), 
        width=300, height=300,
        border_radius=150,
        rotate=ft.Rotate(angle=0),
        animate_rotation=ft.Animation(4000, "easeOutQuart"), 
    )

    pointer = ft.Container(
        content=ft.Icon(ft.Icons.ARROW_LEFT, color="#ffffff", size=50),
        right=0, top=125,
    )

    game_area = ft.Stack(
        [ft.Container(content=wheel_container, padding=20), pointer],
        width=360, height=340
    )

    # Texto Ganador
    lbl_winner = ft.Text(
        ref=winner_text_ref,
        value="¡Presiona GIRAR!",
        size=20, color="#cccccc", weight="bold",
        text_align="center"
    )

    # Botón Girar
    btn_spin = ft.Container(
        content=ft.Text("GIRAR", size=24, color="white", weight="bold"),
        bgcolor="#27ae60", # Verde juego
        height=60, width=250,
        border_radius=30,
        alignment=ft.Alignment.CENTER,
        on_click=spin_roulette,
        ink=True,
        shadow=ft.BoxShadow(blur_radius=15, color=ft.Colors.with_opacity(0.4, "#27ae60"))
    )

    # Montaje
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