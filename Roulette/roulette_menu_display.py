def show_main_menu():
    print("BIENVENIDO AL FOKIN PROGRAMA DE LAS FOKIN RULETAS")
    print("Por favor, seleccione una opción:")
    print("=========================================")
    print("1. Crear ruleta")
    print("2. Seleccionar ruleta")
    print("0. Salir")
    option = input("Opcion: ")
    try:
        return option
    except ValueError:
        print("Opción no válida. Por favor, intente de nuevo.")
        return None

def show_roulette_menu():
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