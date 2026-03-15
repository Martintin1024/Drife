import flet as ft
# Ajusta estos imports según donde tengas exactamente tus funciones CRUD
from Roulette.crud import create_roulette_db 
from Roulette.Options.crud import create_option_db
from Utilities.helpers import create_header, create_action_btn

def view_create_menu(page: ft.Page, user_id, on_back):
    page.clean()
    page.title = "Drife"
    page.bgcolor = "#1a1a1a"

    # 1. Campo para el Nombre de la Ruleta
    txt_title = ft.TextField(label="Nombre de la Ruleta", border_color="#27ae60", color="#ffffff", expand=True)

    # 2. Lista visual donde irán los campos de las opciones
    options_list = ft.Column(spacing=10)

    def add_option_field(e=None):
        """Agrega un nuevo campo de texto vacío a la lista"""
        new_field = ft.TextField(
            hint_text=f"Opción {len(options_list.controls) + 1}...",
            border_color="#555555",
            color="#ffffff"
        )
        options_list.controls.append(new_field)
        page.update()

    # Arrancamos dándole 2 campos vacíos por defecto al usuario
    add_option_field()
    add_option_field()

    # 3. Función Principal de Guardado
    def save_new_roulette(e):
        title = txt_title.value.strip()
        
        # Recolectamos solo los campos de opciones que no estén vacíos
        valid_options = [f.value.strip() for f in options_list.controls if f.value.strip()]

        # Validaciones
        if not title:
            page.snack_bar = ft.SnackBar(ft.Text("Ponle un nombre a la ruleta"))
            return

        if len(valid_options) < 2:
            page.snack_bar = ft.SnackBar(ft.Text("Necesitas escribir al menos 2 opciones"))
            return

        # Creamos la Ruleta y recibimos el ID nuevo
        success, result = create_roulette_db(user_id, title)
        
        if success:
            new_roulette_id = result # result contiene el ID
            # Guardamos cada opción enlazada a este nuevo ID
            for opt in valid_options:
                create_option_db(new_roulette_id, opt)
            
            page.snack_bar = ft.SnackBar(ft.Text("¡Ruleta creada con éxito!"))
            on_back() # Volvemos al menú principal
        else:
           page.snack_bar = ft.SnackBar(ft.Text(f"Error: {result}"))

    # 4. Construcción de Interfaz usando nuestros Atajos (Helpers)
    header = create_header("CREAR RULETA", lambda e: on_back())
    btn_save = create_action_btn("GUARDAR RULETA", "#27ae60", ft.Icons.CHECK, save_new_roulette)
    btn_add_opt = ft.TextButton("Añadir otro campo", icon=ft.Icons.ADD, on_click=add_option_field)

    # 5. Renderizado
    page.add(
        ft.Column([
            header,
            ft.Container(height=20),
            txt_title,
            ft.Container(height=30),
            ft.Text("Opciones (Mínimo 2):", size=20, color="#ffffff", weight="bold"),
            options_list,
            btn_add_opt,
            ft.Container(height=40),
            ft.Container(content=btn_save, alignment=ft.Alignment.CENTER)
        ], expand=True, scroll=ft.ScrollMode.AUTO)
    )