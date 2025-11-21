from Roulette.menu_display import show_main_menu, show_roulette_menu
from Roulette.crud import create_roulette, select_roulette
from Utilities.helpers import cls

def action_main_menu(current_user_id = None):
    while True:

        opcion = show_main_menu()

        if opcion == "0":
            print("Saliendo del programa. ¡Hasta luego!")
            return
        
        elif opcion == "1":
            create_roulette(current_user_id)
        
        elif opcion == "2":
            current_roulette_id = select_roulette(current_user_id)
            if current_roulette_id != None:
                action_roulette_menu(current_user_id, current_roulette_id)
        
        else:
            print("Opción no válida. Por favor, intente de nuevo.")
        
        cls()

def action_roulette_menu(current_user_id, current_roulette_id):
    while True:

        opcion = show_roulette_menu()

        if opcion == "0":
            print("Regresando al menú principal.")
            return
        
        elif opcion == "1":
            print("Aca tendrias la opcion de jugar la ruleta")
        
        elif opcion == "2":
            print("Aca tendrias la opcion de editar la ruleta")

        elif opcion == "3":
            print("Aca tendrias la opcion de eliminar la ruleta")
        
        else:
            print("Opción no válida. Por favor, intente de nuevo.")
        
        input()
        cls()