import flet as ft
from Roulette.Options.crud import get_roulette_items_text
from Roulette.crud import delete_roulette_db 
from Utilities.helpers import get_visual_roulette, create_header, create_action_btn
from Roulette.Options.option_menu import view_option_menu
from Roulette.Gameplay.play import view_play_roulette 


def view_roulette_details(page: ft.Page, user_id, r_id, r_name, on_back):
    page.clean()
    page.window.icon = "favicon.png"
    page.title = "Drife: Draw your Life"
    page.bgcolor = "#1a1a1a"
    page.padding = 20

    current_items = get_roulette_items_text(r_id)
    title_ref = ft.Ref[ft.Text]()

    def go_to_play(e):
        view_play_roulette(
            page, user_id, r_id, r_name, 
            on_back=lambda: view_roulette_details(page, user_id, r_id, r_name, on_back)
        )

    def go_to_options(e):
        def back_from_options(updated_name):
            view_roulette_details(page, user_id, r_id, updated_name, on_back)

        current_name = title_ref.current.value 
        view_option_menu(page, user_id, r_id, current_name, on_back=back_from_options)

    # --- FUNCIÓN DE CONFIRMACIÓN DE BORRADO ---
    def delete_roulette(e):
        page.show_dialog(delete_confirm_dialog)

    def handle_delete_confirmation(e):
        page.pop_dialog()
        
        # ¡CORREGIDO! Pasamos user_id y r_id en el orden exacto que pide tu función
        delete_roulette_db(user_id, r_id)
        
        # Avisamos que se borró y volvemos al menú
        try:
            page.snack_bar = ft.SnackBar(ft.Text(f"Ruleta '{r_name}' eliminada exitosamente"))
            page.snack_bar.open = True
            page.update()
        except:
            pass
            
        on_back()

    # --- DIÁLOGO DE CONFIRMACIÓN ---
    delete_confirm_dialog = ft.AlertDialog(
        title=ft.Text("⚠ Confirmar eliminación"),
        content=ft.Text(f"¿Estás seguro de que quieres eliminar la ruleta '{r_name}' de forma permanente?"),
        actions=[
            ft.TextButton("Eliminar", on_click=handle_delete_confirmation, icon=ft.Icons.DELETE, icon_color="#ED223F"),
            ft.TextButton("Cancelar", on_click=lambda e: page.pop_dialog()),
        ],
        actions_alignment=ft.MainAxisAlignment.END,
    )

    header = create_header(r_name, lambda e: on_back())
    # Sobrescribimos el texto del header para poder cambiarlo de nombre si hace falta
    header.controls[1] = ft.Text(r_name, size=30, color="#ffffff", weight="bold", ref=title_ref)

    # --- VISTA PREVIA DE LA RULETA (¡RESTAURADA!) ---
    visual_content = get_visual_roulette(current_items, size=250)
    preview_container = ft.Container(
        content=visual_content,
        alignment=ft.Alignment.CENTER,
        padding=20
    )

    # --- BOTONES DE ACCIÓN (SIN EL BOTÓN DE DISEÑO) ---
    play_btn = create_action_btn("JUGAR AHORA", "#ED223F", ft.Icons.PLAY_ARROW, go_to_play)
    edit_options_btn = create_action_btn("EDITAR OPCIONES", "#CC9038", ft.Icons.LIST, go_to_options)
    delete_btn = create_action_btn("ELIMINAR RULETA", "#ED223F", ft.Icons.DELETE, delete_roulette)

    main_col = ft.Column(
        [
            header,
            ft.Container(height=10),
            preview_container,
            ft.Text("Vista Previa", color="#cccccc", size=12, text_align="center"),
            ft.Container(height=30),
            
            # Fila 1: Jugar y Editar
            ft.Row([play_btn, edit_options_btn], alignment=ft.MainAxisAlignment.SPACE_EVENLY),
            ft.Container(height=20),
            
            # Fila 2: Eliminar
            ft.Row([delete_btn], alignment=ft.MainAxisAlignment.CENTER),
        ],
        expand=True,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER
    )

    page.add(main_col)