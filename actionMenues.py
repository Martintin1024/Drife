from functions import createRoulette, showUsers
from visualMenu import showMainMenu, cls

def actionMainMenu(currentUserId = None):
    while True:

        opcion = showMainMenu()

        if opcion == "0":
            print("Saliendo del programa. ¡Hasta luego!")
            return
        
        elif opcion == "1":
            createRoulette(currentUserId)
        
        elif opcion == "2":
            showUsers()
        
        else:
            print("Opción no válida. Por favor, intente de nuevo.")
        
        cls()