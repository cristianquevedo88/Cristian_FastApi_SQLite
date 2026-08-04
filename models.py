from sqlalchemy import Column, Integer, String

from database import Base


class Asignatura(Base):
    __tablename__ = "asignaturas"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    nombre = Column(String, unique=True, index=True, nullable=False)
    creditos = Column(Integer, nullable=False)
    horas_presenciales = Column(Integer, nullable=False)

    horas_autonomas = Column(Integer, nullable=False)
    nivel_dificultad = Column(String, nullable=False)
