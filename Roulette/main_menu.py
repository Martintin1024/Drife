import flet as ft
from Roulette.Options.crud import get_roulette_items_text
from Roulette.crud import get_user_roulettes, create_roulette_db
from Roulette.roulette_menu import view_roulette_details
from Utilities.helpers import get_visual_roulette

def view_dashboard(page: ft.Page, user_id, on_logout):
    page.clean()
    page.title = "Drife"
    page.bgcolor = "#1a1a1a"  
    page.vertical_alignment = ft.MainAxisAlignment.START
    page.padding = 20

    def go_to_details(r_id, r_name):
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
            real_items = get_roulette_items_text(r_id)
            
            visual_content = get_visual_roulette(real_items, size=60)

            card_content = ft.Container(
                content=ft.Column(
                    [
                        visual_content, 
                        ft.Text(value=r_name, size=16, weight=ft.FontWeight.BOLD, text_align="center", color="#cccccc")
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                ),
                bgcolor="#720F1E",
                border_radius=20,
                padding=15,
                alignment=ft.Alignment.CENTER,
                on_click=lambda e: go_to_details(r_id, r_name),
                ink=True 
            )
            return card_content

        for r_id, r_name in roulettes_list:
            card = create_roulette_card(r_id, r_name)
            items_grid.append(card)

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
        grid_roulettes.controls = charge_roulettes()
        grid_roulettes.update()

    txt_new_name = ft.TextField(label="Nombre de la ruleta", autofocus=True)

    def confirm_creation(e):
        name = txt_new_name.value.strip()
        if name:
            success, message = create_roulette_db(user_id, name)
            if success:
                txt_new_name.value = ""
                create_dialog.open = False
                page.update()
                update_grid() 
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

    grid_roulettes = ft.GridView(
        expand=True,
        runs_count=2,          
        max_extent=200,        
        child_aspect_ratio=1.0, 
        spacing=15,             
        run_spacing=15,         
        controls=[]             
    )

    grid_roulettes.controls = charge_roulettes()

    app_bar = ft.Row(
        [
            ft.IconButton(ft.Icons.LOGOUT, tooltip="Cerrar Sesión", on_click=lambda e: on_logout(), icon_color="#aaaaaa"),
            ft.Text("Mis Ruletas", size=24, weight=ft.FontWeight.BOLD, color="#ED223F"),
            ft.Container(width=40), 
        ],
        alignment=ft.MainAxisAlignment.SPACE_BETWEEN
    )

    vista = ft.Column(
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

    page.add(vista)