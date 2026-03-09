import sqlite3
from Utilities.helpers import set_db_path

def create_option_db(roulette_id, option_name):
    if not option_name or not option_name.strip():
        return False, "El nombre no puede estar vacío"

    db_path = set_db_path()
    conn = None
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        sql = "INSERT INTO Options (roulette_id, option_name) VALUES (?, ?)"
        cursor.execute(sql, (roulette_id, option_name.strip()))
        conn.commit()
        return True, "Opción creada"

    except sqlite3.Error as e:
        return False, f"Error BD: {e}"
    finally:
        if conn: conn.close()

def get_options_db(roulette_id):
    db_path = set_db_path()
    conn = None
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        sql = "SELECT option_id, option_name FROM Options WHERE roulette_id = ?"
        cursor.execute(sql, (roulette_id,))
        return cursor.fetchall()
    except sqlite3.Error:
        return []
    finally:
        if conn: conn.close()

def update_option_db(roulette_id, option_id, new_name):
    if not new_name or not new_name.strip():
        return False, "Nombre vacío"

    db_path = set_db_path()
    conn = None
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        sql = "UPDATE Options SET option_name = ? WHERE option_id = ? AND roulette_id = ?"
        cursor.execute(sql, (new_name.strip(), option_id, roulette_id))
        conn.commit()
        return True, "Actualizado correctamente"
    except sqlite3.Error as e:
        return False, f"Error: {e}"
    finally:
        if conn: conn.close()

def delete_option_db(roulette_id, option_id):
    db_path = set_db_path()
    conn = None
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        sql = "DELETE FROM Options WHERE option_id = ? AND roulette_id = ?"
        cursor.execute(sql, (option_id, roulette_id))
        conn.commit()
        return True, "Eliminado correctamente"
    except sqlite3.Error as e:
        return False, f"Error: {e}"
    finally:
        if conn: conn.close()

def get_roulette_items_text(roulette_id):
    data = get_options_db(roulette_id)
    return [item[1] for item in data]