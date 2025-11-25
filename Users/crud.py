import sqlite3
import getpass as gp
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
        while len(user_name.strip()) == 0:
            user_name = input("No se puede ingresar un nombre vacío. Por favor, ingrese el nombre de usuario: ")
        pass_word = gp.getpass("CONTRASEÑA: ")
        while len(pass_word.strip()) == 0:
            pass_word = input("No se puede ingresar una contraseña vacío. Por favor, ingrese la contraseña de vuelta: ")

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
            return current_user_id

    except sqlite3.Error as e:
        print(f"Error al acceder a la base de datos: '{e}'. Pulse enter para continuar.")
        if conn:
            conn.rollback()

    
    finally:
        if conn:
            conn.close()
    input()
    return int(current_user_id)

def update_user_password(current_user_id):
    db_path = set_db_path()
    conn = None
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        print("ACTUALIZAR CONTRASEÑA")
        print("================================")
        new_password = gp.getpass("NUEVA CONTRASEÑA: ")
        while len(new_password.strip()) == 0:
            new_password = input("No se puede ingresar una contraseña vacío. Por favor, ingrese la contraseña de vuelta: ")
        confirm_password = gp.getpass("CONFIRMAR CONTRASEÑA: ")

        if new_password != confirm_password:
            print("Las contraseñas no coinciden. Pulse enter para continuar.")
            return
        else:
            sql_actualizar = "UPDATE Users SET password = ? WHERE user_id = ?"
            cursor.execute(sql_actualizar, (new_password, current_user_id))
            conn.commit()

    except sqlite3.Error as e:
        print(f"Error al actualizar la contraseña: {e}. Pulse enter para continuar.")
        if conn:
            conn.rollback()

    else:
        print("¡Contraseña actualizada con éxito!")

    finally:
        if conn:
            conn.close()
    input()
    return

def update_user_name(current_user_id):
    db_path = set_db_path()
    conn = None
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        print("ACTUALIZAR NOMBRE DE USUARIO")
        print("================================")
        new_user_name = input("NUEVO NOMBRE DE USUARIO: ")
        while len(new_user_name.strip()) == 0:
            new_user_name = input("No se puede ingresar un nombre vacío. Por favor, ingrese el nombre de usuario: ")

        sql_actualizar = "UPDATE Users SET user_name = ? WHERE user_id = ?"
        cursor.execute(sql_actualizar, (new_user_name, current_user_id))
        conn.commit()

    except sqlite3.Error as e:
        print(f"Error al actualizar el nombre de usuario: {e}. Pulse enter para continuar.")
        if conn:
            conn.rollback()

    else:
        print("¡Nombre de usuario actualizado con éxito!")

    finally:
        if conn:
            conn.close()
    input()
    return

def delete_user_account(current_user_id):
    db_path = set_db_path()
    conn = None
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        print("ELIMINAR CUENTA DE USUARIO")
        print("================================")
        confirmation = input("¿Está seguro de que desea eliminar su cuenta? Esta acción no se puede deshacer. (s/n): ")
        if confirmation.lower() != 's':
            print("Eliminación de cuenta cancelada. Pulse enter para continuar.")
            return

        sql_eliminar = "DELETE FROM Users WHERE user_id = ?"
        cursor.execute(sql_eliminar, (current_user_id,))
        conn.commit()

    except sqlite3.Error as e:
        print(f"Error al eliminar la cuenta: {e}. Pulse enter para continuar.")
        if conn:
            conn.rollback()

    else:
        print("¡Cuenta eliminada con éxito!")

    finally:
        if conn:
            conn.close()
    input()
    return