from .functions import createRoulette, selectRoulette
from UI.visualMenu import  cls, showMainMenu, showRouletteMenu

def actionMainMenu(currentUserId = None):
    while True:

        opcion = showMainMenu()

        if opcion == "0":
            print("Saliendo del programa. ¡Hasta luego!")
            return
        
        elif opcion == "1":
            createRoulette(currentUserId)
        
        elif opcion == "2":
            currentRouletteId = selectRoulette(currentUserId)
            if currentRouletteId != None:
                ActionRouletteMenu(currentUserId, currentRouletteId)
        
        else:
            print("Opción no válida. Por favor, intente de nuevo.")
        
        cls()

def ActionRouletteMenu(currentUserId, currentRouletteId):
    while True:

        opcion = showRouletteMenu()

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
        
        cls()