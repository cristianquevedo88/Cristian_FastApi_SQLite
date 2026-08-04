from pydantic import BaseModel, ConfigDict, Field


class AsignaturaCrear(BaseModel):
    """Esquema de ENTRADA: solo lo que el usuario debe enviar."""

    nombre: str = Field(..., min_length=1, description="Nombre único de la asignatura")
    creditos: int = Field(..., ge=1, le=10, description="Número de créditos (1-10)")
    horas_presenciales: int = Field(..., ge=0, description="Horas presenciales de la asignatura")


class AsignaturaRespuesta(BaseModel):
    """Esquema de SALIDA: incluye todos los campos, incluidos los calculados."""

    id: int
    nombre: str
    creditos: int
    horas_presenciales: int
    horas_autonomas: int
    nivel_dificultad: str

    model_config = ConfigDict(from_attributes=True)


class AsignaturaResumen(AsignaturaRespuesta):
    """Esquema de SALIDA para /asignaturas/resumen con campo calculado al vuelo."""

    total_horas_semanales: float
