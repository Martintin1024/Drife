import sqlite3
from Utilities.helpers import cls, set_db_path
import random

def spin_roulette(current_roulette_id, current_name_roulette):
    db_path = set_db_path()
    print(f"Has seleccionado la ruleta: {current_name_roulette}")
    input("Presiona Enter para girar la ruleta...")

    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        sql_select_options = "SELECT option_name FROM Options WHERE roulette_id = ?"
        cursor.execute(sql_select_options, (current_roulette_id,))

        results = cursor.fetchall()
        options = [row[0] for row in results]

        if not options:
            print("La ruleta no tiene opciones para girar.")
            return
        
        selected_option = random.choice(options)

        print(f"La ruleta ha girado y ha caído en: {selected_option}")

    except sqlite3.Error as e:
        print(f"Error al acceder a la base de datos: {e}")

    finally:
        if conn:
            conn.close()
        return