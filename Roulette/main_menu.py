import flet as ft
from Roulette.crud import get_user_roulettes, create_roulette_db
from Roulette.roulette_menu import view_roulette_details

def view_dashboard(page: ft.Page, user_id, on_logout):
    page.clean()
    
    # Configuración de la página
    page.title = "Drife"
    page.bgcolor = "#1a1a1a"  
    page.vertical_alignment = ft.MainAxisAlignment.START
    page.padding = 20
    # --- Lógica de Actualización de la UI ---
    def go_to_details(r_id, r_name):
        # Llamamos a la nueva vista, y le pasamos una función lambda
        # para que sepa cómo volver a ESTE menú (recargándolo)
        view_roulette_details(
            page, 
            user_id, 
            r_id, 
            r_name, 
            on_back=lambda: view_dashboard(page, user_id, on_logout)
        )

    def charge_roulettes():
        items_grid = []
        roulettes_list = get_user_roulettes(user_id) 

        def create_roulette_card(r_id, r_name):
            card_content = ft.Container(
                content=ft.Column(
                    [
                        ft.Icon(ft.Icons.PIE_CHART, size=50), # Corregí ft.Colors.PRIMARY por el HEX
                        ft.Text(value=r_name, size=16, weight=ft.FontWeight.BOLD, text_align="center", color="#CC9038")
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                ),
                bgcolor="#720F1E",
                border_radius=20,
                padding=15,
                alignment=ft.Alignment.CENTER,
                # --- AQUÍ ESTÁ EL CAMBIO ---
                # En lugar de print, llamamos a go_to_details
                on_click=lambda e: go_to_details(r_id, r_name),
                ink=True # Efecto visual de click
            )
            return card_content

        for r_id, r_name in roulettes_list:
            card = create_roulette_card(r_id, r_name)
            items_grid.append(card)

        # Botón Nueva Ruleta (Igual que antes)
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
            bgcolor=ft.Colors.with_opacity(0.1, "#ED223F"), 
            border_radius=20,
            padding=15,
            alignment=ft.Alignment.CENTER,
            on_click=open_create_dialog 
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