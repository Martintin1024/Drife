import flet as ft
from Roulette.Options.crud import get_roulette_items_text
from Roulette.crud import delete_roulette_db, update_roulette_db
from Utilities.helpers import get_visual_roulette
# --- IMPORTAMOS LA LÓGICA DEL JUEGO ---
from Roulette.Gameplay.play import view_play_roulette 

def view_roulette_details(page: ft.Page, user_id, r_id, r_name, on_back):
    page.clean()
    page.title = f"Configuración: {r_name}"
    page.bgcolor = "#1a1a1a" # Gris oscuro estilo dashboard
    
    # Variables de estado
    items_actuales = get_roulette_items_text(r_id)
    title_ref = ft.Ref()
    preview_ref = ft.Ref()

    # --- NAVEGACIÓN AL JUEGO ---
    def go_to_play(e):
        view_play_roulette(
            page, user_id, r_id, r_name, 
            # Cuando volvamos del juego, regresamos a ESTE menú de configuración
            on_back=lambda: view_roulette_details(page, user_id, r_id, r_name, on_back)
        )

    # --- DIÁLOGOS (Borrar / Renombrar) ---
    def close_dlg(dlg):
        dlg.open = False
        page.update()

    def confirm_delete(e):
        delete_roulette_db(user_id, r_id)
        on_back() # Volver al dashboard principal

    delete_dialog = ft.AlertDialog(
        title=ft.Text("¿Eliminar esta ruleta?"),
        content=ft.Text("Esta acción no se puede deshacer."),
        actions=[
            ft.TextButton("Cancelar", on_click=lambda e: close_dlg(delete_dialog)),
            ft.TextButton("Eliminar", on_click=confirm_delete, style=ft.ButtonStyle(color="#ff0000")),
        ],
    )

    txt_rename = ft.TextField(label="Nuevo nombre", value=r_name, border_color="#cc9038")
    def confirm_rename(e):
        if txt_rename.value:
            update_roulette_db(user_id, r_id, txt_rename.value)
            title_ref.current.value = txt_rename.value
            close_dlg(rename_dialog)
            page.update()

    rename_dialog = ft.AlertDialog(
        content=txt_rename,
        actions=[ft.ElevatedButton("Guardar", on_click=confirm_rename)],
    )

    # --- UI DEL MENÚ ---
    
    # Header
    header = ft.Row([
        ft.IconButton(ft.Icons.ARROW_BACK, icon_color="#ffffff", on_click=lambda e: on_back()),
        ft.Text("Volver", color="#cccccc")
    ])

    # Título
    lbl_title = ft.Text(ref=title_ref, value=r_name, size=40, color="#ffffff", weight="bold")

    # Vista Previa (Estática, solo imagen)
    # Usamos un contenedor simple, sin lógica de giro
    preview_container = ft.Container(
        ref=preview_ref,
        content=get_visual_roulette(items_actuales, size=200),
        width=200, height=200,
        border_radius=100,
        alignment=ft.Alignment.CENTER,
        # Sombra suave para darle estilo
        shadow=ft.BoxShadow(blur_radius=20, color=ft.Colors.with_opacity(0.2, "black")) 
    )

    # Botones de Acción
    def action_btn(text, color, icon, func):
        return ft.Container(
            content=ft.Row([
                ft.Icon(icon, color="#ffffff"),
                ft.Text(text, size=18, color="#ffffff", weight="bold")
            ], alignment=ft.MainAxisAlignment.CENTER),
            bgcolor=color,
            height=60, width=300,
            border_radius=15,
            alignment=ft.Alignment.CENTER,
            on_click=func,
            ink=True
        )

    page.add(
        ft.Column(
            [
                header,
                ft.Container(height=10),
                ft.Container(content=lbl_title, alignment=ft.Alignment.CENTER),
                ft.Container(height=20),
                
                # Vista Previa
                ft.Container(content=preview_container, alignment=ft.Alignment.CENTER),
                ft.Text("Vista Previa", color="#cccccc", size=12),
                
                ft.Container(height=40),
                
                # Botón JUGAR (Grande y destacado)
                action_btn("JUGAR AHORA", "#ED223F", ft.Icons.PLAY_ARROW, go_to_play),
                
                ft.Container(height=15),
                
                # Botón Editar Opciones
                action_btn("EDITAR OPCIONES", "#8e44ad", ft.Icons.LIST, lambda e: print("Abrir editor...")),
                
                ft.Container(height=30),
                ft.Divider(color="#cccccc"),
                
                ft.Row([
                    ft.TextButton("Renombrar Ruleta", icon=ft.Icons.EDIT, on_click=lambda e: (setattr(rename_dialog, 'open', True), page.update())),
                    ft.TextButton("Borrar Ruleta", icon=ft.Icons.DELETE, icon_color="red", style=ft.ButtonStyle(color="#ff0000"), on_click=lambda e: (setattr(delete_dialog, 'open', True), page.update()))
                ], alignment=ft.MainAxisAlignment.CENTER)
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            scroll=ft.ScrollMode.AUTO
        )
    )