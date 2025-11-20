import sqlite3
import getpass as gp
import pandas as pd
from Utilities.helpers import set_db_path

def register_new_user():
    db_path = set_db_path()
    conn = None
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        print("REGISTRO DE NUEVO USUARIO")
        print("================================")
        user_name = input("NOMBRE DE USUARIO: ")
        pass_word = gp.getpass("CONTRASEÑA: ")
        if (not pass_word) or (not user_name):
            input("El nombre de usuario no puede estar vacío. Pulse enter para continuar.")
            return False

        sql_insertar = "INSERT INTO Users (user_name, password) VALUES (?, ?)"
        cursor.execute(sql_insertar, (user_name, pass_word))
        conn.commit()   
             

    except sqlite3.Error as e:
        print(f"Error al insertar datos en la base de datos: {e}. Pulse enter para continuar.")
        if conn:
            conn.rollback()
        return False

    else:
        print(f"¡El usuario {user_name} fue agregado con éxito!")

    finally:
        if conn:
            conn.close()
            input()
    return True

def log_in_user():
    db_path = set_db_path()
    conn = None
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        print("INICIO DE SESIÓN")
        print("================================")
        user_name = input("NOMBRE DE USUARIO: ")
        pass_word = gp.getpass("CONTRASEÑA: ")

        sql_buscar = "SELECT user_id, user_name FROM Users WHERE user_name = ? AND password = ?"
        cursor.execute(sql_buscar, (user_name, pass_word))

        result = cursor.fetchone()
        
        if result:
            current_user_id = result[0]
            print(f"¡Bienvenido {user_name}!")
        else:
            current_user_id = None
            print("Nombre de usuario o contraseña incorrectos.")

    except sqlite3.Error as e:
        print(f"Error al acceder a la base de datos: '{e}'. Pulse enter para continuar.")
        if conn:
            conn.rollback()

    
    finally:
        if conn:
            conn.close()
    input()
    return current_user_id


def show_users():
    db_path = set_db_path()
    conn = None
    try:
        conn = sqlite3.connect(db_path)
        
        cursor = conn.cursor()

        sql_mostrar = "SELECT * FROM Users"

        cursor.execute(sql_mostrar)

        results = cursor.fetchall()

        results_dF = pd.DataFrame(results)

        try:
            print(results_dF)
        except Exception as e:
            print(f"Error al mostrar los datos: {e}")

    finally:
        if conn:
            conn.close()
        input()
    return 
