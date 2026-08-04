from fastapi import Depends, FastAPI, HTTPException, status
from sqlalchemy.orm import Session

import models
import schemas
from database import Base, engine, get_db

Base.metadata.create_all(bind=engine)

app = FastAPI()


@app.post(
    "/asignaturas",
    response_model=schemas.AsignaturaRespuesta,
    status_code=status.HTTP_201_CREATED,
)
def crear_asignatura(asignatura: schemas.AsignaturaCrear, db: Session = Depends(get_db)):
    
    horas_autonomas = (asignatura.creditos * 48) - asignatura.horas_presenciales

    
    if horas_autonomas < 10:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Las horas presenciales superan el límite permitido para el número de créditos.",
        )

    
    if asignatura.creditos >= 5 or horas_autonomas > 120:
        nivel_dificultad = "Avanzado"
    elif 3 <= asignatura.creditos <= 4:
        nivel_dificultad = "Intermedio"
    else:
        nivel_dificultad = "Básico"

    nueva_asignatura = models.Asignatura(
        nombre=asignatura.nombre,
        creditos=asignatura.creditos,
        horas_presenciales=asignatura.horas_presenciales,
        horas_autonomas=horas_autonomas,
        nivel_dificultad=nivel_dificultad,
    )

    db.add(nueva_asignatura)
    db.commit()
    db.refresh(nueva_asignatura)

    return nueva_asignatura


@app.get("/asignaturas/resumen", response_model=list[schemas.AsignaturaResumen])
def obtener_resumen(db: Session = Depends(get_db)):
    asignaturas = db.query(models.Asignatura).all()

    resumen = []
    for a in asignaturas:
        total_horas_semanales = round((a.horas_presenciales + a.horas_autonomas) / 16, 1)
        resumen.append(
            schemas.AsignaturaResumen(
                id=a.id,
                nombre=a.nombre,
                creditos=a.creditos,
                horas_presenciales=a.horas_presenciales,
                horas_autonomas=a.horas_autonomas,
                nivel_dificultad=a.nivel_dificultad,
                total_horas_semanales=total_horas_semanales,
            )
        )

    return resumen
