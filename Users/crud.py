import sqlite3
# import getpass as gp <-- Ya no sirve en GUI
from Utilities.helpers import set_db_path

# Ahora la función RECIBE nombre y contraseña, no los pide.
def register_new_user(user_name, pass_word):
    db_path = set_db_path()
    conn = None
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # Validación básica (esto antes lo hacías con un while)
        if not user_name.strip() or not pass_word.strip():
            return False, "Campos vacíos"

        sql_insert = "INSERT INTO Users (user_name, password) VALUES (?, ?)"
        cursor.execute(sql_insert, (user_name, pass_word))
        conn.commit()   
        return True, "Usuario creado con éxito"

    except sqlite3.Error as e:
        if conn:
            conn.rollback()
        return False, "Este usuario ya fue creado, ingrese uno nuevo"

    finally:
        if conn:
            conn.close()

# Lo mismo aquí: recibe los datos listos
def log_in_user(user_name, pass_word):
    db_path = set_db_path()
    conn = None
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        sql_search = "SELECT user_id, user_name FROM Users WHERE user_name = ? AND password = ?"
        cursor.execute(sql_search, (user_name, pass_word))

        result = cursor.fetchone()
        
        if result:
            return result[0] # Retornamos solo el ID
        else:
            return None # Falló el login

    except sqlite3.Error as e:
        return None
    
    finally:
        if conn:
            conn.close()

# (Las otras funciones de update/delete las adaptaremos después, 
# por ahora centrémonos en entrar al sistema)