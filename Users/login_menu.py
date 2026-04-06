import flet as ft
from Users.crud import login_user

def view_login(page: ft.Page, on_login_success, on_go_to_register):
    page.clean()
    
    email_field = ft.TextField(label="Email o Usuario", width=280, icon=ft.Icons.EMAIL)
    password_field = ft.TextField(label="Contraseña", width=280, password=True, can_reveal_password=True, icon=ft.Icons.LOCK)
    message_label = ft.Text(color="#ff0000")
    
    login_button = ft.ElevatedButton(
        content=ft.Text("Iniciar Sesión", color="#dddddd"), 
        bgcolor="#ED223F", 
        width=280, 
        disabled=True
    )

    def validate_fields(e):
        login_button.disabled = not (email_field.value and password_field.value)
        login_button.update()

    email_field.on_change = validate_fields
    password_field.on_change = validate_fields

    def login_event(e):
        user_id = login_user(email_field.value, password_field.value)
        if user_id:
            on_login_success(user_id)
        else:
            message_label.value = "Datos incorrectos o correo no verificado"
            message_label.color = "#ff0000"
            page.update()

    def register_navigation_event(e):
        on_go_to_register()

    login_button.on_click = login_event

    page.add(
        ft.Column([
            ft.Text("Bienvenido a Drife", size=30, weight="bold", color="#ED223F"),
            ft.Divider(color="#CC9038", thickness=2),
            email_field, password_field, message_label,
            login_button,
            ft.OutlinedButton(
                content=ft.Text("Registrarse", color="#ED223F"),
                style=ft.ButtonStyle(side={ft.ControlState.DEFAULT: ft.BorderSide(2, "#ED223F")}),
                width=280,
                on_click=register_navigation_event
            ),
        ], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER)
    )
    page.update()