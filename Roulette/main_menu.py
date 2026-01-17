import flet as ft
from Roulette.crud import create_roulette_db, get_user_roulettes, delete_roulette_db

primary_color = "#ED223F"
secondary_color = "#CC9038"

def vista_dashboard(page: ft.Page, user_id, on_logout):
    page.clean()
    page.vertical_alignment = ft.MainAxisAlignment.START 
    
    # --- Lógica interna del dashboard ---
    def borrar_ruleta(e, rid):
        delete_roulette_db(user_id, rid)
        recargar_lista() # Recargamos solo la lista interna

    def crear_ruleta(e, nombre, dialogo):
        if nombre:
            create_roulette_db(user_id, nombre)
            page.close(dialogo)
            recargar_lista()

    # --- UI Helpers ---
    def recargar_lista():
        # Truco: Limpiamos la lista y la volvemos a llenar
        columna_lista.controls.clear()
        datos = get_user_roulettes(user_id)
        
        if not datos:
            columna_lista.controls.append(ft.Text("No tienes ruletas aún.", color="grey"))
        else:
            for r_id, r_nombre in datos:
                item = ft.Container(
                    content=ft.Row([
                        ft.Icon("donut_large", color=secondary_color),
                        ft.Text(r_nombre, size=16, weight="bold", expand=True),
                        ft.IconButton(icon=ft.Icons.PLAY_ARROW, icon_color="green"),
                        ft.IconButton(icon=ft.Icons.DELETE, icon_color="red", 
                            on_click=lambda e, x=r_id: borrar_ruleta(e, x))
                    ]),
                    padding=10, border=ft.border.all(1, "grey"), border_radius=10,
                    bgcolor=ft.colors.with_opacity(0.1, "white")
                )
                columna_lista.controls.append(item)
        page.update()

    # Contenedor de la lista
    columna_lista = ft.Column(scroll=ft.ScrollMode.AUTO, height=400)
    
    # Diálogo Crear
    campo_nombre = ft.TextField(label="Nombre")
    dialogo = ft.AlertDialog(
        title=ft.Text("Nueva Ruleta"), content=campo_nombre,
        actions=[ft.TextButton("Crear", on_click=lambda e: crear_ruleta(e, campo_nombre.value, dialogo))]
    )

    # --- Dibujamos la pantalla ---
    page.add(
        ft.Row([
            ft.Text("Mis Ruletas", size=25, weight="bold", color=primary_color),
            # Al hacer click en salir, llamamos a la función que nos pasó el Main
            ft.IconButton(icon=ft.Icons.LOGOUT, on_click=lambda e: on_logout()) 
        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
        ft.Divider(color=secondary_color),
        columna_lista,
        ft.Container(height=20),
        ft.ElevatedButton("Crear Nueva", icon=ft.Icons.ADD, bgcolor=primary_color, color="white", width=300,
            on_click=lambda e: page.open(dialogo))
    )
    
    # Carga inicial de datos
    recargar_lista()