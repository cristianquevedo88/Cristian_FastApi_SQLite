from fastapi import FastAPI, HTTPException, status
import sqlite3
from typing import List
from database import obtener_conexion, inicializar_db
from schema import AprendizCrear, AprendizRespuesta

app = FastAPI(title="API con SQlite nativo")

inicializar_db()

@app.get("/") #decorador
def ruta_raiz():
    return {"mensaje": "API Conectada a la BD"}

@app.get("/aprendices", response_model=List[AprendizRespuesta])
def obtener_aprendices():
    """
    Obtener todos los aprendices de la base de datos.
    
    """
    with obtener_conexion() as conexion:
        cursor = conexion.cursor()
        cursor.execute("SELECT * FROM aprendiz")
        filas = cursor.fetchall()
        # convertimos cada fila en un diccionario y la devolvemos
        return [dict(fila) for fila in filas]


@app.post("/aprendices", response_model=AprendizRespuesta, status_code=status.HTTP_201_CREATED)
def crear_aprendiz(aprendiz: AprendizCrear):
    with obtener_conexion() as conexion:
        cursor = conexion.cursor()
        try:
            query = "INSERT INTO aprendiz(nombre, documento, programa) VALUES (?,?,?)"
            cursor.execute(query, (aprendiz.nombre, aprendiz.documento, aprendiz.programa))
            conexion.commit()

            # obtener el id del nuevo aprendiz
            nuevo_id = cursor.lastrowid
            return {**aprendiz.model_dump(), "id": nuevo_id}
        except sqlite3.IntegrityError:
            raise HTTPException(
                status_code=400,
                detail="El documento ingresado ya existe."
            )

