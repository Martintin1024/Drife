import flet as ft
from Users.login_menu import view_login
from Roulette.main_menu import view_dashboard

def main(page: ft.Page):
    # Configuración Global
    page.title = "Drife"
    page.theme_mode = ft.ThemeMode.DARK
    page.window_width = 400
    page.window_height = 700
    
    # --- SISTEMA DE NAVEGACIÓN ---
    
    def go_to_login():
        # Llamamos a la vista de login y le pasamos la función "ir_a_dashboard"
        # para que sepa qué hacer cuando el login sea exitoso.
        view_login(page, on_login_success=go_to_dashboard)

    def go_to_dashboard(user_id):
        # Llamamos al dashboard y le pasamos la función "ir_a_login"
        # para que sepa qué hacer cuando cierren sesión.
        view_dashboard(page, user_id, on_logout=go_to_login)

    # Arrancamos la app yendo al login
    go_to_login()

ft.app(main)