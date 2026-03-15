import flet as ft
from Roulette.Options.crud import get_options_db, create_option_db, delete_option_db, update_option_db
from Roulette.crud import update_roulette_db

def view_option_menu(page: ft.Page, user_id, r_id, r_name, on_back):
    page.clean()
    page.title = "Drife"
    page.bgcolor = "#1a1a1a" 

    options_column = ft.Column(spacing=10, scroll=ft.ScrollMode.AUTO, expand=True)
    count_text = ft.Text(size=20, color="#ffffff", weight="bold")
    
    # --- FUNCIÓN DE GUARDADO SILENCIOSO (EDITAR) ---
    def update_inline(oid, new_val, old_val, control):
        if new_val.strip() == "":
            control.value = old_val
            page.update()
        elif new_val.strip() != old_val:
            update_option_db(r_id, oid, new_val.strip())
            control.on_blur = lambda e: update_inline(oid, e.control.value, new_val.strip(), control)
            control.on_submit = lambda e: update_inline(oid, e.control.value, new_val.strip(), control)
            try:
                page.snack_bar = ft.SnackBar(ft.Text("Opción actualizada"), duration=1500)
                page.snack_bar.open = True
                page.update()
            except:
                pass

    def load_options():
        options_column.controls.clear()
        opts = get_options_db(r_id)
        
        count_text.value = f"Opciones: {len(opts)} (50 máx.)"
        
        for idx, opt in enumerate(opts):
            o_id, o_name = opt
            
            txt_name = ft.TextField(
                value=o_name,
                border="none",         
                bgcolor="transparent", 
                color="#ffffff",
                text_size=16,
                content_padding=0,     
                expand=True,
            )
            
            txt_name.on_blur = lambda e, oid=o_id, old=o_name, ctrl=txt_name: update_inline(oid, e.control.value, old, ctrl)
            txt_name.on_submit = lambda e, oid=o_id, old=o_name, ctrl=txt_name: update_inline(oid, e.control.value, old, ctrl)

            row = ft.Container(
                content=ft.Row([
                    ft.Icon(ft.Icons.DRAG_INDICATOR, color="#555555"), 
                    ft.Text(f"{idx + 1}.", color="#cccccc", size=16),
                    txt_name, 
                    ft.IconButton(
                        icon=ft.Icons.DELETE, 
                        icon_color="#ED223F", 
                        tooltip="Borrar",
                        on_click=lambda e, oid=o_id: delete_opt(oid)
                    )
                ]),
                bgcolor="#252525",
                padding=10,
                border_radius=10
            )
            options_column.controls.append(row)
        page.update()

    def delete_opt(oid):
        delete_option_db(r_id, oid)
        load_options()

    # --- NUEVO SISTEMA: AÑADIR INLINE (RÁPIDO) ---
    txt_new_opt = ft.TextField(
        hint_text="Escribe una nueva opción y presiona Enter...",
        hint_style=ft.TextStyle(color="#777777"),
        border="none",
        bgcolor="transparent",
        color="#ffffff",
        text_size=16,
        content_padding=0,
        expand=True,
    )

    async def add_inline(e):
        val = txt_new_opt.value.strip()
        if val:
            create_option_db(r_id, val)
            txt_new_opt.value = "" # Limpiamos el texto
            load_options()         # Recargamos la lista
            await txt_new_opt.focus()    # Mantenemos el foco para escribir otra vez rápido

    txt_new_opt.on_submit = add_inline # Guarda al apretar Enter

    # Barra inferior destacada para añadir
    row_add = ft.Container(
        content=ft.Row([
            ft.Icon(ft.Icons.ADD_CIRCLE, color="#CC9038", size=30),
            txt_new_opt,
            ft.IconButton(
                icon=ft.Icons.SEND, 
                icon_color="#CC9038", 
                tooltip="Añadir (Enter)", 
                on_click=add_inline
            )
        ]),
        bgcolor="#1f1f1f",
        padding=10,
        border_radius=15,
        border=ft.border.all(2, "#CC9038") # Borde morado para destacarlo
    )

    # --- TÍTULO DE LA RULETA ---
    txt_title = ft.TextField(value=r_name, label="Título", border_color="#CC9038", color="#ffffff", expand=True)
    
    def save_title(e):
        if txt_title.value:
            update_roulette_db(user_id, r_id, txt_title.value)
            try:
                page.snack_bar = ft.SnackBar(ft.Text("Título actualizado"))
                page.snack_bar.open = True
                page.update()
            except:
                pass 

    # --- INTERFAZ BASE ---
    header = ft.Row([
        ft.IconButton(ft.Icons.ARROW_BACK, icon_color="#ffffff", on_click=lambda e: on_back(txt_title.value)),
        ft.Text("OPCIONES A ELEGIR:", size=30, color="#ffffff", weight="bold")
    ], alignment=ft.MainAxisAlignment.START)

    title_section = ft.Row([
        txt_title,
        ft.IconButton(ft.Icons.SAVE, icon_color="#27ae60", tooltip="Guardar Título", on_click=save_title)
    ])

    page.add(
        ft.Column(
            [
                header,
                ft.Container(height=10),
                title_section,
                ft.Container(height=20),
                count_text,
                ft.Container(content=options_column, expand=True), 
                ft.Container(content=row_add, padding=ft.padding.only(top=10, bottom=20)) # Aquí insertamos la barra
            ],
            expand=True
        )
    )

    load_options()