import sqlite3
import pandas as pd

def insertNewUser():
    try:
        conn = sqlite3.connect("baseDeLaRuleta.db")
        cursor = conn.cursor()

        userName = input("Ingresar nuevo usuario: ")
        if not userName:
            print("El nombre de usuario no puede estar vacío.")
            return

        sqlInsertar = "INSERT INTO Users (userName) VALUES (?)"
        cursor.execute(sqlInsertar, (userName,))
        conn.commit()        

    except sqlite3.Error as e:
        print(f"Error al insertar datos en la base de datos: ", e)
        if conn:
            conn.rollback()

    else:
        print(f"¡El usuario {userName} fue agregado con éxito!")

    finally:
        if conn:
            conn.close()
            print("Saliendo de la base de datos")

    return

def showUsers():
    try:
        conn = sqlite3.connect("baseDeLaRuleta.db")
        
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
            print("Escapando de Latam... " \
            "Digo de la base de datos")
    return