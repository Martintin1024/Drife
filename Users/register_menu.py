import flet as ft
from Users.crud import register_user

primary_color = "#ED223F"
text_color = "#dddddd"

def view_register(page: ft.Page, on_back):
    page.clean()
    
    email_field = ft.TextField(label="Correo electrónico", width=280, icon=ft.Icons.EMAIL)
    username_field = ft.TextField(label="Nombre de usuario", width=280, icon=ft.Icons.PERSON)
    password_field = ft.TextField(label="Contraseña", width=280, password=True, can_reveal_password=True, icon=ft.Icons.LOCK)
    confirm_field = ft.TextField(label="Confirmar contraseña", width=280, password=True, can_reveal_password=True, icon=ft.Icons.LOCK)
    message_label = ft.Text(color="red")
    
    register_button = ft.ElevatedButton(
        content=ft.Text("Crear cuenta", color=text_color), 
        bgcolor=primary_color, 
        width=280, 
        disabled=True
    )

    def validate_fields(e):
        # habilitar boton solo si todos los campos tienen texto
        register_button.disabled = not (email_field.value and username_field.value and password_field.value and confirm_field.value)
        register_button.update()

    email_field.on_change = validate_fields
    username_field.on_change = validate_fields
    password_field.on_change = validate_fields
    confirm_field.on_change = validate_fields

    def register_event(e):
        if password_field.value != confirm_field.value:
            message_label.value = "Las contraseñas no coinciden"
            message_label.color = "red"
            page.update()
            return
            
        success, msg = register_user(email_field.value, username_field.value, password_field.value)
        message_label.value = msg
        message_label.color = "green" if success else "red"
        
        if success:
            # limpiamos los campos para que quede prolijo
            email_field.value = ""
            username_field.value = ""
            password_field.value = ""
            confirm_field.value = ""
            
        page.update()

    def back_event(e):
        on_back()

    register_button.on_click = register_event

    page.add(
        ft.Column([
            ft.Text("Registro", size=30, weight="bold", color=primary_color),
            ft.Divider(color="#CC9038", thickness=2),
            email_field, username_field, password_field, confirm_field, message_label,
            register_button,
            ft.OutlinedButton(
                content=ft.Text("Volver al inicio de sesión", color=primary_color),
                style=ft.ButtonStyle(side={ft.ControlState.DEFAULT: ft.BorderSide(2, primary_color)}),
                width=280,
                on_click=back_event
            ),
        ], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER)
    )
    page.update()