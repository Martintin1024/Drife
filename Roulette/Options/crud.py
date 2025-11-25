import sqlite3
from Utilities.helpers import set_db_path, cls
import pandas as pd

def create(current_roulette_id, name_roulette):
    db_path = set_db_path()
    conn = None
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        print(f"Creando opciones para la ruleta '{name_roulette}'...")
        print("================================")
        option_name = input("¿Cual va a ser el nombre de la opción? ")
        while len(option_name.strip()) == 0:
            option_name = input("No se puede ingresar un nombre vacío. Por favor, ingrese el nombre de la opción: ")

        sql_create_option = """
        INSERT INTO Options (roulette_id, option_name) VALUES (?, ?)
        """

        cursor.execute(sql_create_option, (current_roulette_id, option_name,))
        conn.commit()

    except sqlite3.Error as e:
        print(f"Error al crear la opción: {e}")
        if conn:
            conn.rollback()

    else:
        print("¡La opción fue creada con éxito!")

    finally:
        if conn:
            conn.close()
            print("Saliendo de la base de datos")

    input()
    return

def view(current_roulette_id, name_roulette):
    db_path = set_db_path()
    conn = None
    print   (f"El id de la ruleta es: {current_roulette_id}")
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        print(f"Viendo opciones de la ruleta '{name_roulette}'...")
        print("================================")
        
        sql_show_options = """
        SELECT option_id, option_name FROM Options WHERE roulette_id = ?
        """

        cursor.execute(sql_show_options, (current_roulette_id,))
        results = cursor.fetchall()
        
        if results:
            df = pd.DataFrame(results, columns=['option_id', 'option_name'])
            print(df.to_string(index=False))
        else:
            print("No hay opciones para esta ruleta.")

    except sqlite3.Error as e:
        print(f"Error al acceder a la base de datos: {e}")
        if conn:
            conn.rollback()
    finally:
        if conn:
            conn.close()
            print("Saliendo de la base de datos")
    
    input()
    cls()
    return

def update_name(current_roulette_id, name_roulette):
    db_path = set_db_path()
    conn = None
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        sql_count_options = """
        SELECT COUNT(*) FROM Options WHERE roulette_id = ?
        """
        result = cursor.execute(sql_count_options, (current_roulette_id,))
        sql_count_options = result.fetchone()[0]

        if sql_count_options > 0:

            sql_show_options = """
            SELECT option_id, option_name from Options WHERE roulette_id = ?
            """
            cursor.execute(sql_show_options, (current_roulette_id,))
            results = cursor.fetchall()
        
            df = pd.DataFrame(results, columns=['option_id', 'option_name'])
            print(df.to_string(index=False))
        else:
            print("No hay opciones en esta ruleta.")
            input()
            cls()
            return

        print(f"Modificando opción de la ruleta '{name_roulette}'...")
        print("================================")
        option_id = input("Ingrese el ID de la opción que desea modificar: ")
        while len(option_id.strip()) == 0:
            option_id = input("No se puede ingresar un id vacío. Por favor, ingrese el id de la opción: ")
        new_option_name = input("Ingrese el nuevo nombre para la opción: ")
        while len(new_option_name.strip()) == 0:
            new_option_name = input("No se puede ingresar un nombre vacío. Por favor, ingrese el nombre de la opción: ")

        sql_modify_option = """
        UPDATE Options SET option_name = ? WHERE option_id = ? AND roulette_id = ?
        """

        cursor.execute(sql_modify_option, (new_option_name, option_id, current_roulette_id,))
        conn.commit()

    except sqlite3.Error as e:
        print(f"Error al modificar la opción: {e}")
        if conn:
            conn.rollback()

    else:
        print("¡La opción fue modificada con éxito!")

    finally:
        if conn:
            conn.close()
            print("Saliendo de la base de datos")

    input()
    cls()
    return

def delete(current_roulette_id, name_roulette):
    db_path = set_db_path()
    conn = None
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        sql_count_options = """
        SELECT COUNT(*) FROM Options WHERE roulette_id = ?
        """
        result = cursor.execute(sql_count_options, (current_roulette_id,))
        sql_count_options = result.fetchone()[0]

        if int(sql_count_options) > 0:

            sql_show_options = """
            Select option_id, option_name from Options WHERE roulette_id = ?
            """
            cursor.execute(sql_show_options, (current_roulette_id,))
            results = cursor.fetchall()
        
            df = pd.DataFrame(results, columns=['option_id', 'option_name'])
            print(df.to_string(index=False))
        else:
            print("No hay opciones en esta ruleta.")
            input()
            cls()
            return

        print(f"Borrando opción de la ruleta '{name_roulette}'...")
        print("================================")
        option_id = input("Ingrese el ID de la opción que desea borrar: ")
        while len(option_id.strip()) == 0:
            option_id = input("No se puede ingresar un id vacío. Por favor, ingrese el id de la opción: ")

        sql_delete_option = """
        DELETE FROM Options WHERE option_id = ? AND roulette_id = ?
        """

        cursor.execute(sql_delete_option, (option_id, current_roulette_id,))
        conn.commit()

    except sqlite3.Error as e:
        print(f"Error al borrar la opción: {e}")
        if conn:
            conn.rollback()

    else:
        print("¡La opción fue borrada con éxito!")

    finally:
        if conn:
            conn.close()
        print("Saliendo de la base de datos")
    
    input()
    cls()
    return