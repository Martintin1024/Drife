from Users.menu_display import show_log_in_menu
from Roulette.action_menu import action_main_menu
from Users.crud import log_in_user, register_new_user
from Utilities.helpers import cls

while True:
    option = show_log_in_menu()

    if option == "1":
        continuing = log_in_user()
        if continuing:
            cls()
            action_main_menu(current_user_id = continuing)
        elif continuing is None:
            cls()
            input("Inicio de sesión fallido. Intente de nuevo.")
    elif option == "2":
        register_new_user()
        if continuing:
            print("Registro completado. Ahora puede iniciar sesión.")
    elif option == "0":
        break
    cls()