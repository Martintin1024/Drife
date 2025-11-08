import os

def cls():
    os.system('cls' if os.name == 'nt' else 'clear')
    return

def showLogInMenu():
    print("BIENVENIDO AL FOKIN PROGRAMA DE LAS FOKIN RULETAS")
    print("Por favor, inicie sesión:")
    print("=========================================")
    print("1. Iniciar sesión")
    print("2. Registrarse")
    print("0. Salir")
    option = input("Opcion: ")
    try:
        return option
    except ValueError:
        print("Opción no válida. Por favor, intente de nuevo.")
        return None

def showMainMenu():
    print("BIENVENIDO AL FOKIN PROGRAMA DE LAS FOKIN RULETAS")
    print("Por favor, seleccione una opción:")
    print("=========================================")
    print("1. Crear ruleta")
    print("2. Mostrar usuarios")
    print("0. Salir")
    option = input("Opcion: ")
    try:
        return option
    except ValueError:
        print("Opción no válida. Por favor, intente de nuevo.")
        return None

def showRouletteMenu():
    print("MENÚ DE RULETA")
    print("Por favor, seleccione una opción:")
    print("=========================================")
    print("1. Jugar ruleta")
    print("2. Editar ruleta")
    print("3. Eliminar ruleta")
    print("0. Volver al menú principal")
    option = input("Opcion: ")
    try:
        return option
    except ValueError:
        print("Opción no válida. Por favor, intente de nuevo.")
        return None