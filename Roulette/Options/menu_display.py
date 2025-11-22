def crud_menu(entity):
    print(f"MENÚ DE EDICIÓN DE LA RULETA: {entity.upper()}")
    print("Por favor, seleccione una opción:")
    print("=========================================")
    print("1. Agregar opciones")
    print("2. Ver opciones")
    print("3. Modificar opciones")
    print("4. Borrar opciones")
    print("0. Volver al menú principal")
    option = input("Opcion: ")
    try:
        return option
    except ValueError:
        print("Opción no válida. Por favor, intente de nuevo.")
        return None