import flet as ft
from Roulette.crud import get_user_roulettes, create_roulette_db

BG_COLOR = "#1a1a1a"        # Fondo casi negro
CARD_COLOR = "#252525"      # Gris oscuro (Reemplaza al Surface Variant)

def view_dashboard(page: ft.Page, user_id, on_logout):
    page.clean()
    
    # Configuración de la página
    page.title = "Drife"
    page.bgcolor = BG_COLOR
    page.vertical_alignment = ft.MainAxisAlignment.START
    page.padding = 20
    # --- Lógica de Actualización de la UI ---
    def charge_roulettes():
        """Consulta la BD y devuelve la lista de controles (tarjetas) para el Grid"""
        items_grid = []
        
        # 1. Obtenemos datos reales desde tu CRUD
        roulettes_list = get_user_roulettes(user_id) # Devuelve [(id, nombre), ...]

        # 2. Creamos una tarjeta por cada ruleta existente
        for r_id, r_name in roulettes_list:
            card = ft.Container(
                content=ft.Column(
                    [
                        # Icono de ruleta (puedes cambiarlo por una imagen luego)
                        ft.Icon(ft.Icons.PIE_CHART, size=50, color=ft.Colors.PRIMARY),
                        ft.Text(value=r_name, size=16, weight=ft.FontWeight.BOLD, text_align="center", color="#CC9038")
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                ),
                bgcolor="#720F1E", # Color oscuro estándar de Flet
                border_radius=20,
                padding=15,
                alignment=ft.Alignment.CENTER,
                on_click=lambda e, x=r_name: print(f"Abrir ruleta: {x}") # Aquí conectarás la vista de juego
            )
            items_grid.append(card)

        # 3. Agregamos al final la tarjeta de "NUEVA RULETA"
        new_btn= ft.Container(
            content=ft.Column(
                [
                    ft.Icon(ft.Icons.ADD_CIRCLE_OUTLINE, size=50, color="#CC9038"),
                    ft.Text("NUEVA\nRULETA", size=16, weight=ft.FontWeight.BOLD, color="#CC9038", text_align="center"),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=5
            ),
            bgcolor=ft.Colors.with_opacity(0.1, "#ED223F"), # Un gris muy sutil
            border_radius=20,
            padding=15,
            alignment=ft.Alignment.CENTER,
            on_click=open_create_dialog # Llama al diálogo
        )
        items_grid.append(new_btn)
        
        return items_grid

    def update_grid():
        """Refresca el contenido del grid (útil tras crear una ruleta)"""
        grid_roulettes.controls = charge_roulettes()
        grid_roulettes.update()

    # --- Lógica para Crear Ruleta (Diálogo) ---
    txt_new_name = ft.TextField(label="Nombre de la ruleta", autofocus=True)

    def confirm_creation(e):
        name = txt_new_name.value.strip()
        if name:
            # Llamamos a tu función de crud.py
            success, message = create_roulette_db(user_id, name)
            if success:
                txt_new_name.value = ""
                create_dialog.open = False
                page.update()
                update_grid() # ¡Aquí ocurre la magia! Se actualiza la vista sola.
                page.show_snack_bar(ft.SnackBar(ft.Text("¡Ruleta creada!")))
            else:
                page.show_snack_bar(ft.SnackBar(ft.Text(f"Error: {message}")))
        else:
             page.show_snack_bar(ft.SnackBar(ft.Text("Escribe un nombre válido")))

    create_dialog = ft.AlertDialog(
        title=ft.Text("Crear Nueva Ruleta"),
        content=txt_new_name,
        actions=[
            ft.TextButton("Cancelar", on_click=lambda e: page.close_dialog()),
            ft.ElevatedButton("Crear", on_click=confirm_creation),
        ],
    )

    def open_create_dialog(e):
        page.dialog = create_dialog
        create_dialog.open = True
        page.update()

    # --- Interfaz Principal (Layout) ---
    
    # Contenedor Grid
    grid_roulettes = ft.GridView(
        expand=True,
        runs_count=2,           # 2 Columnas (como la foto)
        max_extent=200,         # Ancho máximo de tarjeta
        child_aspect_ratio=1.0, # Cuadradas
        spacing=15,             # Espacio horizontal
        run_spacing=15,         # Espacio vertical
        controls=[]             # Se llenará con 'charge_roulettes()'
    )

    # Inicializamos el grid
    grid_roulettes.controls = charge_roulettes()

    # Barra superior con botón de Salir
    app_bar = ft.Row(
        [
            ft.IconButton(icon=ft.Icons.LOGOUT, tooltip="Cerrar Sesión", on_click=lambda e: on_logout(), icon_color="#ED223F"),
            ft.Text("Mis Ruletas", size=24, weight=ft.FontWeight.BOLD, color="#ED223F"),
            ft.Container(width=40), # Espaciador para equilibrar visualmente
        ],
        alignment=ft.MainAxisAlignment.SPACE_BETWEEN
    )

    # Armado final de la vista
    vista = ft.Column(
        [
            ft.Container(height=10), # Margen superior
            app_bar,
            ft.Divider(),
            ft.Container(
                content=grid_roulettes,
                expand=True, # Para que ocupe todo el espacio restante
                padding=20
            )
        ],
        expand=True
    )

    page.add(vista)