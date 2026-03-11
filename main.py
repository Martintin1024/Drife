import flet as ft
from Users.login_menu import view_login
from Roulette.main_menu import view_dashboard

def main(page: ft.Page):
    page.title = "Drife"
    page.theme_mode = ft.ThemeMode.DARK
    page.window_width = 400
    page.window_height = 700
    
    def go_to_login():
        view_login(page, on_login_success=go_to_dashboard)

    def go_to_dashboard(user_id):
        view_dashboard(page, user_id, on_logout=go_to_login)

    go_to_login()

ft.app(main)