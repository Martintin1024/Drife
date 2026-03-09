import flet as ft
from Users.crud import log_in_user, register_new_user

# Definimos los colores aquí o los importamos de un config.py
primary_color = "#ED223F"
text_color = "#dddddd"

def view_login(page: ft.Page, on_login_success):
    """
    Pinta la pantalla de login.
    on_login_success: Es una función que el Main nos pasa para que la ejecutemos cuando el usuario entre.
    """
    page.clean()
    
    txt_user = ft.TextField(label="Usuario", width=280, icon=ft.Icons.PERSON)
    txt_pass = ft.TextField(label="Contraseña", width=280, password=True, can_reveal_password=True, icon=ft.Icons.LOCK)
    lbl_mensaje = ft.Text(color="red")
    
    login_button = ft.ElevatedButton(
        content=ft.Text("Iniciar Sesión", color=text_color), 
        bgcolor=primary_color, 
        width=280, 
        disabled=True
    )

    # Validaciones internas (lógica visual)
    def validate_fields(e):
        login_button.disabled = not (txt_user.value and txt_pass.value)
        login_button.update()

    txt_user.on_change = validate_fields
    txt_pass.on_change = validate_fields

    # Lógica de Login
    def login_event(user_id):
        user_id = log_in_user(txt_user.value, txt_pass.value)
        if user_id:
            # ¡EXITO! Aquí no cambiamos de pantalla nosotros.
            # Le avisamos al Main que cambie de pantalla.
            on_login_success(user_id)
        elif user_id == 0:
            lbl_mensaje.value = "Este nombre de usuario ya existe," \
            "por favor elija otro"
        else:
            lbl_mensaje.value = "Datos incorrectos"
            page.update()

    def register_event(e):
        exito, msg = register_new_user(txt_user.value, txt_pass.value)
        lbl_mensaje.value = msg
        lbl_mensaje.color = "green" if exito else "red"
        page.update()

    # Botón Login
    login_button.on_click = login_event

    # Dibujamos
    page.add(
        ft.Column([
            ft.Text("Bienvenido a Drife", size=30, weight="bold", color=primary_color),
            ft.Divider(color="#CC9038", thickness=2),
            txt_user, txt_pass, lbl_mensaje,
            login_button,
            ft.OutlinedButton(
                content=ft.Text("Registrarse", color=primary_color),
                style=ft.ButtonStyle(side={ft.ControlState.DEFAULT: ft.BorderSide(2, primary_color)}),
                width=280,
                on_click=register_event
            ),
        ], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER)
    )
    page.update()