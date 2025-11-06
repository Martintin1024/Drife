from visualMenu import showLogInMenu, cls
from actionMenues import actionMainMenu
from functions import logInUser, registerNewUser

while True:
    option = showLogInMenu()

    if option == 1:
        continuing = logInUser()
        if continuing:
            actionMainMenu()
        else:
            cls()
            print("Inicio de sesión fallido. Intente de nuevo.")
    elif option == 2:
        registerNewUser()
        cls()
        print("Registro completado. Ahora puede iniciar sesión.")
    elif option == 0:
        break
    cls()