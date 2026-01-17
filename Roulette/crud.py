import sqlite3
from Utilities.helpers import set_db_path

def create_roulette_db(user_id, name_roulette):
    """Crea una ruleta y devuelve (True, Mensaje) o (False, Error)"""
    db_path = set_db_path()
    conn = None
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        sql_create = "INSERT INTO Roulettes (user_id, name_roulette) VALUES (?, ?)"
        cursor.execute(sql_create, (user_id, name_roulette))
        conn.commit()
        return True, "Ruleta creada con éxito"

    except sqlite3.Error as e:
        return False, f"Error SQL: {e}"
    finally:
        if conn: conn.close()

def get_user_roulettes(user_id):
    """Devuelve una lista de tuplas [(id, nombre), (id, nombre)...]"""
    db_path = set_db_path()
    conn = None
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        sql = "SELECT roulette_id, name_roulette FROM Roulettes WHERE user_id = ?"
        cursor.execute(sql, (user_id,))
        results = cursor.fetchall()
        return results # Retorna la lista (puede estar vacía)

    except sqlite3.Error:
        return []
    finally:
        if conn: conn.close()

def delete_roulette_db(user_id, roulette_id):
    """Borra una ruleta específica"""
    db_path = set_db_path()
    conn = None
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        sql = "DELETE FROM Roulettes WHERE roulette_id = ? AND user_id = ?"
        cursor.execute(sql, (roulette_id, user_id))
        conn.commit()
        return True
    except sqlite3.Error:
        return False
    finally:
        if conn: conn.close()

# Dejamos update y options para la próxima etapa