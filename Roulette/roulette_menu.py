import flet as ft
from Roulette.Options.crud import get_roulette_items_text
from Roulette.crud import delete_roulette_db, update_roulette_db
from Utilities.helpers import get_visual_roulette

def view_roulette_details(page: ft.Page, user_id, r_id, r_name, on_back):
    page.clean()
    page.title = f"Drife"
    page.bgcolor = "#1a1a1a"
    
    # 1. Recuperamos los datos para pintar la ruleta grande
    items_actuales = get_roulette_items_text(r_id)
    
    title_ref = ft.Ref()

    # ... (Funciones close_dlg, open_dlg, confirm_delete, confirm_rename SIGUEN IGUAL) ...
    
    # --- CÓDIGO DE DIÁLOGOS (Resumido, déjalo igual que antes) ---
    def close_dlg(dlg):
        dlg.open = False
        page.update()
    def open_dlg(dlg):
        page.dialog = dlg
        dlg.open = True
        page.update()
    def confirm_delete(e):
        success, msg = delete_roulette_db(user_id, r_id)
        if success:
            page.close_dialog()
            page.show_snack_bar(ft.SnackBar(ft.Text("Ruleta eliminada")))
            on_back() 
        else:
            page.show_snack_bar(ft.SnackBar(ft.Text(f"Error: {msg}")))
    delete_dialog = ft.AlertDialog(
        title=ft.Text("¿Eliminar Ruleta?"),
        content=ft.Text("Se borrará para siempre. ¿Estás seguro?"),
        actions=[
            ft.TextButton("Cancelar", on_click=lambda e: page.close_dialog()),
            ft.TextButton("Sí, Eliminar", on_click=confirm_delete, style=ft.ButtonStyle(color="#ff0000")),
        ],
    )
    txt_rename = ft.TextField(label="Nuevo nombre", value=r_name, color="#ffffff", border_color="#cc9038")
    def confirm_rename(e):
        new_val = txt_rename.value.strip()
        if new_val:
            success, msg = update_roulette_db(user_id, r_id, new_val)
            if success:
                title_ref.current.value = new_val 
                close_dlg(rename_dialog)
                page.update()
                page.show_snack_bar(ft.SnackBar(ft.Text("Nombre actualizado")))
            else:
                page.show_snack_bar(ft.SnackBar(ft.Text(f"Error: {msg}")))
    rename_dialog = ft.AlertDialog(
        title=ft.Text("Renombrar Ruleta"),
        content=txt_rename,
        actions=[
            ft.TextButton("Cancelar", on_click=lambda e: close_dlg(rename_dialog)),
            ft.ElevatedButton("Guardar", on_click=confirm_rename, bgcolor="#00ff00", color="#ffffff"),
        ],
    )

    # ---------------------------------------------------------
    # 2. DISEÑO VISUAL
    # ---------------------------------------------------------

    header = ft.Row(
        [
            ft.IconButton(
                icon=ft.Icons.ARROW_BACK, 
                icon_color="#aaaaaa", 
                icon_size=30,
                tooltip="Volver",
                on_click=lambda e: on_back()
            ),
            ft.Container(width=10),
            ft.Text("Volver al menú", color="#aaaaaa", size=16)
        ]
    )

    # 3. AQUÍ HACEMOS LA MAGIA VISUAL
    # Generamos la ruleta grande (Size 150 o más)
    visual_grande = get_visual_roulette(items_actuales, size=150)

    title_display = ft.Column(
        [
            visual_grande, # <--- Reemplazamos el Icon estático por esto
            
            ft.Container(height=10), # Un poco de aire
            
            ft.Text(
                ref=title_ref,
                value=r_name, 
                size=40, 
                weight=ft.FontWeight.BOLD, 
                color="#ffffff", 
                text_align="center"
            ),
        ],
        horizontal_alignment=ft.CrossAxisAlignment.CENTER
    )

    btn_play = ft.Container(
        content=ft.Row(
            [
                ft.Icon(ft.Icons.PLAY_ARROW, size=60, color="#ffffff"),
                ft.Text("JUGAR", size=30, weight="bold", color="#ffffff")
            ], 
            alignment=ft.MainAxisAlignment.CENTER
        ),
        bgcolor="#ed223f",
        width=300, height=100,
        border_radius=20,
        alignment=ft.Alignment.CENTER,
        ink=True,
        on_click=lambda e: print(f"Jugar ruleta: {title_ref.current.value}") 
    )

    def option_btn(icon, text, color, on_click_func):
        return ft.Container(
            content=ft.Column(
                [
                    ft.Icon(icon, size=35, color=color),
                    ft.Text(text, color="#ffffff", size=14, weight="bold")
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                spacing=5
            ),
            bgcolor="#252525",
            width=130, height=130,
            border_radius=15,
            border=ft.border.all(1, color),
            alignment=ft.Alignment.CENTER,
            ink=True,
            on_click=on_click_func
        )

    options_row = ft.Row(
        [
            option_btn(ft.Icons.LIST, "Editar\nOpciones", "#cc9038", lambda e: print("Ir a items...")),
            option_btn(ft.Icons.EDIT, "Cambiar\nNombre", "#6193B4", lambda e: open_dlg(rename_dialog)),
            option_btn(ft.Icons.DELETE, "Borrar\nRuleta", "#ff0000", lambda e: open_dlg(delete_dialog)),
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        spacing=20
    )

    page.add(
        ft.Column(
            [
                ft.Container(height=10),
                header,
                ft.Container(height=20),
                ft.Container(content=title_display, alignment=ft.Alignment.CENTER),
                ft.Container(height=40),
                ft.Container(content=btn_play, alignment=ft.Alignment.CENTER),
                ft.Container(height=40),
                ft.Divider(color="#cc9038"),
                ft.Text("Configuración", color="#aaaaaa", size=16, text_align="center"),
                ft.Container(height=20),
                options_row
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        )
    )