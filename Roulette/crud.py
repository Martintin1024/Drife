import sqlite3
from Utilities.helpers import set_db_path

db_path = "Data/roulette_data.db"


def create_roulette(current_user_id):
    db_path = set_db_path()
    conn = None
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        print("Creando tabla de ruletas...")
        print(current_user_id)
        print("================================")
        name_roulette = input("¿Cual va a ser el nombre de la ruleta? ")

        sql_create_roulette = """
        INSERT INTO Roulettes (user_id, name_roulette) VALUES (?, ?)
        """

        cursor.execute(sql_create_roulette, (current_user_id, name_roulette,))
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

def select_roulette(current_user_id):
    db_path = set_db_path()
    conn = None
    id_roulette = None
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        sql_count_roulettes = """SELECT COUNT(*) FROM Roulettes WHERE user_id = ?"""
        cursor.execute(sql_count_roulettes, (current_user_id,))
        count_result = cursor.fetchone()

        if count_result[0] == 0:
            print("No hay ruletas disponibles para este usuario.")
            input()
            return None
        
        print("Seleccionar ruleta")
        print("================================")

        sql_show_roulettes = """
        SELECT roulette_id, name_roulette FROM Roulettes WHERE user_id = ?
        """

        cursor.execute(sql_show_roulettes, (current_user_id,))

        results = cursor.fetchall()

        if results:
            for row in results:
                print(f"ID: {row[0]} - Nombre: {row[1]}")
            selected_id = input("Ingrese el ID de la ruleta que desea seleccionar: ")
            id_roulette = int(selected_id)

            sql_name_roulette = """SELECT name_roulette FROM Roulettes WHERE roulette_id = ? AND user_id = ?"""
            cursor.execute(sql_name_roulette, (id_roulette, current_user_id,))
            name_result = cursor.fetchone()
            if name_result:
                print(f"Ruleta seleccionada: {name_result[0]}")
            else:
                print("La ruleta seleccionada no existe.")
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
    return id_roulette, name_result[0]

def update_roulette(current_user_id):
    db_path = set_db_path()
    conn = None
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        sql_count_roulettes = """SELECT COUNT(*) FROM Roulettes WHERE user_id = ?"""
        cursor.execute(sql_count_roulettes, (current_user_id,))
        count_result = cursor.fetchone()

        if count_result[0] == 0:
            print("No hay ruletas disponibles para este usuario.")
            input()
            return None

        print("Actualizar ruleta")
        print("================================")

        sql_show_roulettes = """
        SELECT roulette_id, name_roulette FROM Roulettes WHERE user_id = ?
        """

        cursor.execute(sql_show_roulettes, (current_user_id,))

        results = cursor.fetchall()

        if results:
            for row in results:
                print(f"ID: {row[0]} - Nombre: {row[1]}")
            selected_id = input("Ingrese el ID de la ruleta que desea actualizar: ")
            id_roulette = int(selected_id)
            new_name = input("Ingrese el nuevo nombre para la ruleta: ")

            sql_actualizar_ruleta = """
            UPDATE Roulettes SET name_roulette = ? WHERE roulette_id = ? AND user_id = ?
            """

            cursor.execute(sql_actualizar_ruleta, (new_name, id_roulette, current_user_id,))
            conn.commit()
            print("¡Ruleta actualizada con éxito!")
        else:
            print("No hay ruletas disponibles para este usuario.")

    except sqlite3.Error as e:
        print(f"Error al acceder a la base de datos: {e}")
        if conn:
            conn.rollback()

    finally:
        if conn:
            conn.close()

    input()
    return

def delete_roulette(current_user_id):
    db_path = set_db_path()
    conn = None
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        sql_count_roulettes = """SELECT COUNT(*) FROM Roulettes WHERE user_id = ?"""
        cursor.execute(sql_count_roulettes, (current_user_id,))
        count_result = cursor.fetchone()

        if count_result[0] == 0:
            print("No hay ruletas disponibles para este usuario.")
            input()
            return None

        print("Eliminar ruleta")
        print("================================")

        sql_show_roulettes = """
        SELECT roulette_id, name_roulette FROM Roulettes WHERE user_id = ?
        """

        cursor.execute(sql_show_roulettes, (current_user_id,))

        results = cursor.fetchall()

        if results:
            for row in results:
                print(f"ID: {row[0]} - Nombre: {row[1]}")
            selected_id = input("Ingrese el ID de la ruleta que desea eliminar: ")
            id_roulette = int(selected_id)

            sql_eliminar_ruleta = """
            DELETE FROM Roulettes WHERE roulette_id = ? AND user_id = ?
            """

            cursor.execute(sql_eliminar_ruleta, (id_roulette, current_user_id,))
            conn.commit()
            print("¡Ruleta eliminada con éxito!")
        else:
            print("No hay ruletas disponibles para este usuario.")

    except sqlite3.Error as e:
        print(f"Error al acceder a la base de datos: {e}")
        if conn:
            conn.rollback()

    finally:
        if conn:
            conn.close()

    input()
    return