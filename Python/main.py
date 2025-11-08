from UI.visualMenu import showLogInMenu, cls
from logic.actionMenues import actionMainMenu
from logic.functions import logInUser, registerNewUser

while True:
    option = showLogInMenu()

    if option == "1":
        continuing = logInUser()
        if continuing:
            actionMainMenu(currentUserId = continuing)
        else:
            cls()
            print("Inicio de sesión fallido. Intente de nuevo.")
    elif option == "2":
        registerNewUser()
        if continuing:
            print("Registro completado. Ahora puede iniciar sesión.")
    elif option == "0":
        break
    cls()