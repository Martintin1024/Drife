import sqlite3
import pandas as pd
import getpass as gp

dbPath = "Database/baseDeLaRuleta.db"

def registerNewUser():
    conn = None
    try:
        conn = sqlite3.connect(dbPath)
        cursor = conn.cursor()

        print("REGISTRO DE NUEVO USUARIO")
        print("================================")
        userName = input("NOMBRE DE USUARIO: ")
        passWord = gp.getpass("CONTRASEÑA: ")
        if (not passWord) or (not userName):
            input("El nombre de usuario no puede estar vacío. Pulse enter para continuar.")
            return False

        sqlInsertar = "INSERT INTO Users (userName, passWord) VALUES (?, ?)"
        cursor.execute(sqlInsertar, (userName, passWord))
        conn.commit()   
             

    except sqlite3.Error as e:
        print(f"Error al insertar datos en la base de datos: {e}. Pulse enter para continuar.")
        if conn:
            conn.rollback()
        return False

    else:
        print(f"¡El usuario {userName} fue agregado con éxito!")

    finally:
        if conn:
            conn.close()
            input()
    return True

def logInUser():
    conn = None
    try:
        conn = sqlite3.connect(dbPath)
        cursor = conn.cursor()

        print("INICIO DE SESIÓN")
        print("================================")
        userName = input("NOMBRE DE USUARIO: ")
        passWord = gp.getpass("CONTRASEÑA: ")

        sqlBuscar = "SELECT * FROM Users WHERE userName = ? AND passWord = ?"
        cursor.execute(sqlBuscar, (userName, passWord))

        result = cursor.fetchone()
        
        if result:
            currentUserId = result[0]
            print(f"¡Bienvenido {userName}!")
        else:
            currentUserId = None
            print("Nombre de usuario o contraseña incorrectos.")

    except sqlite3.Error as e:
        print(f"Error al acceder a la base de datos: {e}. Pulse enter para continuar.")
        if conn:
            conn.rollback()

    
    finally:
        if conn:
            conn.close()
    input()
    return currentUserId


def showUsers():
    conn = None
    try:
        conn = sqlite3.connect(dbPath)
        
        cursor = conn.cursor()

        sqlMostrar = "SELECT * FROM Users"

        cursor.execute(sqlMostrar)

        results = cursor.fetchall()

        resultsDF = pd.DataFrame(results)

        try:
            print(resultsDF)
        except:
            print("Le pifiaste maestro")
        finally:
            print("Te la terminé de mostrar")

    except sqlite3.Error as e:
        print(f"Eta puta mielda no funsiona papi: {e}")
        if conn:
            conn.rollback()

    finally:
        if conn:
            conn.close()
        input()
    return 

def createRoulette(currentUserId):
    conn = None
    try:
        conn = sqlite3.connect(dbPath)
        cursor = conn.cursor()

        print("Creando tabla de ruletas...")
        print(currentUserId)
        print("================================")
        nameRoulette = input("¿Cual va a ser el nombre de la ruleta? ")

        sqlCrearRuleta = """
        INSERT INTO Roulettes (idUser, nameRoulette) VALUES (?, ?)
        """

        cursor.execute(sqlCrearRuleta, (currentUserId, nameRoulette,))
        conn.commit()

    except sqlite3.Error as e:
        print(f"Error al crear la ruleta: {e}")
        if conn:
            conn.rollback()

    else:
        print("¡La ruleta fue creada con éxito!")

    finally:
        if conn:
            conn.close()
            print("Saliendo de la base de datos")

    input()
    return

def selectRoulette(currentUserId):
    conn = None
    idRoulette = None
    try:
        conn = sqlite3.connect(dbPath)
        cursor = conn.cursor()

        print("Seleccionar ruleta")
        print("================================")

        sqlMostrarRuletas = """
        SELECT idRoulette, nameRoulette FROM Roulettes WHERE idUser = ?
        """

        cursor.execute(sqlMostrarRuletas, (currentUserId,))

        results = cursor.fetchall()

        if results:
            for row in results:
                print(f"ID: {row[0]} - Nombre: {row[1]}")
            selectedId = input("Ingrese el ID de la ruleta que desea seleccionar: ")
            idRoulette = int(selectedId)
        else:
            print("No hay ruletas disponibles para este usuario.")

    except sqlite3.Error as e:
        print(f"Error al acceder a la base de datos: {e}")
        if conn:
            conn.rollback()

    else:
        print("¡Ruleta seleccionada con éxito!")

    finally:
        if conn:
            conn.close()

    input()
    return idRoulette