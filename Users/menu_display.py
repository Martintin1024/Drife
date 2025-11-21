def show_log_in_menu():
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