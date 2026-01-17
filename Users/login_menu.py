import flet as ft
from Users.crud import log_in_user, register_new_user

# Definimos los colores aquí o los importamos de un config.py
primary_color = "#ED223F"
text_color = "#dddddd"

def vista_login(page: ft.Page, on_login_success):
    """
    Pinta la pantalla de login.
    on_login_success: Es una función que el Main nos pasa para que la ejecutemos cuando el usuario entre.
    """
    page.clean()
    
    txt_user = ft.TextField(label="Usuario", width=280, icon=ft.Icons.PERSON)
    txt_pass = ft.TextField(label="Contraseña", width=280, password=True, can_reveal_password=True, icon=ft.Icons.LOCK)
    lbl_mensaje = ft.Text(color="red")
    
    boton_login = ft.ElevatedButton(
        content=ft.Text("Iniciar Sesión", color=text_color), 
        bgcolor=primary_color, 
        width=280, 
        disabled=True
    )

    # Validaciones internas (lógica visual)
    def validar_campos(e):
        boton_login.disabled = not (txt_user.value and txt_pass.value)
        boton_login.update()

    txt_user.on_change = validar_campos
    txt_pass.on_change = validar_campos

    # Lógica de Login
    def evento_login(user_id):
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

    def evento_registro(e):
        exito, msg = register_new_user(txt_user.value, txt_pass.value)
        lbl_mensaje.value = msg
        lbl_mensaje.color = "green" if exito else "red"
        page.update()

    # Botón Login
    boton_login.on_click = evento_login

    # Dibujamos
    page.add(
        ft.Column([
            ft.Text("Bienvenido a Drife", size=30, weight="bold", color=primary_color),
            ft.Divider(color="#CC9038", thickness=2),
            txt_user, txt_pass, lbl_mensaje,
            boton_login,
            ft.OutlinedButton(
                content=ft.Text("Registrarse", color=primary_color),
                style=ft.ButtonStyle(side={ft.ControlState.DEFAULT: ft.BorderSide(2, primary_color)}),
                width=280,
                on_click=evento_registro
            ),
        ], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER)
    )
    page.update()