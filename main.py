import flet as ft
# Importamos las vistas desde sus carpetas
from Users.login_menu import vista_login
from Roulette.main_menu import vista_dashboard

def main(page: ft.Page):
    # Configuración Global
    page.title = "Drife App"
    page.theme_mode = ft.ThemeMode.DARK
    page.window_width = 400
    page.window_height = 700
    
    # --- SISTEMA DE NAVEGACIÓN ---
    
    def ir_a_login():
        # Llamamos a la vista de login y le pasamos la función "ir_a_dashboard"
        # para que sepa qué hacer cuando el login sea exitoso.
        vista_login(page, on_login_success=ir_a_dashboard)

    def ir_a_dashboard(user_id):
        # Llamamos al dashboard y le pasamos la función "ir_a_login"
        # para que sepa qué hacer cuando cierren sesión.
        vista_dashboard(page, user_id, on_logout=ir_a_login)

    # Arrancamos la app yendo al login
    ir_a_login()

ft.app(main)