import flet as ft
from google import genai
import threading 
from Roulette.Options.crud import get_roulette_items_text, create_option_db
from Roulette.crud import get_user_roulettes, create_roulette_db
from Roulette.roulette_menu import view_roulette_details
from Utilities.helpers import get_visual_roulette
from Roulette.create_menu import view_create_menu

def view_dashboard(page: ft.Page, user_id, on_logout):
    page.clean()
    page.title = "Drife"
    page.bgcolor = "#1a1a1a"  
    page.vertical_alignment = ft.MainAxisAlignment.START
    page.padding = 20
    
    # --- ai config ---
    api_key = "aca iria la api key"

    def go_to_details(r_id, r_name):
        view_roulette_details(
            page, 
            user_id, 
            r_id, 
            r_name, 
            on_back=lambda: view_dashboard(page, user_id, on_logout)
        )

    def go_to_create(e=None):
        view_create_menu(
            page, 
            user_id, 
            on_back=lambda: view_dashboard(page, user_id, on_logout)
        )

    # ==========================================
    # ai fast generation logic 
    # ==========================================
    ai_topic_input = ft.TextField(label="¿De qué tema quieres la ruleta?", autofocus=True, border_color="#8e44ad", color="#ffffff")

    success_dialog = ft.AlertDialog(
        title=ft.Text("✨ ¡Éxito!"),
        content=ft.Text("¡Ruleta mágica creada con éxito!"),
        actions=[ft.TextButton("¡Genial!", on_click=lambda e: page.pop_dialog())],
    )

    error_dialog = ft.AlertDialog(
        title=ft.Text("❌ Error"),
        content=ft.Text("Algo salió mal."),
        actions=[ft.TextButton("Cerrar", on_click=lambda e: page.pop_dialog())],
    )

    def generate_magic_roulette(e):
        topic = ai_topic_input.value.strip()
        if not topic:
            return

        # ==========================================
        # ai interface logic - start loading
        # ==========================================
        
        # 1. Animación y texto
        ai_generate_btn.content = ft.Row(
            [
                ft.ProgressRing(width=16, height=16, color="#ffffff", stroke_width=2),
                ft.Text("Generando...", weight="bold", color="#ffffff")
            ],
            alignment=ft.MainAxisAlignment.CENTER,
        )
        
        # 2. Oscurecemos el botón para dar sensación de "ocupado"
        ai_generate_btn.bgcolor = "#5e2c7c" 
        
        # 3. Deshabilitamos
        ai_generate_btn.disabled = True
        ai_cancel_btn.disabled = True 
        ai_topic_input.disabled = True
        
        ai_generate_btn.update()
        ai_topic_input.update()
        ai_cancel_btn.update()

        # ==========================================
        # ai connection thread
        # ==========================================
        def talked_to_gemini():
            try:
                client = genai.Client(api_key=api_key)
                prompt = f"Dame 8 opciones de '{topic}'. Responde ÚNICAMENTE con los nombres separados por comas, sin viñetas, sin saludos y sin texto extra."
                
                response = client.models.generate_content(
                    model='gemini-2.5-flash',
                    contents=prompt,
                )

                options_array = [opt.strip() for opt in response.text.split(',')]
                success, new_id = create_roulette_db(user_id, topic.capitalize())

                if success:
                    for opt in options_array:
                        create_option_db(new_id, opt)

                    ai_topic_input.value = ""
                    update_grid()
                    page.pop_dialog()
                    page.show_dialog(success_dialog)
                else:
                    page.pop_dialog()
                    error_dialog.content = ft.Text(f"Error al guardar: {new_id}")
                    page.show_dialog(error_dialog)

            except Exception as error:
                page.pop_dialog()
                error_dialog.content = ft.Text(f"Error con la IA: {error}")
                page.show_dialog(error_dialog)
                
            finally:
                # ==========================================
                # ai interface logic - stop loading
                # ==========================================
                ai_generate_btn.content = ft.Text("Generar", weight="bold", color="#ffffff")
                ai_generate_btn.bgcolor = "#8e44ad" 
                ai_generate_btn.disabled = False
                ai_cancel_btn.disabled = False
                ai_topic_input.disabled = False
                page.update()

        threading.Thread(target=talked_to_gemini).start()

    # --- DEFINICIÓN DE BOTONES ---

    # Le ponemos altura (height=45) para que se vean bien gorditos y clickeables
    ai_generate_btn = ft.ElevatedButton(
        content=ft.Text("Generar", weight="bold", color="#ffffff"), 
        bgcolor="#8e44ad", 
        height=45,
        on_click=generate_magic_roulette
    )

    ai_cancel_btn = ft.ElevatedButton(
        content=ft.Text("Cancelar", weight="bold", color="#ffffff"),
        bgcolor="#333333",
        height=45,
        on_click=lambda e: page.pop_dialog()
    )

    # ¡LA MAGIA DEL DISEÑO APILADO ESTÁ ACÁ!
    # Metemos todo en una columna apretada (tight=True) y le decimos
    # que estire los elementos a lo ancho (STRETCH)
    dialog_content = ft.Column(
        [
            ai_topic_input,
            ft.Container(height=10), # Un pequeño espacio
            ai_generate_btn,         # Generar arriba
            ai_cancel_btn            # Cancelar abajo
        ],
        tight=True, 
        horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
        spacing=10
    )

    ai_dialog = ft.AlertDialog(
        title=ft.Text("✨ Ruleta Mágica Automática"),
        content=dialog_content,
        # Ya no usamos 'actions' porque metimos los botones en el 'content'
        actions_padding=0 
    )

    def open_ai_dialog(e):
        ai_topic_input.value = ""
        page.show_dialog(ai_dialog)

    # ==========================================
    # grid and ui
    # ==========================================
    def load_roulettes():
        items_grid = []
        roulettes_list = get_user_roulettes(user_id) 

        def create_roulette_card(r_id, r_name):
            real_items = get_roulette_items_text(r_id)
            visual_content = get_visual_roulette(real_items, size=60)

            card_content = ft.Container(
                content=ft.Column(
                    [
                        visual_content, 
                        ft.Text(value=r_name, size=16, weight="bold", text_align="center", color="#cccccc")
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                ),
                bgcolor="#720F1E",
                border_radius=20,
                padding=15,
                alignment=ft.Alignment.CENTER,
                on_click=lambda e: go_to_details(r_id, r_name)
            )
            return card_content

        for r_id, r_name in roulettes_list:
            card = create_roulette_card(r_id, r_name)
            items_grid.append(card)

        new_btn = ft.Container(
            content=ft.Column(
                [
                    ft.Icon(ft.Icons.ADD_CIRCLE_OUTLINE, size=50, color="#CC9038"), 
                    ft.Text("NUEVA\nRULETA", size=16, weight="bold", color="#CC9038", text_align="center"),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=5
            ),
            bgcolor=ft.Colors.with_opacity(0.1, "#ED223F"), 
            border_radius=20,
            padding=15,
            alignment=ft.Alignment.CENTER,
            on_click=go_to_create 
        )
        items_grid.append(new_btn)
        
        ai_btn = ft.Container(
            content=ft.Column(
                [
                    ft.Icon(ft.Icons.AUTO_AWESOME, size=50, color="#8e44ad"), 
                    ft.Text("RULETA\nCON IA", size=16, weight="bold", color="#8e44ad", text_align="center"),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=5
            ),
            bgcolor=ft.Colors.with_opacity(0.1, "#8e44ad"), 
            border_radius=20,
            padding=15,
            alignment=ft.Alignment.CENTER,
            on_click=open_ai_dialog 
        )
        items_grid.append(ai_btn)
        
        return items_grid
    
    def update_grid():
        grid_roulettes.controls = load_roulettes()
        grid_roulettes.update()

    grid_roulettes = ft.GridView(
        expand=True,
        runs_count=2,          
        max_extent=200,        
        child_aspect_ratio=1.0, 
        spacing=15,             
        run_spacing=15,         
        controls=[]             
    )

    grid_roulettes.controls = load_roulettes()

    app_bar = ft.Row(
        [
            ft.IconButton(ft.Icons.LOGOUT, tooltip="Cerrar Sesión", on_click=lambda e: on_logout(), icon_color="#aaaaaa"),
            ft.Text("Mis Ruletas", size=24, weight="bold", color="#ED223F"),
            ft.Container(width=40), 
        ],
        alignment=ft.MainAxisAlignment.SPACE_BETWEEN
    )

    main_view = ft.Column(
        [
            ft.Container(height=10), 
            app_bar,
            ft.Divider(color="#CC9038"),
            ft.Container(
                content=grid_roulettes,
                expand=True, 
                padding=20
            )
        ],
        expand=True
    )

    page.add(main_view)