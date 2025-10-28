import sqlite3
import pandas as pd

## CREAR UN USUARIO ##

try:
    conn = sqlite3.connect("baseDeLaRuleta.db")

    cursor = conn.cursor()

    nuevoUsuario = "Martin"
    sqlInsertar = "INSERT INTO Usuario (nombreUsuario) VALUES (?)"

    cursor.execute(sqlInsertar, (nuevoUsuario,))

    conn.commit()

    print(f"¡El usuario ", nuevoUsuario, " fue agregado con éxito!")

except sqlite3.Error as e:
    print(f"Error al insertar datos en la base de datos: ", e)
    if conn:
        conn.rollback()

finally:
    if conn:
        conn.close()
        print("Saliendo de la base de datos")

print("-" * 20)

## VER USUARIOS ##

