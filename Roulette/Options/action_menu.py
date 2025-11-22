from Roulette.Options.crud import create, view, update_name, delete
from Roulette.Options.menu_display import crud_menu
from Utilities.helpers import cls

def action_crud_menu(current_roulette_id, name_roulette):
    while True:

        option = crud_menu(name_roulette)

        if option == "0":
            print("Regresando al menú de la ruleta.")
            return
        
        elif option == "1":
            create(current_roulette_id, name_roulette)
        
        elif option == "2":
            view(current_roulette_id, name_roulette)
        
        elif option == "3":
            update_name(current_roulette_id, name_roulette)
        
        elif option == "4":
            delete(current_roulette_id, name_roulette)
        
        else:
            print("Opción no válida. Por favor, intente de nuevo.")
        
        cls()