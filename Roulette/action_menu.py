from Roulette.menu_display import show_main_menu, show_roulette_menu
from Roulette.crud import create, select, update, delete
from Utilities.helpers import cls
from Roulette.Options.action_menu import action_crud_menu
from Roulette.Gameplay.play import spin_roulette

def action_main_menu(current_user_id = None):
    while True:

        opcion = show_main_menu()

        if opcion == "0":
            print("Saliendo del programa. ¡Hasta luego!")
            return
        
        elif opcion == "1":
            create(current_user_id)
        
        elif opcion == "2":
            current_roulette_id, current_roulette_name = select(current_user_id)
            if current_roulette_id != None:
                action_menu(current_user_id, current_roulette_id, current_roulette_name)
        
        else:
            print("Opción no válida. Por favor, intente de nuevo.")
        
        cls()

def action_menu(current_user_id, current_roulette_id, current_roulette_name):
    while True:

        opcion = show_roulette_menu()

        if opcion == "0":
            print("Regresando al menú principal.")
            return
        
        elif opcion == "1":
            spin_roulette(current_roulette_id, current_roulette_name)
        
        elif opcion == "2":
            update(current_user_id, current_roulette_id)

        elif opcion == "3":
            delete(current_roulette_id)

        elif opcion == "4": ### OPTIONS ###
            action_crud_menu(current_roulette_id, current_roulette_name)
        
        else:
            print("Opción no válida. Por favor, intente de nuevo.")
        
        input()
        cls()