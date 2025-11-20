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

        sql_crear_ruleta = """
        INSERT INTO Roulettes (user_id, name_roulette) VALUES (?, ?)
        """

        cursor.execute(sql_crear_ruleta, (current_user_id, name_roulette,))
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

        print("Seleccionar ruleta")
        print("================================")

        sql_mostrar_ruletas = """
        SELECT roulette_id, name_roulette FROM Roulettes WHERE user_id = ?
        """

        cursor.execute(sql_mostrar_ruletas, (current_user_id,))

        results = cursor.fetchall()

        if results:
            for row in results:
                print(f"ID: {row[0]} - Nombre: {row[1]}")
            selected_id = input("Ingrese el ID de la ruleta que desea seleccionar: ")
            id_roulette = int(selected_id)
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
    return id_roulette