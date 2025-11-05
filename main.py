from funciones import insertNewUser, showUsers
print("BIENVENIDO AL FOKIN PROGRAMA DE LAS FOKIN RULETAS")
print("Por favor, seleccione una opción:")
print("1. Insertar nuevo usuario")
print("2. Mostrar usuarios")
print("0. Salir")

while True:
    opcion = input("Ingrese el número de la opción deseada: ")

    if opcion == "1":
        insertNewUser()
    elif opcion == "2":
        showUsers()
    elif opcion == "0":
        print("Saliendo del programa. ¡Hasta luego!")
        break
    else:
        print("Opción no válida. Por favor, intente de nuevo.")