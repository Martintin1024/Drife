import flet as ft
from Users.login_menu import view_login
from Users.register_menu import view_register
from Roulette.main_menu import view_dashboard

def main(page: ft.Page):
    page.title = "drife"
    page.theme_mode = ft.ThemeMode.DARK
    page.window_width = 400
    page.window_height = 750 # le di un poquito mas de altura para que entren los 4 campos comodos
    
    def go_to_login():
        view_login(page, on_login_success=go_to_dashboard, on_go_to_register=go_to_register)

    def go_to_register():
        view_register(page, on_back=go_to_login)

    def go_to_dashboard(user_id):
        view_dashboard(page, user_id, on_logout=go_to_login)

    go_to_login()

ft.app(target=main, view=ft.AppView.WEB_BROWSER)