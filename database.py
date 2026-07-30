import sqlite3
DATABASE_NAME = 'sistema_aprendices.db'

def obtener_conexion():
    """
    Crear una conexion con la base de datos y retornarla en forma de diccionario.

    """
    conexion = sqlite3.connect(DATABASE_NAME)
    conexion.row_factory = sqlite3.Row
    return conexion

def inicializar_db():
    """
    Crear las tablas necesarias si es que no existen.
    
    """
    with obtener_conexion() as conexion:
        cursor = conexion.cursor()
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS aprendiz(
         id INTEGER PRIMARY KEY AUTOINCREMENT,
         nombre TEXT NOT NULL,
         documento TEXT UNIQUE NOT NULL,
         programa TEXT NOT NULL
         )
        """)
        conexion.commit()