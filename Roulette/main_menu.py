import flet as ft
from Roulette.crud import create_roulette_db, get_user_roulettes, delete_roulette_db

# Colores globales
PRIMARY_COLOR = "#ED223F"
SECONDARY_COLOR = "#CC9038"

def view_dashboard(page: ft.Page, user_id, on_logout):
    page.clean()
    page.vertical_alignment = ft.MainAxisAlignment.START 
    
    # ---------------------------------------------------------
    # 1. DEFINICIÓN DE LA LISTA (Usamos ListView)
    # ---------------------------------------------------------
    roulette_list = ft.ListView(expand=True, spacing=10, padding=20)

    # ---------------------------------------------------------
    # 2. LÓGICA
    # ---------------------------------------------------------
    
    def delete_roulette(e, rid):
        delete_roulette_db(user_id, rid)
        recharge_list()

    def create_roulette(e, nombre, dialogo):
        if nombre:
            create_roulette_db(user_id, nombre)
            page.close(dialogo)
            recharge_list()

    def recharge_list():
        roulette_list.controls.clear()
        
        datos = get_user_roulettes(user_id)
        
        if not datos:
            roulette_list.controls.append(
                ft.Text("No tienes ruletas creadas.", color="grey", text_align="center")
            )
        else:
            for r_id, r_nombre in datos:
                
                # --- CORRECCIÓN AQUÍ ---
                # Usamos 'icon' (parametro) con el string directo "play_arrow".
                # Sin 'content', sin 'ft.icons.ALGO'. Solo texto.
                btn_play = ft.IconButton(
                    icon="play_arrow",  
                    icon_color="green",
                    tooltip="Jugar"
                )
                
                btn_delete = ft.IconButton(
                    icon="delete",
                    icon_color="red",
                    on_click=lambda e, x=r_id: delete_roulette(e, x),
                    tooltip="Borrar"
                )

                # Usamos Card y ListTile para un diseño limpio
                item = ft.Card(
                    color="#252525", 
                    content=ft.ListTile(
                        # Para el icono principal también usamos texto directo en ft.Icon
                        leading=ft.Icon("donut_large", color=SECONDARY_COLOR),
                        title=ft.Text(r_nombre, color="white", weight="bold"),
                        trailing=ft.Row([btn_play, btn_delete], alignment=ft.MainAxisAlignment.END, width=100)
                    )
                )
                roulette_list.controls.append(item)
        
        page.update()

    # ---------------------------------------------------------
    # 3. UI EXTRAS (Diálogos y Botones)
    # ---------------------------------------------------------
    
    name_field = ft.TextField(label="Nombre de la ruleta")
    dialog = ft.AlertDialog(
        title=ft.Text("Nueva Ruleta"), 
        content=name_field,
        actions=[
            ft.TextButton("Cancelar", on_click=lambda e: page.close(dialog)),
            ft.TextButton("Crear", on_click=lambda e: create_roulette(e, name_field.value, dialog))
        ]
    )

    # ---------------------------------------------------------
    # 4. ARMADO DE LA PANTALLA
    # ---------------------------------------------------------
    
    # Encabezado
    header = ft.Container(
        content=ft.Column([
            ft.Row([
                ft.Text("Mis Ruletas", size=25, weight="bold", color=PRIMARY_COLOR),
                ft.IconButton(
                    icon="logout", # Icono directo
                    icon_color="white",
                    on_click=lambda e: on_logout()
                )
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
            ft.Divider(color=SECONDARY_COLOR),
        ]),
        padding=10
    )

    # Botón de crear (Este es un ElevatedButton, ese sí soporta content)
    create_btn = ft.Container(
        content=ft.ElevatedButton(
            content=ft.Row([ft.Icon("add", color="white"), ft.Text("Crear Nueva", color="white")]),
            bgcolor=PRIMARY_COLOR,
            width=300,
            on_click=lambda e: page.open(dialog)
        ),
        padding=10,
        alignment="center"
    )

    # Agregamos todo
    page.add(
        header,
        roulette_list, 
        create_btn,
    )
    
    recharge_list()